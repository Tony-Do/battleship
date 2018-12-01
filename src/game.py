import random, sys, pygame
from pygame.locals import *

xrange = range
FPS = 20 #frames per second
REVEALSPEED = 10 #matrix spot reload
WINDOWWIDTH = 1200 #width of game
WINDOWHEIGHT = 800 #height of game
TILESIZE = 40 #size of tiles
BUTTONHEIGHT = 30 #button sizing
BUTTONWIDTH = 50 #button sizing
TEXT_HEIGHT = 25 #text size
TEXT_LEFT_POSN = 10 #text posn
BOARDWIDTH = 10 #grid size
BOARDHEIGHT = 10 #grid size
DISPLAYWIDTH = 200 #width of board
EXPLOSIONSPEED = 10 #speed of explosions

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE) - DISPLAYWIDTH) / 2) #xpos top left board
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE)) / 2) #ypos of top left board

#Color Control
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GREEN   = (  0, 204,   0)
GRAY    = ( 60,  60,  60)
BLUE    = (  0,  50, 255)
YELLOW  = (255, 255,   0)
DARKGRAY =( 40,  40,  40)

BGCOLOR = GRAY
BUTTONCOLOR = GREEN
TEXTCOLOR = WHITE
TILECOLOR = GREEN
BORDERCOLOR = BLUE
TEXTSHADOWCOLOR = BLUE
SHIPCOLOR = YELLOW
HIGHLIGHTCOLOR = BLUE


def main():
    """
    Initialization of game
    """
    global DISPLAYSURF, FPSCLOCK, BASICFONT, HELP_SURF, HELP_RECT, NEW_SURF, \
        NEW_RECT, SHOTS_SURF, SHOTS_RECT, BIGFONT, COUNTER_SURF, \
        COUNTER_RECT, HBUTTON_SURF, EXPLOSION_IMAGES
    pygame.init()
    PYCLOCK = pygame.time.Clock()
    # Fonts used by the game
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 50)

    # Create and label the buttons
    HELP_SURF = BASICFONT.render("RULES", True, WHITE)
    HELP_RECT = HELP_SURF.get_rect()
    HELP_RECT.topleft = (WINDOWWIDTH - 180, WINDOWHEIGHT - 350)
    NEW_SURF = BASICFONT.render("NEW", True, WHITE)
    NEW_RECT = NEW_SURF.get_rect()
    NEW_RECT.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 200)

    # The 'Shots:' label at the top
    SHOTS_SURF = BASICFONT.render("Shots: ", True, WHITE)
    SHOTS_RECT = SHOTS_SURF.get_rect()
    SHOTS_RECT.topleft = (WINDOWWIDTH - 750, WINDOWHEIGHT - 570)

    # Load the explosion graphics from the /img folder
    EXPLOSION_IMAGES = [
        pygame.image.load("img/blowup1.png"), pygame.image.load("img/blowup2.png"),
        pygame.image.load("img/blowup3.png"), pygame.image.load("img/blowup4.png"),
        pygame.image.load("img/blowup5.png"), pygame.image.load("img/blowup6.png")]

    # Set the title in the menu bar to 'Battleship'
    pygame.display.set_caption('Battleship')

    # Keep the game running at all times
    while True:
        winner = run_game()  # Run the game until it stops and save the result in shots_taken
        show_gameover_screen(winner)  # Display a gameover screen by passing in shots_taken
