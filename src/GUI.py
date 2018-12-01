###########
# IMPORTS #
###########
import pygame
import time

#############
# CONSTANTS #
#############

display_width = 1000
display_height = 1000
black = (0, 0, 0)  # RGB concentrations
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

####################
# INITIALIZE BOARD #
####################

pygame.init()  # initiates pygame
gameDisplay = pygame.display.set_mode((display_width, display_height,))  # board size
pygame.display.set_caption('Battleship')  # game title

clock = pygame.time.Clock()  # a real time clock

carrier = pygame.image.load('images/carrier1.png').convert()  # loads a carrier photo onto the carrier variable

background = pygame.image.load('images/background.jpg').convert()


##############
# FUNCTIONS  #
##############


def battleship(x, y):
    x = x - 20
    y = y - 20
    gameDisplay.blit(carrier, (x - 10, y - 10))


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 45)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


def message_intro():
    message_display('Welcome to Battleship!')


def button(msg, xcoordinate, ycoordinate, recwidth, recheight, inactive, active, action=None):
    mouse = pygame.mouse.get_pos()
    # print(mouse)
    click = pygame.mouse.get_pressed()  # mouse press registers as [ left, middle, right]
    # print(click)

    if xcoordinate + recwidth > mouse[0] > xcoordinate and ycoordinate + recheight > mouse[1] > ycoordinate:
        # if mouse coordinates are between (150,450), highlight the respected boxes
        pygame.draw.rect(gameDisplay, inactive, (xcoordinate, ycoordinate, recwidth, recheight))

        if click[0] == 1 and action != None:  # if left click is pressed on one of the actions, x action is performed
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, active, (xcoordinate, ycoordinate, recwidth, recheight))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((xcoordinate + (recwidth / 2)), (ycoordinate + (recheight / 2)))
    gameDisplay.blit(textSurf, textRect)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        message_intro()

        button("Play", 150, 450, 100, 50, green, bright_green, "play")
        button("Quit", 450, 450, 100, 50, red, bright_red, "quit")

        pygame.display.update()
        clock.tick(60)


def game_loop():
    x = (display_width * 0.1)
    y = (display_height * 0.1)

    gameExit = False  # declares an end variable for when the user exits the game

    while not gameExit:  # while the user doesn't exit out the game

        ###########################
        # EVENT HANDLING LOOP     #
        ###########################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user presses the exit window
                pygame.quit()
                quit()

        gameDisplay.fill(white)  # fills up entire GUI with white space
        battleship(x, y)  # place battleship at x,y coordinates

        pygame.display.flip()  # will update the entire GUI
        clock.tick(20)  # frames per second game. Can increase to 60


######
# MAIN#
######

game_intro()
game_loop()

########
# EXIT #
########

pygame.quit()  # quits pygame and closes the GUI
quit()
