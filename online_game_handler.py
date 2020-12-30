"""
    Name: online_game_handler.py

    Description: This file contains the class of the online game handler - it sends the user guesses and receives the
                 rival's guesses - handles the game from the board input until the end.

    Usage: from online_game_handler import OnlineGameHandler

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Created
"""
from Communication.communication_handler import *
from Game.board_manager import INVALID_COORDINATES_RETURN_VALUE, VICTORY_RETURN_VALUE

GUESS_ANSWER_TO_MESSAGE = {
    HIT_CODE: "hit.",
    SINK_CODE: "submarine sank",
    WIN_CODE: "You have won!",
    MISS_CODE: "miss"
}


class OnlineGameHandler:
    """
    a class that its instances control the game in the client side - runs the game as rounds from the first round until
    someone wins.
    """

    def __init__(self, i_start, game_socket, board_manager, io_manager, communication_handler):
        """
        a C'tor for the OnlineGameHandler.
        :param bool i_start: True if we start the game, False otherwise.
        :param socket.socket game_socket: the socket on which the game runs.
        :param BoardManager board_manager: the board manager for this client's game.
        :param IOHandler io_manager: the io manager used.
        :param CommunicationHandler communication_handler: the communication handler used.
        :return: a new OnlineGameHandler is created.
        """
        self.my_turn = i_start
        self.game_socket = game_socket
        self.board_manager = board_manager
        self.io_manager = io_manager
        self.comm_handler = communication_handler

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
        rival_answer = HIT_CODE
        while rival_answer != MISS_CODE:
            attack_position = self.io_manager.ask_user_for_attack_input()
            self.comm_handler.send_message(GUESS_CODE, [*attack_position])
            rival_answer_code, extra_arguments = self.comm_handler.recv_message()
            if rival_answer_code == GUESS_ANSWER_CODE:
                rival_answer = extra_arguments[0]
                print(GUESS_ANSWER_TO_MESSAGE[rival_answer])
                if rival_answer == WIN_CODE:
                    self.finish_game()
                    return False
            elif rival_answer_code == ERROR_CODE and extra_arguments[0] == INVALID_COORDINATES_ERROR_CODE:
                print("Invalid coordinates supplied. try again.")

        self._change_turn()
        return True

    def run_rival_turn(self):
        """
        this function runs the turn when this is the rivals turn.
        :return: True if the game continues, False if it ends.
        """
        my_answer = HIT_CODE
        while my_answer != MISS_CODE:
            rival_message_code, extra_arguments = self.comm_handler.recv_message()
            if rival_message_code == GUESS_CODE:
                attack_x, attack_y = extra_arguments[0], extra_arguments[1]
                my_answer = self.board_manager.answer_attack_attempt(attack_x, attack_y)
                if my_answer == INVALID_COORDINATES_RETURN_VALUE:
                    self.comm_handler.send_message(ERROR_CODE, [INVALID_COORDINATES_ERROR_CODE])
                else:
                    if my_answer == VICTORY_RETURN_VALUE:
                        print("You have lost.")
                        self.finish_game()
                        return False
                    print(GUESS_ANSWER_TO_MESSAGE[my_answer])
                    self.comm_handler.send_message(GUESS_ANSWER_CODE, [my_answer])

        self._change_turn()
        return True

    def finish_game(self):
        """
        this function is used to clean all of the resources and exit the game.
        """
        self.comm_handler.close_communication()
