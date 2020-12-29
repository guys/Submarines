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

    def __init__(self, i_start, game_socket):
        """
        a C'tor for the OnlineGameHandler.
        :param bool i_start: True if we start the game, False otherwise.
        :param socket.socket game_socket: the socket on which the game runs.
        :return: a new OnlineGameHandler is created.
        """
        self.my_turn = i_start
        self.game_socket = game_socket
