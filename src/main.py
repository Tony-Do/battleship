###########
# IMPORTS #
###########
import player as player_module
import cmd

#########
# CLASS #
#########
class Console(cmd.Cmd):

    # ATTRIBUTES
    player = None
    ai = None

    def do_new(self, args):
        """new - Starts a new game and initializes the player and ai"""
        print("...Starting a new game\n")
        self.player = player_module.Player()
        self.ai = player_module.Player()
        self.prompt = str(self.player) + "\n> "

        # Place ships for AI
        # TO BE IMPLEMENTED: self.__place_ai_ships_temp()

    def do_place(self, args):
        """place <ship_name> <coordinate (e.g. "B3")> <orientation (e.g. vertical)> - This places a ship on the field"""
        commands = self.__parse_input(args)         # Parse the arguements in to a list

        # If there are not exactly three arguments provided, show an error
        if len(commands) == 3:

            # Place the ship
            ship_name = commands[0]
            coordinate = commands[1]
            orientation = commands[2]
            try:
                self.player.place_ship(ship_name, coordinate, orientation)
            except Exception as e:
                print(e)
            self.prompt = str(self.player) + "\n> "
        else:
            print("*** invalid number of arguments. See 'help place'")

    def do_attack(self, args):
        """attack <coordinate>\t- This command attacks the corresponding enemy square"""
        commands = self.__parse_input(args)
        if len(commands) == 1:
            try:
                self.player.attack(commands[0])
            except Exception as e:
                print(e)
        else:
            print("*** invalid number of arguments")

    def do_exit(self, args):
        """exit - Exits the program"""
        raise SystemExit

    # PRIVATE METHODS    
    def __parse_input(self, args):
        result = []

        argument = ""
        is_phrase = False

        for x in args:
            if x == "\"" and not is_phrase:
                is_phrase = True
            elif x == "\"" and is_phrase:
                is_phrase = False
                result.append(argument)
                argument = ""
            elif x == " " and not is_phrase and len(argument) != 0:
                result.append(argument)
                argument = ""
            elif x == " " and len(argument) == 0:
                continue
            else:
                argument = argument + x
        if len(args) == 0:
            pass
        elif args[len(args) - 1] != "\"":
            result.append(argument)
        return result

    # TEMPORARY!
    def __place_ai_ships_temp(self):
        self.ai.place_ships("Carrier", "A1", "Vertical")
        self.ai.place_ships("Battleship", "B1", "Vertical")
        self.ai.place_ships("Destroyer", "C1", "Vertical")
        self.ai.place_ships("Submarine", "D1", "Vertical")
        self.ai.place_ships("Patrol Boat", "E1", "Vertical")

    # OVERRIDEN METHODS
    def emptyline(self):
        pass

########
# MAIN #
########
if __name__ == "__main__":

    console = Console()
    console.prompt = "> "
    console.cmdloop("BATTLESHIP")
