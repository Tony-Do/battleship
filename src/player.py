###########
# IMPORTS #
###########
import ship




####################################################
# CLASS MatrixBlock
# --------------------------------------------------
# A block of the matrix
####################################################
class MatrixBlock:

    hasShip = False
    hasBeenShot = False

####################################################
# CLASS Player
# --------------------------------------------------
# This class represents a player, either the user or
# the AI. It contains the player's battlefield, the
# enemy's battlefield, and the ships at his or her
# disposal
####################################################
class Player:

    # CONSTRUCTOR
    def __init__(self):
        # ATTRIBUTES
        self.__ships = ship.ShipSet(True)  # Initializes a full collection of ships (as opposed to an empty on
        self.__my_field = Field(True)  # Initializes the player's field, with fog of war off
        self.__opponent_field = Field(False)  # Initializes the enemy's field, with fog of war on

    # PUBLIC METHODS
    # place_ship - Adds a ship to the player's field
    def place_ship(self, ship_name, coordinate, orientation):
        # Check if ship is in ship set
        if not self.__ships.ship_exists(ship_name):
            return False   

        # Pop that ship from self.__ships
        ship = self.__ships.pop(ship_name)
    
        # Place it into the field at the right coordinate
        self.__my_field.place(ship, coordinate, orientation)
            
        return True

    # attack - Attacks the enemy's field
    def attack(self, x_coordinate, y_coordinate):
        # TODO
        pass

    # OVERRIDEN METHODS
    # __str__ - convert player object into a string
    def __str__(self):
        output = "ENEMY FIELD\n"
        output = output + str(self.__opponent_field) + "\n\n"
        output = output + "MY FIELD\n"
        output = output + str(self.__my_field) + "\n"
        output = output + "SHIPS TO PLACE\n"
        output = output + str(self.__ships)
        return output


####################################################
# CLASS Field
# --------------------------------------------------
# This class represents a field. It can be
# initialized with or without the fog of war
####################################################
class Field:

    # CONSTRUCTOR
    def __init__(self, fog_of_war):
        # ATTRIBUTES
        self.__fog_of_war = fog_of_war  # Sets the fog of war to on or off
        self.__matrix = self.__init_matrix()  # Initializes the matrix

    # PUBLIC METHODS
    # place a ship into field
    # convert coordinate to matrix format and place ship according to orientation
    def place(self, ship, coordinate, rawOrientation):

        # prints all placement info
        print("Placing ship at " + coordinate + " with orientation of " + rawOrientation)

        # convert Column from letter to number
        matrixCol = ord(coordinate[0])-65
        print(matrixCol)
        matrixRow = int(coordinate[1]) - 1
        print(matrixRow)

        # determines endpoint for VERTICAL/HORIZONTAL placement of ships, if > 10 it is out of bounds
        #TODO THIS STILL DOESNT WORK DAMN IT

        rawOrientation = rawOrientation.lower()
        if rawOrientation == "horizontal":
            print("Entered horizontal placement")
            end_point = ship.length + int(matrixRow)
            if end_point > 10:
                print('{0} = OUT OF BOUNDS'.format(str(end_point)))
            for i in range(ship.length):
                self.__matrix[matrixRow][int(matrixCol) + i] = 1
        elif rawOrientation == "vertical":
            print("Entered vertical placement")
            end_point = ship.length + int(matrixCol)
            if end_point > 10:
                print('{0} = OUT OF BOUNDS'.format(str(end_point)))
            for i in range(ship.length):
                self.__matrix[matrixRow + i][int(matrixCol)] = 1
        else:
            print("*** Error - " + rawOrientation + " is an invalid orientation (Please choose vertical/horizontal)")
        print(rawOrientation)

        # TODO if out of bounds, don't actually place the ship

    # PRIVATE METHODS
    # init_matrix - returns an initialized matrix. For internal class use only
    def __init_matrix(self):
        return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def __convert_coordinate(self, coordinate):
        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        column_letter = coordinate[0]
        row = coordinate[1] - 1

        column_letter = column_letter.upper()
        column = columns.index(column_letter)

        return [row, column]

    # converting to string variable
    def __str__(self):
        output = "  A, B, C, D, E, F, G, H, I, J \n"
        output = output + "------------------------------" + "\n"
        for x in self.__matrix:
            output = output + "|" + str(x) + "\n"
            output = output + "------------------------------" + "\n"
        return output

    # MAIN
    if __name__ == "__main__":
        player1 = Player()
        print(str(player1))
