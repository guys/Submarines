"""
    Name: online_game_handler.py

    Description: This file contains the class of the online game handler - it sends the user guesses and receives the
                 rival's guesses - handles the game from the board input until the end.

    Usage: from online_game_handler import OnlineGameHandler

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Created
"""


class OnlineGameHandler:
    """
    a class that its instances control the game in the client side - runs the game as rounds from the first round until
    someone wins.
    """

    def __init__(self, i_start, game_socket, board_manager, io_manager):
        """
        a C'tor for the OnlineGameHandler.
        :param bool i_start: True if we start the game, False otherwise.
        :param socket.socket game_socket: the socket on which the game runs.
        :param BoardManager board_manager: the board manager for this client's game.
        :return: a new OnlineGameHandler is created.
        """
        self.my_turn = i_start
        self.game_socket = game_socket
        self.board_manager = board_manager
        self.io_manager = io_manager

    def _change_turn(self):
        """
        this function is used to change the turn ownership.
        :return: changes my_turn from True to False and vice-versa.
        """
        self.my_turn ^= 1

    def run_turn(self):
        """
        this function is used to run a single turn according to whose turn it is.
        :return: True if the game continues, False if it ends.
        """
        if self.my_turn:
            return self.run_my_turn()
        return self.run_rival_turn()

    def run_my_turn(self):
        """
        this function runs the turn of this user.
        :return: True if the game continues, False if it ends.
        """
        pass

    def run_rival_turn(self):
        """
        this function runs the turn when this is the rivals turn.
        :return: True if the game continues, False if it ends.
        """
        pass
