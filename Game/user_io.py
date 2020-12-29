"""
    Name: user_io.py

    Description: This file contains the class that is responsible for the io of the user - a certain function is called
                 from it when a user input is needed.

    Usage: from Game.user_io import IOHandler

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Created
"""


class IOHandler:
    """
    this class holds all of the functions in association with input from the user.
    """

    @staticmethod
    def get_board(board_dimensions, submarine_sizes):
        """
        a function to get the board submarine placements from the user, will ask the user to enter a submarine starting
        position and a direction until all of the submarines are placed according to the rules.
        :param int board_dimensions: the dimensions of the board ( for example 10 means 10 by 10)
        :param list(int) submarine_sizes: the sizes of submarines used in the game.
        :return: a board of board_dimensions by board_dimensions that the submarines are placed on.
        """
        pass

    @staticmethod
    def is_submarine_input_valid(board, submarine_size, starting_position, direction):
        """
        a function to check io
        :param list(list(tuple)) board: the board we check if the placement is valid on.
        :param int submarine_size: the size of the submarine we want to place.
        :param tuple starting_position: the x and y representing the wanted starting position of the submarine.
        :param int direction: the direction of the submarine(up/down/right/left)
        :return: True if the submarine input is valid, False otherwise.
        """
        pass
