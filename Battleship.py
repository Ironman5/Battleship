"""
COMP.CS.100 Programming 1
Assignment: Laivanupotus
Tekijä: Mika Valtonen
Opiskelijanumero: 166364

This program implement a single player version of the Battleship game in which
the player tries to sink the computer's fleet.
"""

FILE_ERROR_MESSAGE = "File can not be read!"
COORDINATE_ERROR_MESSAGE = "Error in ship coordinates!"
OVERLAPPING_ERROR_MESSAGE = "There are overlapping ships in the input file!"
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


class Ship:
    """
    This class models a ship in battleship game.
    """

    def __init__(self, name):
        """
        A ship object is initialized with the name and its location.
        Default settings are:
        __type = first letter of names
        __hit_coordinates = empty list
        __status = True (the ship is not sunk)

        :param name: list, name of the ship and its coordinates
        """
        self.__name = name[0]
        self._coordinates = name[1:]
        self.__type = name[0][0].upper()
        self.__hit_coordinates = []
        self.__status = True

    def check_hit(self, shot_coordinates, matrix):
        """
        Check to see if the shot is a hit

        :param shot_coordinates: list, [x-coordinate, y-coordinate]
        :param matrix: matrix, [10][10]-game board
        """

        # Add hits to hit_coordinates
        if shot_coordinates in self._coordinates:
            self.__hit_coordinates.append(shot_coordinates)
            # add to hits to the matrix
            matrix[shot_coordinates[0]][shot_coordinates[1]] = "X"
            # Check if the ship is sank
            self.check_sank(matrix)

    def check_sank(self, matrix):
        """
        Check if the ship is sank

        :param matrix: matrix, [10][10] -game board
        """
        # Change the marks on the board if all points on the ship have been hit
        if len(self._coordinates) == len(self.__hit_coordinates):
            for coordinate in self.__hit_coordinates:
                matrix[coordinate[0]][coordinate[1]] = self.__type
            # Change ship status to sank
            self.__status = False
            print(f"You sank a {self.__name}!")

    def get_status(self):
        """
        Show ship status; on the surface or sunken

        :return: boolean; True = on the surface, False = sunken
        """
        return self.__status


def load_ships(file_name):
    """Tries to load the list of ships from a text file. It is assumed
    that each line of the file has one entry and that the line consists of
    the name and the locations of ship separated with a comma.

    :param file_name: str, the name of the file containing the entries.
    :return: list, the list containing the entries, if the the file can
    be opened and the entries read from the file. The return value is None,
    if an exception is raised.
    """

    try:
        # Try to open the file for the reading of the entries.
        reader = open(file_name, mode="r")

        # Initialize the a list for ships and reserved_coordinates.
        ships = []
        reserved_coordinates = []

        # Populate the list, until the file has been processed.
        for line in reader:
            # Remove the character(s) that end and split the line
            line = line.rstrip().split(";")
            # Ship data
            new_ship = [line[0]]
            for coordinate in line[1:]:
                # Check the validity of the coordinates
                if coordinate[0].upper() not in LETTERS or \
                        coordinate[1:] not in NUMBERS:
                    raise IndexError(COORDINATE_ERROR_MESSAGE)
                # Check the overlap of the coordinates
                if coordinate in reserved_coordinates:
                    raise IndexError(OVERLAPPING_ERROR_MESSAGE)
                else:
                    reserved_coordinates.append(coordinate)
                # Add new ship to the list
                new_ship.append([NUMBERS.index(coordinate[1]),
                                 LETTERS.index(coordinate[0].upper())])

            # Create a new object and add it to the list.
            ships.append(Ship(new_ship))

        # Close the file.
        reader.close()

    except OSError:
        print(FILE_ERROR_MESSAGE)
        ships = None

    except IndexError as error_msg:
        print(error_msg)
        ships = None

    # Return the entries or the error code.
    return ships


def print_board(matrix):
    """
    Print game board

    :param matrix: matrix, [10][10]-game board
    """
    # Print the letters
    print("\n ", *LETTERS)

    # Print the matrix with indexes
    for index, row in enumerate(matrix):
        print(index, " ".join(matrix[index]), index)

    # Print the letters
    print(" ", *LETTERS)


def play_game(ships, matrix):
    """
    Play game

    :param ships: list, name of the ship and its coordinates
    :param matrix: matrix, [10][10]-game board
    :return: None, end of the game
    """

    AMOUNT_OF_SHIPS = len(ships)
    SANKED_SHIPS = 0

    # Print game board
    print_board(matrix)

    while True:

        shot = input("\nEnter place to shoot (q to quit): ")

        # End the game
        if shot == "q" or shot == "Q":

            print("Aborting game!")
            return

        # Check valid input
        if not shot or \
                shot[0].upper() not in LETTERS or \
                shot[1:] not in NUMBERS:
            print("Invalid command!")
            print_board(matrix)
            continue

        # Find out shot coordinates
        x_coordinate = NUMBERS.index(shot[1])
        y_coordinate = LETTERS.index(shot[0].upper())

        # Mark shot in matrix with *
        if matrix[x_coordinate][y_coordinate] != " ":
            print("Location has already been shot at!")
            print_board(matrix)
            continue
        else:
            matrix[x_coordinate][y_coordinate] = "*"

        # Check the game situation
        for ship in ships:
            # Check if the shot is a hit
            ship.check_hit([x_coordinate, y_coordinate], matrix)
            # Check sunken ships
            if not ship.get_status():
                SANKED_SHIPS += 1

        print_board(matrix)

        # End the game if all ships are sunk
        if AMOUNT_OF_SHIPS == SANKED_SHIPS:
            print("\nCongratulations! You sank all enemy ships.")
            return
        else:
            SANKED_SHIPS = 0


def main():

    # Load ships data
    ships = load_ships(input("Enter file name: "))

    # End the game with invalid data
    if ships is None:
        return

    # Initialize the battle board.
    matrix = [[" " for i in range(10)] for j in range(10)]

    # Play game
    play_game(ships, matrix)


if __name__ == "__main__":
    main()
