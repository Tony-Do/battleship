###########
# IMPORTS #
###########
import ship
import random



####################################################
# CLASS MatrixBlock
# --------------------------------------------------
# A block of the matrix
####################################################
class MatrixBlock:

    def __init__(self):
        self.hasShip = False
        self.hasBeenShot = False
        self.shipName = ""

    def __str__(self):
        if self.shipName == "":
            return " "
        else:
            return self.shipName[0]

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
            raise Exception("*** Ship does not exist")
        # Check if all ships have been placed
        if len(self.__ships) == 0:
            raise Exception("*** All ships have been placed!")

        # Pop that ship from self.__ships
        ship = self.__ships.get(ship_name)
    
        # Place it into the field at the right coordinate
        self.__my_field.place(ship, coordinate, orientation)

        self.__ships.pop(ship_name)
            
        return True

    # attack - Attacks the enemy's field
    def attack(self, x_coordinate, y_coordinate):
        print("TODO")

    # OVERRIDEN METHODS
    # __str__ - convert player object into a string
    def __str__(self):
        output = "ENEMY FIELD\n"
        output = output + str(self.__opponent_field) + "\n\n"
        output = output + "MY FIELD\n"
        output = output + str(self.__my_field) + "\n"
        if len(self.__ships) == 0:
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
    def place(self, a_ship, coordinate, rawOrientation):

        # prints all placement info
        print("Placing ship at " + coordinate + " with orientation of " + rawOrientation)

        # convert Column from letter to number
        matrixCol = ord(coordinate[0].upper())-65
        print(matrixCol)
        matrixRow = int(coordinate[1:]) - 1
        print(matrixRow)

        # determines endpoint for VERTICAL/HORIZONTAL placement of ships, if > 10 it is out of bounds
        #TODO THIS STILL DOESNT WORK DAMN IT

        rawOrientation = rawOrientation.lower()
        if rawOrientation == "horizontal":
            print("Entered horizontal placement")
            end_point = a_ship.length + int(matrixRow)
            if end_point > 10:
                raise Exception('{0} = OUT OF BOUNDS'.format(str(end_point)))
            for index in range(matrixCol, matrixCol + len(a_ship)):
                if self.__matrix[matrixRow][index].hasShip == True:
                    raise Exception("*** placement conflicts with previously placed ship")
            for i in range(a_ship.length):
                self.__matrix[matrixRow][int(matrixCol)+i].hasShip = True
                self.__matrix[matrixRow][int(matrixCol)+i].shipName = a_ship.get_name()

        elif rawOrientation == "vertical":
            print("Entered vertical placement")
            end_point = a_ship.length + int(matrixCol)
            if end_point > 10:
                raise Exception('{0} = OUT OF BOUNDS'.format(str(end_point)))
            for index in range(matrixRow, matrixRow + len(a_ship)):
                print(str(self.__matrix[index][matrixCol]))
                if self.__matrix[index][matrixCol].hasShip == True:
                    raise Exception("*** placement conflicts with previously placed ship")
            for i in range(a_ship.length):
                self.__matrix[matrixRow+i][int(matrixCol)].hasShip = True
                self.__matrix[matrixRow+i][int(matrixCol)].shipName = a_ship.get_name()

        else:
            print("*** Error - " + rawOrientation + " is an invalid orientation (Please choose vertical/horizontal)")
        print(rawOrientation)

        # TODO if out of bounds, don't actually place the ship

    # PRIVATE METHODS
    # init_matrix - returns an initialized matrix. For internal class use only
    def __init_matrix(self):
        matrix = []
        for i in range(0, 10):
            row = []
            for j in range(0,10):
                row.append(MatrixBlock())
            matrix.append(row)
        return matrix

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
            for block in x:
                output = output + "[" + str(block) + "]"
            output = output + "\n------------------------------\n"
        return output


class AI(Player):

    def __init__(self):

        # PLACE SHIPS
        self.__place()

    def __place(self):

        while len(self.__ships) != 0:
            x = random.randint(0, 10) # Convert to number
            y = random.randint(0, 10)
            coordinate = x + y # change
            ship_name = self.__ships.get_random()
            orientation = None
            if random.randint(0,1) == 0:
                orientation = "Vertical"
            else:
                orientation = "Horizontal"

            try:
                self.place_ship(ship_name, coordinate, orientation)
            except:
                print("TODO")
                # Try again

    # MAIN
    if __name__ == "__main__":
        player1 = Player()
        print(str(player1))
