"""
    Name: user_io.py

    Description: This file contains the class that is responsible for the io of the user - a certain function is called
                 from it when a user input is needed.

    Usage: from Game.user_io import IOHandler

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Created
"""
from Game.submarine import Submarine
DIRECTION_TO_POSITION_CHANGE = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1)
}
DEFAULT_CELL_VALUE = (0, None)


class IOHandler:
    """
    this class holds all of the functions in association with input from the user.
    """

    def get_board(self, board_dimensions, submarine_sizes):
        """
        a function to get the board submarine placements from the user, will ask the user to enter a submarine starting
        position and a direction until all of the submarines are placed according to the rules.
        :param int board_dimensions: the dimensions of the board ( for example 10 means 10 by 10)
        :param list(int) submarine_sizes: the sizes of submarines used in the game.
        :return: a board of board_dimensions by board_dimensions that the submarines are placed on.
        """
        board = []
        for _ in range(board_dimensions):
            board.append([DEFAULT_CELL_VALUE] * board_dimensions)

        submarines_locations = []
        for submarine_size in submarine_sizes:
            starting_pos, direction = self._get_submarine_input(submarine_size)
            while not self._is_submarine_input_valid(
                    board_dimensions, submarines_locations, submarine_size, starting_pos, direction):

                print("Invalid input for the submarine, please try again.")
                starting_pos, direction = self._get_submarine_input(submarine_size)

            current_submarine = Submarine(submarine_size)
            for location in self._calculate_submarine_positions_by_start_and_direction(
                    submarine_size, starting_pos, direction):

                submarines_locations.append(location)
                board[location[1]][location[0]] = (0, current_submarine)

        return board

    def _get_submarine_input(self, submarine_size):
        """
        a function to get a single submarine input from the user.(starting position and direction)
        :param int submarine_size: the size of the current submarine - will be used when prompting the message to the
                                   user.
        :return: the input of the user - the starting position as a tuple of tuple of x and y and the direction.
        """
        print(f"Please enter the starting position and the direction of the submarine of size {submarine_size}")
        x_position = self._get_number_input("Please enter the x starting position of the submarine:\n")
        y_position = self._get_number_input("Please enter the y starting position of the submarine:\n")
        direction = input("Please enter the direction of the submarine (left, right, up or down):\n")
        while direction not in DIRECTION_TO_POSITION_CHANGE.keys():
            direction = input("Please enter the direction of the submarine (left, right, up or down):\n")
        return (x_position, y_position), direction

    def _get_number_input(self, prompt_message):
        """
        a function to get an input as a number - will try to get the input until it is numeric.
        :param str prompt_message: the message that we want to prompt to the user.
        :return: the numeric input as int.
        """
        input_number = ""
        while not input_number.isnumeric():
            print("The following input must be numeric!")
            input_number = input(prompt_message)
        return int(input_number)

    def _is_submarine_input_valid(self, dimensions, submarines_positions, submarine_size, starting_position, direction):
        """
        a function to check io
        :param int dimensions: the dimensions of the board
        :param list(tuple) submarines_positions: the positions currently occupied by submarines.
        :param int submarine_size: the size of the submarine we want to place.
        :param tuple starting_position: the x and y representing the wanted starting position of the submarine.
        :param str direction: the direction of the submarine(up/down/right/left)
        :return: True if the submarine input is valid, False otherwise.
        """
        current_submarine_positions = self._calculate_submarine_positions_by_start_and_direction(
            submarine_size, starting_position, direction)
        for position in current_submarine_positions:
            if position[0] < 0 or position[0] >= dimensions or position[1] < 0 or position[1] >= dimensions:
                return False
            if self._are_there_submarines_around(submarines_positions, position):
                return False
        return True

    def _are_there_submarines_around(self, submarines_locations, position):
        """
        a function to check if there are submarines around a given position
        :param list(tuple) submarines_locations: the locations of the submarines on the map.
        :param tuple position: the position in question.
        :return: True if there are submarines around the given position, False otherwise.
        """
        for direction, position_change in DIRECTION_TO_POSITION_CHANGE.items():
            if (position[0] + position_change[0], position[1] + position_change[1]) in submarines_locations:
                return True
        return False

    def _calculate_submarine_positions_by_start_and_direction(self, submarine_size, starting_pos, direction):
        """
        a function to calculate the positions that the submarine will occupy (done in order to check the validity)
        :param int submarine_size: the size of the submarine
        :param tuple starting_pos: the starting x and y of the submarine
        :param str direction: the direction of the submarine
        :return: a list of tuples of the positions that the submarine will occupy.
        """
        current_position = list(starting_pos)
        occupied_positions = [starting_pos]
        for _ in range(submarine_size - 1):
            current_position[0] += DIRECTION_TO_POSITION_CHANGE[direction][0]
            current_position[1] += DIRECTION_TO_POSITION_CHANGE[direction][1]
            occupied_positions.append(tuple(current_position))

        return occupied_positions
