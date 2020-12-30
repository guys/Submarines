"""
    Name: board_manager.py

    Description: This file has a class of board manager - it contains the main control of the board - a board with
                 submarines on it that returns an answer of an attack attempt.

    Usage: from Game.board_manager import BoardManager

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
VICTORY_RETURN_VALUE = 3
INVALID_COORDINATES_RETURN_VALUE = 4


class BoardManager:
    """
    a class for managing the board - contains the board of the game and returns answers to attack attempts
    """

    def __init__(self, game_board, number_of_submarines):
        """
        a C'tor for the board manager - sets the game board to be in the given state.
        :param list(list(tuple)) game_board: the game board which is a list of list of tuples that contain a status
                                             code for the cell(was hit or not) and the submarine in it(None if there is
                                             no submarine in it.
        :param int number_of_submarines: the number of submarines on the board.
        :return: a new BoardManager instance is created.
        """
        self.game_board = game_board
        self.number_of_submarines = number_of_submarines

    def answer_attack_attempt(self, attack_x, attack_y):
        """
        a function that gets the rival's attack coordinates - applies the hit logic and returns a status code for the
        attack(MISS/HIT/SINK)
        :param int attack_x: the x position of the attack on the board.
        :param int attack_y: the y position of the attack on the board.
        :return: SINK if the submarine is now sinking, HIT if the submarine was hit but is not sinking and miss if
                 there was no submarine in the given location.
        """
        if attack_x < 0 or attack_x >= len(self.game_board[0]) or attack_y < 0 or attack_y >= len(self.game_board):
            return INVALID_COORDINATES_RETURN_VALUE
        cell_attacked = self.game_board[attack_y][attack_x]
        attacked_submarine = cell_attacked[TUPLE_SUBMARINE_POSITION]

        if cell_attacked[TUPLE_STATUS_CODE_POSITION] == NOT_HIT_STATUS_CODE and attacked_submarine:
            self.game_board[attack_y][attack_x] = (WAS_HIT_STATUS_CODE, attacked_submarine)
            attacked_submarine.take_hit()
            if attacked_submarine.is_sinking():
                self.number_of_submarines -= 1
                if self.number_of_submarines == 0:
                    return VICTORY_RETURN_VALUE
                return SINK_RETURN_VALUE
            return HIT_RETURN_VALUE
        return MISS_RETURN_VALUE
