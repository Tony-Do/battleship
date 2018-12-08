
"""
Battleship362
Sam
Kyle
Tony
"""

# Imports
import pygame, sys, random
from pygame.locals import *
from globals import *

IMAGES = {}
 
def main():
    """
    Setup of game components
    """
    global WINDOWSURFACE, GLOBALCLOCK, FONTSIZESMALL, LOCINFO, INFORECT, LOCRESET, RESETRECT, FONTSIZELARGE, EFFECTS
    global LOCNAMEPLATE1, LOCNAMEPLATE2, NAMEPLATE1RECT, NAMEPLATE2RECT, AILASTHIT, FONTSIZEMEDIUM, LOCMUTE, MUTERECT
    global ARTSIZE, OCEANSIZE

    pygame.init()
    GLOBALCLOCK = pygame.time.Clock()
    WINDOWSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Battleship362')
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    pygame.mixer.music.load("../Sounds/Battleship.ogg")
    pygame.mixer.music.play(-1)

    # BACKGROUND IMAGE FOR INTRO SCREEN
    IMAGES['background'] = pygame.image.load('images/background.jpg').convert_alpha()

    IMAGES['art'] = pygame.image.load('../Images/art.png')
    ARTSIZE = IMAGES['art'].get_size()
    IMAGES['artbigger'] = pygame.transform.scale(IMAGES['art'], (int(ARTSIZE[0]*3), int(ARTSIZE[1]*3)))

    IMAGES['ocean'] = pygame.image.load('../Images/ocean.png')
    OCEANSIZE = IMAGES['art'].get_size()
    IMAGES['oceanbigger'] = pygame.transform.scale(IMAGES['ocean'], (int(ARTSIZE[0] * 4), int(ARTSIZE[1] * 1)))

    # FONTS
    FONTSIZESMALL = pygame.font.Font('../Fonts/slkscr.ttf', 20)
    FONTSIZELARGE = pygame.font.Font('../Fonts/slkscr.ttf', 50)
    FONTSIZEMEDIUM = pygame.font.Font('../Fonts/slkscr.ttf', 40)

    # BUTTONS
    LOCINFO = FONTSIZESMALL.render("INFO", True, COLTEXT)
    INFORECT = LOCINFO.get_rect()
    INFORECT.topleft = (WINDOWWIDTH - 390, WINDOWHEIGHT - 100)
    LOCRESET = FONTSIZESMALL.render("RESET", True, COLTEXT)
    RESETRECT = LOCRESET.get_rect()
    RESETRECT.topleft = (WINDOWWIDTH - 550, WINDOWHEIGHT - 100)
    LOCMUTE = FONTSIZESMALL.render("MUTE", True, COLTEXT)
    MUTERECT = LOCMUTE.get_rect()
    MUTERECT.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 100)


    LOCNAMEPLATE1 = FONTSIZESMALL.render("Enemy", True, COLTEXT)
    NAMEPLATE1RECT = LOCNAMEPLATE1.get_rect()
    NAMEPLATE1RECT.topleft = (WINDOWWIDTH - 1010, WINDOWHEIGHT - 46)
    LOCNAMEPLATE2 = FONTSIZESMALL.render("You", True, COLTEXT)
    NAMEPLATE2RECT = LOCNAMEPLATE2.get_rect()
    NAMEPLATE2RECT.topleft = (WINDOWWIDTH - 1000, WINDOWHEIGHT - 770)

    
    # IMAGES, can add more in and cycle through
    EFFECTS = [pygame.image.load("../Images/explosion.png")]

    # Run displays, can be changed from while True to while not exit
    game_intro_display()
    while True:
        winner = main_game_loop()  # Game loop and pass through winning player
        game_end_display(winner)  # Display end screen


def main_game_loop():
    """
    Runs game loop
    """

    # Tiles cleared from fog of war
    shown_user_tiles = make_board(False)
    shown_opponent_tiles = make_board(False)

    # Create game boards
    user_board = make_board(None)
    opponent_board = make_board(None)
    shipSet = ["battleship", "cruiser", "destroyer", "submarine"]

    # Add ships to each board
    user_board = random_shipset_placement(user_board, shipSet)
    opponent_board = random_shipset_placement(opponent_board, shipSet)

    # Tuple of mouse position
    mouse_x_pos, mouse_y_pos = 0, 0

    # Keeps track of what the AI has selected in a matrix
    matrix = [[0 for x in range(10)] for y in range(10)]

    while True:
        # Background, Buttons, Boards
        WINDOWSURFACE.fill(COLBACKGROUND)
        WINDOWSURFACE.blit(LOCINFO, INFORECT)
        WINDOWSURFACE.blit(LOCMUTE, MUTERECT)
        WINDOWSURFACE.blit(LOCRESET, RESETRECT)
        WINDOWSURFACE.blit(LOCNAMEPLATE1,NAMEPLATE1RECT)
        WINDOWSURFACE.blit(LOCNAMEPLATE2,NAMEPLATE2RECT)
        
        draw_boards(user_board, shown_user_tiles, 1)
        draw_boards(opponent_board, shown_opponent_tiles, 2)

        pygame.draw.rect(WINDOWSURFACE, COLUSERSHIPS, (0, 0, 1200, 800), 25)  # screen border
        pygame.draw.rect(WINDOWSURFACE, COLBUTTON, (70, 70, 300, 300), 2)     # Board border
        pygame.draw.rect(WINDOWSURFACE, COLBUTTON, (70, 438, 300, 300), 2)    # Board2 border
        pygame.draw.rect(WINDOWSURFACE, COLTEXT, (WINDOWWIDTH - 395, WINDOWHEIGHT - 102, 58, 25), 2)  # help border
        pygame.draw.rect(WINDOWSURFACE, COLTEXT, (WINDOWWIDTH - 555, WINDOWHEIGHT - 102, 70, 25), 2)  # reset border
        pygame.draw.rect(WINDOWSURFACE, COLTEXT, (WINDOWWIDTH - 255, WINDOWHEIGHT - 102, 62, 25), 2)  # mute border

        pygame.draw.rect(WINDOWSURFACE, COLSHIP, (650, 600, 25, 25), 25)  # example ship
        pygame.draw.rect(WINDOWSURFACE, COLTILE, (650, 400, 25, 25), 25)  # example tile
        pygame.draw.rect(WINDOWSURFACE, COLUSERSHIPS, (650, 500, 25, 25), 25)  # example user hidden ships

        infoSurface, infoRectangle = create_writable_object('Damaged ships', FONTSIZESMALL, BLACK)
        infoRectangle.topleft = (TEXTPOS + 700, TEXTSIZE + 580)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        infoSurface, infoRectangle = create_writable_object('Friendly ships hidden by fog of war', FONTSIZESMALL, BLACK)
        infoRectangle.topleft = (TEXTPOS + 700, TEXTSIZE + 480)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        infoSurface, infoRectangle = create_writable_object('Untargeted waters', FONTSIZESMALL, BLACK)
        infoRectangle.topleft = (TEXTPOS + 700, TEXTSIZE + 380)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        menuSurface, menuRectangle = create_writable_object('Battleship', FONTSIZELARGE, BLACK)
        menuRectangle.center = (int(WINDOWWIDTH / 2) + 200, int(WINDOWHEIGHT / 2) - 300)
        WINDOWSURFACE.blit(menuSurface, menuRectangle)

        menuSurface, menuRectangle = create_writable_object('Battleship', FONTSIZELARGE, WHITE)
        menuRectangle.center = (int(WINDOWWIDTH / 2) + 197, int(WINDOWHEIGHT / 2) - 305)
        WINDOWSURFACE.blit(menuSurface, menuRectangle)

        menuSurface, menuRectangle = create_writable_object('362', FONTSIZEMEDIUM, BLACK)
        menuRectangle.center = (int(WINDOWWIDTH / 2) + 400, int(WINDOWHEIGHT / 2) - 300)
        WINDOWSURFACE.blit(menuSurface, menuRectangle)

        menuSurface, menuRectangle = create_writable_object('362', FONTSIZEMEDIUM, WHITE)
        menuRectangle.center = (int(WINDOWWIDTH / 2) + 397, int(WINDOWHEIGHT / 2) - 305)
        WINDOWSURFACE.blit(menuSurface, menuRectangle)

        infoSurface, infoRectangle = create_writable_object('Sink your opponents fleet!', FONTSIZESMALL, COLTEXT)
        infoRectangle.topleft = (TEXTPOS+621, TEXTSIZE + 120)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        infoSurface, infoRectangle = create_writable_object('Target and sink enemy ships while', FONTSIZESMALL, COLTEXT)
        infoRectangle.topleft = (TEXTPOS+621, TEXTSIZE + 180)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        infoSurface, infoRectangle = create_writable_object('they are hidden by the fog of war.', FONTSIZESMALL,
                                                            COLTEXT)
        infoRectangle.topleft = (TEXTPOS+621, TEXTSIZE + 210)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        infoSurface, infoRectangle = create_writable_object('Destroy all enemy ships before ', FONTSIZESMALL, COLTEXT)
        infoRectangle.topleft = (TEXTPOS+621, TEXTSIZE + 240)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        infoSurface, infoRectangle = create_writable_object('your fleet is gone.', FONTSIZESMALL, COLTEXT)
        infoRectangle.topleft = (TEXTPOS+621, TEXTSIZE + 270)
        WINDOWSURFACE.blit(infoSurface, infoRectangle)

        mouse_clicked = False

        check_for_quit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if INFORECT.collidepoint(event.pos):  # Access info
                    WINDOWSURFACE.fill(COLBACKGROUND)
                    info_display()
                if MUTERECT.collidepoint(event.pos):
                    if pygame.mixer.music.get_volume() == 1.0:
                        pygame.mixer.music.set_volume(0.0)
                    else:
                        pygame.mixer.music.set_volume(1.0)
                elif RESETRECT.collidepoint(event.pos):  # Reset game
                    main()
                else:
                    mouse_x_pos, mouse_y_pos = event.pos
                    mouse_clicked = True  # Click mouse at position
            elif event.type == MOUSEMOTION:
                mouse_x_pos, mouse_y_pos = event.pos  # update mouse pos

        tile_x_pos, tile_y_pos = find_tile_at(mouse_x_pos, mouse_y_pos)
        if tile_x_pos is not None and tile_y_pos is not None:
            if not shown_user_tiles[tile_x_pos][tile_y_pos]:
                mouseover_highlight(tile_x_pos, tile_y_pos)
            if not shown_user_tiles[tile_x_pos][tile_y_pos] and mouse_clicked:
                reveal_tile_animation(user_board, [(tile_x_pos, tile_y_pos)])
                shown_user_tiles[tile_x_pos][tile_y_pos] = True # Remove fog of war
                if check_revealed_tile(user_board, [(tile_x_pos, tile_y_pos)]):  # Correct selection of ship
                    left, top = find_top_left_pos(tile_x_pos, tile_y_pos, 1)
                    effect_animation((left, top))
                    if check_for_win(user_board, shown_user_tiles):
                        return "HUMANS"
                    if check_for_win(opponent_board, shown_opponent_tiles):
                        return "AI"
                ai_turn(user_board,shown_opponent_tiles,user_board,shown_user_tiles,matrix)
                if check_for_win(user_board, shown_user_tiles):
                    return "HUMANS"
                if check_for_win(opponent_board, shown_opponent_tiles):
                    return "AI"

        pygame.display.update()
        GLOBALCLOCK.tick(GAMEFPS)


def ai_turn(opponent_board, shown_opponent_tiles, user_board, shown_user_tiles, matrix):
    """
    Function gives the AI their turn. Decides the tile to click through ai_find_tile.
    Clicks returned tile, reveals on board 2.
    Displays if the AI shot was a hit or miss.
    """
    AI_X, AI_Y = ai_find_tile(opponent_board, matrix)
    if AI_X is not None and AI_Y is not None:
        if not shown_opponent_tiles[AI_X][AI_Y]:
            shown_opponent_tiles[AI_X][AI_Y] = True
            if check_revealed_tile(opponent_board, [(AI_X, AI_Y)]):
                print("Hit at " + str(AI_X) + ", " + str(AI_Y))
                matrix[AI_X][AI_Y] = 2
                if check_for_win(user_board,shown_user_tiles):
                    return "HUMANS"
                if check_for_win(opponent_board, shown_opponent_tiles):
                    return "AI"


def ai_find_tile(opponent_board, matrix):
    """
    Chooses a random tile
    """
    # Check through the matrix to make sure it hasn't been selected already##
    usable = True
    optimization = True

    while(usable and optimization):
        tile_x_pos = random.randint(0,9)
        tile_y_pos = random.randint(0,9)
        usable = check_matrix(tile_x_pos, tile_y_pos, matrix)
        optimization = check_optimized_turn(tile_x_pos, tile_y_pos, matrix, opponent_board)
        if usable is True and optimization is True: # need to change optimzation to check if adj are ships or just blank
            matrix[tile_x_pos][tile_y_pos] = 1      # use check_revealed_tile
            usable = False
            optimization = False
        else:
            usable = True
            optimization = True
            
    return tile_x_pos, tile_y_pos


def check_matrix(tile_x_pos, tile_y_pos, matrix):
    if matrix[tile_x_pos][tile_y_pos] == 1 or matrix[tile_x_pos][tile_y_pos] == 2:
        return False
    if matrix[tile_x_pos][tile_y_pos] == 0:
        return True


# never clicks on tile with all 4 adjacent targeted prior
def check_optimized_turn(tile_x_pos, tile_y_pos, matrix, opponent_board):
    numOfTargetedAdjacentTiles = 0
    try:
        if matrix[tile_x_pos - 1][tile_y_pos] == 1 and matrix[tile_x_pos - 1][tile_y_pos] != 2:
            numOfTargetedAdjacentTiles += 1
    except:
        numOfTargetedAdjacentTiles += 1
    try:
        if matrix[tile_x_pos + 1][tile_y_pos] == 1 and matrix[tile_x_pos + 1][tile_y_pos] != 2:
            numOfTargetedAdjacentTiles += 1
    except:
        numOfTargetedAdjacentTiles += 1
    try:
        if matrix[tile_x_pos][tile_y_pos + 1] == 1 and matrix[tile_x_pos][tile_y_pos + 1] != 2:
            numOfTargetedAdjacentTiles += 1
    except:
        numOfTargetedAdjacentTiles += 1
    try:
        if matrix[tile_x_pos][tile_y_pos - 1] == 1 and matrix[tile_x_pos][tile_y_pos - 1] != 2:
            numOfTargetedAdjacentTiles += 1
    except:
        numOfTargetedAdjacentTiles += 1
    if numOfTargetedAdjacentTiles == 4:
        return False
    return True


def make_board(entry_tile_value):
    """
    Creates y-tiles by x-tiles with an entry value passed in
    """
    entry_tiles = [[entry_tile_value] * BOARDYTILES for i in range(BOARDXTILES)]

    return entry_tiles


def effect_animation(tile_needs_effect):
    """
    Image loop for effect on a specific tile, will run multiple sprite png's
    """
    for image in EFFECTS:
        image = pygame.transform.scale(image, (TILESIZE + 50, TILESIZE + 50))
        WINDOWSURFACE.blit(image, tile_needs_effect)
        pygame.display.flip()
        GLOBALCLOCK.tick(EFFECTFPS)


def check_revealed_tile(board, tile):
    """
    Check if ship
    """
    return board[tile[0][0]][tile[0][1]] is not None


def reveal_tile_animation(board, tile_to_reveal):
    """
    Uncover tiles, explosion animation is CLICKSPEED
    """
    for covered in range(TILESIZE, (-CLICKSPEED) - 1, -CLICKSPEED):
        draw_tile_surface(board, tile_to_reveal, covered)


def draw_tile_surface(board, tile, covered):
    """
    Updates tile image
    """
    left, top = find_top_left_pos(tile[0][0], tile[0][1], 1)
    if check_revealed_tile(board, tile):
        pygame.draw.rect(WINDOWSURFACE, COLSHIP, (left, top, TILESIZE, TILESIZE))
    else:
        pygame.draw.rect(WINDOWSURFACE, COLBACKGROUND, (left, top, TILESIZE, TILESIZE))
    if covered > 0:
        pygame.draw.rect(WINDOWSURFACE, COLTILE, (left, top, covered, TILESIZE))

    pygame.display.update()
    GLOBALCLOCK.tick(GAMEFPS)


def check_for_quit():
    """
    Quick check for pygame quit event
    """
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()


def check_for_win(board, revealed):
    """
    Checks current board state for winner, check if every tile with a ship is shown
    """
    for tile_x_pos in range(BOARDXTILES):
        for tile_y_pos in range(BOARDYTILES):
            if board[tile_x_pos][tile_y_pos] is not None and not revealed[tile_x_pos][tile_y_pos]:
                return False
    return True


def draw_boards(board, revealed, player):
    """
    Prints boards to window
    """
    if player is 1:
        for tile_x_pos in range(BOARDXTILES):
            for tile_y_pos in range(BOARDYTILES):
                left, top = find_top_left_pos(tile_x_pos, tile_y_pos, player)
                if not revealed[tile_x_pos][tile_y_pos]:
                    pygame.draw.rect(WINDOWSURFACE, COLTILE, (left, top, TILESIZE, TILESIZE))
                else:
                    if board[tile_x_pos][tile_y_pos] is not None:
                        pygame.draw.rect(WINDOWSURFACE, COLSHIP, (left, top, TILESIZE, TILESIZE))
                    else:
                        pygame.draw.rect(WINDOWSURFACE, COLBACKGROUND, (left, top, TILESIZE, TILESIZE))
    if player is 2:
        for tile_x_pos in range(BOARDXTILES):
            for tile_y_pos in range(BOARDYTILES):
                left, top = find_top_left_pos(tile_x_pos, tile_y_pos, player)
                if not revealed[tile_x_pos][tile_y_pos]:
                    if board[tile_x_pos][tile_y_pos] is not None:
                        pygame.draw.rect(WINDOWSURFACE, COLUSERSHIPS, (left, top, TILESIZE, TILESIZE))
                    else:
                        pygame.draw.rect(WINDOWSURFACE, COLTILE, (left, top, TILESIZE, TILESIZE))
                else:
                    if board[tile_x_pos][tile_y_pos] is not None:
                        pygame.draw.rect(WINDOWSURFACE, COLSHIP, (left, top, TILESIZE, TILESIZE))
                    else:
                        pygame.draw.rect(WINDOWSURFACE, COLBACKGROUND, (left, top, TILESIZE, TILESIZE))


def random_shipset_placement(board, ships):
    """
    Brute force placement of ships on a new board
    """
    new_board = board[:]
    ship_length = 0
    for ship in ships:

        valid_pos = False

        while not valid_pos:
            orientationisHorizontal = random.randint(0, 1)

            xStartpos = random.randint(0, 9)
            yStartpos = random.randint(0, 9)

            if 'destroyer' in ship:
                ship_length = 5
            elif 'cruiser' in ship:
                ship_length = 3
            elif 'battleship' in ship:
                ship_length = 4
            elif 'submarine' in ship:
                ship_length = 2

            # valid_pos set to true if ship placement is valid
            valid_pos, ship_coords = add_ship(new_board, xStartpos, yStartpos, orientationisHorizontal, ship_length, ship)

            if valid_pos:
                for coord in ship_coords:
                    new_board[coord[0]][coord[1]] = ship
    return new_board


def add_ship(board, xTile, yTile, orientationIsHorizontal, length, ship):
    """
    Ship placer
    """
    coords = []
    if orientationIsHorizontal:
        for i in range(length):
            if (i + xTile > 9) or (board[i + xTile][yTile] is not None) or has_adj(board, i + xTile, yTile, ship):
                return False, coords
            else:
                coords.append((i + xTile, yTile))
    else:
        for i in range(length):
            if (i + yTile > 9) or (board[xTile][i + yTile] is not None) or has_adj(board, xTile, i + yTile, ship):
                return False, coords
            else:
                coords.append((xTile, i + yTile))
    return True, coords


def has_adj(board, xTile, yTile, ship):
    """
    Checks for adjacent objects
    """
    for x in range(xTile - 1, xTile + 2):
        for y in range(yTile - 1, yTile + 2):
            if (x in range(10)) and (y in range(10)) and (board[x][y] not in (ship, None)):
                return True
    return False


def find_top_left_pos(tile_x_pos, tile_y_pos, player):
    """
    Find tile of top left corner
    """
    offset = 40
    if player is 1:
        left = tile_x_pos * TILESIZE + BOARDONEXPOINT + offset
        top = tile_y_pos * TILESIZE + BOARDONEYPOINT + offset
    if player is 2:
        left = tile_x_pos * TILESIZE + BOARDTWOXPOINT + offset
        top = tile_y_pos * TILESIZE + BOARDTWOYPOINT + offset
    return left, top


def find_tile_at(x, y):
    """
    Returns tile at a position
    """
    for tile_x_pos in range(BOARDXTILES):
        for tile_y_pos in range(BOARDYTILES):
            left, top = find_top_left_pos(tile_x_pos, tile_y_pos, 1)
            tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tile_rect.collidepoint(x, y):
                return tile_x_pos, tile_y_pos
    return None, None


def mouseover_highlight(tile_x_pos, tile_y_pos):
    """
    Highlights current tile
    """
    left, top = find_top_left_pos(tile_x_pos, tile_y_pos, 1)
    pygame.draw.rect(WINDOWSURFACE, COLHIGHLIGHT, (left, top, TILESIZE, TILESIZE), 2)


def info_display():
    """
    Display info  screen
    """

    WINDOWSURFACE.blit(IMAGES['oceanbigger'], (535, 725))
    WINDOWSURFACE.blit(IMAGES['oceanbigger'], (13, 725))
    WINDOWSURFACE.blit(IMAGES['artbigger'], (475, 545))

    pygame.draw.rect(WINDOWSURFACE, COLUSERSHIPS, (0, 0, 1200, 800), 25)  # border

    menuSurface, menuRectangle = create_writable_object('Battleship', FONTSIZELARGE, BLACK)
    menuRectangle.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)-320)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('Battleship', FONTSIZELARGE, WHITE)
    menuRectangle.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2)-325)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('362', FONTSIZEMEDIUM, BLACK)
    menuRectangle.center = (int(WINDOWWIDTH / 2) + 200, int(WINDOWHEIGHT / 2) - 320)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('362', FONTSIZEMEDIUM, WHITE)
    menuRectangle.center = (int(WINDOWWIDTH / 2) + 197, int(WINDOWHEIGHT / 2) - 325)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    infoSurface, infoRectangle = create_writable_object('"Sink your opponents fleet!', FONTSIZESMALL, COLTEXT)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 90)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('Target and sink enemy ships while', FONTSIZESMALL, COLTEXT)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 150)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('they are hidden by the fog of war.', FONTSIZESMALL, COLTEXT)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 180)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('Destroy all enemy ships before ', FONTSIZESMALL, COLTEXT)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 210)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('your fleet is gone."', FONTSIZESMALL, COLTEXT)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 240)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('This game was made in Python 3.6', FONTSIZESMALL, WHITE)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 300)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('using the PyGame Library.', FONTSIZESMALL, WHITE)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 330)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('Authors:', FONTSIZESMALL, WHITE)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 390)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('Kyle Guss', FONTSIZESMALL, WHITE)
    infoRectangle.topleft = (TEXTPOS+20, TEXTSIZE + 420)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('Tony Do', FONTSIZESMALL, WHITE)
    infoRectangle.topleft = (TEXTPOS+20, TEXTSIZE + 450)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('Sam Yeaw', FONTSIZESMALL, WHITE)
    infoRectangle.topleft = (TEXTPOS + 20, TEXTSIZE + 480)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)

    infoSurface, infoRectangle = create_writable_object('Music by Patrick de Arteaga.', FONTSIZESMALL, WHITE)
    infoRectangle.topleft = (TEXTPOS, TEXTSIZE + 540)
    WINDOWSURFACE.blit(infoSurface, infoRectangle)


    while check_for_key_up() is None:
        pygame.display.update()
        GLOBALCLOCK.tick()


def check_for_key_up():
    """
    Only returns keyup events
    """
    for event in pygame.event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]):
        if event.type in (KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION):
            continue
        return event.key
    return None


def create_writable_object(text, font, color):
    """
    Easy print to screen function returns surface, rectangle
    """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def game_end_display(winner):
    """
    Displays end screen
    """
    WINDOWSURFACE.fill(COLBACKGROUND)

    pygame.draw.rect(WINDOWSURFACE, COLUSERSHIPS, (0, 0, 1200, 800), 25)  # border

    menuSurface, menuRectangle = create_writable_object('Oh yeah!', FONTSIZELARGE, COL3DTEXT)
    menuRectangle.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('Oh yeah!', FONTSIZELARGE, COLTEXT)
    menuRectangle.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 5)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object(str(winner) + ' are the Winner', FONTSIZELARGE, COL3DTEXT)
    menuRectangle.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 + 50))
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object(str(winner) + ' are the Winner', FONTSIZELARGE, COLTEXT)
    menuRectangle.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2 + 50) - 5)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    pressKeySurf, pressKeyRect = create_writable_object('Press a key to play again', FONTSIZESMALL, COLTEXT)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    WINDOWSURFACE.blit(pressKeySurf, pressKeyRect)

    while check_for_key_up() is None:
        pygame.display.update()
        GLOBALCLOCK.tick()

def game_intro_display():
    """
    Displays intro screen
    """

    WINDOWSURFACE.fill(COLBACKGROUND)
    WINDOWSURFACE.blit(IMAGES['background'],(0,0))
    

    menuSurface, menuRectangle = create_writable_object('Welcome!', FONTSIZELARGE, BLACK)
    menuRectangle.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 - 200))
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('Welcome!', FONTSIZELARGE, WHITE)
    menuRectangle.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2 - 200) - 5)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('Lets Play Battleship', FONTSIZELARGE, BLACK)
    menuRectangle.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 - 50))
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('Lets Play Battleship', FONTSIZELARGE, WHITE)
    menuRectangle.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2 - 50) - 5)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)

    menuSurface, menuRectangle = create_writable_object('Press any key to continue', FONTSIZESMALL, WHITE)
    menuRectangle.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2 + 300) - 5)
    WINDOWSURFACE.blit(menuSurface, menuRectangle)


    while check_for_key_up() is None:
        pygame.display.update()
        GLOBALCLOCK.tick()


if __name__ == "__main__":
    main()
