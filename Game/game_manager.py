"""
    Name: game_manager.py

    Description: This file has a class of game manager - it contains the main control of the game - a board with
                 submarines on it that returns an answer of an attack attempt.

    Usage: from Game.game_manager import GameManager

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Created
"""

TUPLE_STATUS_CODE_POSITION = 0
TUPLE_SUBMARINE_POSITION = 1

NOT_HIT_STATUS_CODE = 0
WAS_HIT_STATUS_CODE = 1

MISS_RETURN_VALUE = 0
HIT_RETURN_VALUE = 1
SINK_RETURN_VALUE = 2


class GameManager:
    """
    a class for managing the game - contains the board of the game and returns answers to attack attempts
    """

    def __init__(self, game_board):
        """
        a C'tor for the game manager - sets the game board to be in the given state.
        :param list(list(tuple)) game_board: the game board which is a list of list of tuples that contain a status
                                             code for the cell(was hit or not) and the submarine in it(None if there is
                                             no submarine in it.
        :return: a new GameManager instance is created.
        """
        self.game_board = game_board

    def answer_attack_attempt(self, attack_x, attack_y):
        """
        a function that gets the rival's attack coordinates - applies the hit logic and returns a status code for the
        attack(MISS/HIT/SINK)
        :param int attack_x: the x position of the attack on the board.
        :param int attack_y: the y position of the attack on the board.
        :return: SINK if the submarine is now sinking, HIT if the submarine was hit but is not sinking and miss if
                 there was no submarine in the given location.
        """
        cell_attacked = self.game_board[attack_y][attack_x]
        attacked_submarine = cell_attacked[TUPLE_SUBMARINE_POSITION]

        if cell_attacked[TUPLE_STATUS_CODE_POSITION] == NOT_HIT_STATUS_CODE and attacked_submarine:
            attacked_submarine.take_hit()
            if attacked_submarine.is_sinking():
                return SINK_RETURN_VALUE
            return HIT_RETURN_VALUE
        return MISS_RETURN_VALUE
