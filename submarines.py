"""
    Name: submarines.py

    Description: This program initializes everything for the submarine game and starts it according to the user wishes.

    Usage: python submarines.py [ip_address]

    Author: Guy Sugbeker

    Change Log:
    30/12/2020 - Created
"""
import sys
import socket
from Communication.communication_handler import CommunicationHandler, COMMUNICATION_PORT
from Game.board_manager import BoardManager
from Game.user_io import IOHandler
from online_game_handler import OnlineGameHandler


USAGE_MESSAGE = "Incorrect Usage.\nThe correct usage is:\npython submarines.py [ip address of the other player]"
ERROR_RETURN_CODE = -1
OK_RETURN_CODE = 0
LOCAL_ADDRESS = "0.0.0.0"
BOARD_DIMENSIONS = 10
SUBMARINE_SIZES = [2, 3, 3, 4, 5]


def are_arguments_valid(supplied_arguments):
    """
    a function to check the command line arguments given to the program - suppose to be one ip address in the form of
    XXX.XXX.XXX.XXX (each number can be less than 3 characters long)
    :param list supplied_arguments: the command line arguments.
    :return: True if the arguments are valid, False otherwise.
    """
    if len(supplied_arguments) != 2:
        return False
    argument_ip_fields = supplied_arguments[1].split(".")
    if len(argument_ip_fields) != 4 or not "".join(argument_ip_fields).isnumeric():
        return False
    return True


def does_user_wants_to_start():
    """
    a function that checks if the user wants to start the game.
    :return: True if the user wants to start, False otherwise.
    """
    return input("Do you want to be the starting player? (y for yes)") == "y"


def does_user_wants_to_host_the_game():
    """
    a function that checks if the user wants to be the host of the game.
    :return: True if the user wants to be the host, False otherwise.
    """
    return input("Do you want to host the game? (y for yes)") == "y"


def init_communication_handler(wanted_rival_ip):
    """
    a function to start the communication between the user and the rival.
    :param str wanted_rival_ip: the ip of the rival.
    :return: the communication handler and a boolean value stating if the user starts.
    """
    user_socket = socket.socket()
    comm_handler = None
    starting_player = False

    if does_user_wants_to_host_the_game():
        user_socket.bind((LOCAL_ADDRESS, COMMUNICATION_PORT))
        comm_handler = CommunicationHandler(user_socket)
        starting_player = comm_handler.wait_for_player(wanted_rival_ip)
    else:
        starting_player = does_user_wants_to_start()
        comm_handler = CommunicationHandler(user_socket)
        comm_handler.init_game_as_guest(wanted_rival_ip, not starting_player)

    return comm_handler, starting_player


def run_game(comm_handler, is_starting):
    """
    a function to run the game.
    :param CommunicationHandler comm_handler: the communication handler used in this game.
    :param bool is_starting: does our user start.
    """
    io_handler = IOHandler()
    board = io_handler.get_board(BOARD_DIMENSIONS, SUBMARINE_SIZES)
    board_manager = BoardManager(board, len(SUBMARINE_SIZES))
    game_handler = OnlineGameHandler(is_starting, board_manager, io_handler, comm_handler)
    comm_handler.send_wait_ready()
    game_handler.run_game()


def main():
    if not are_arguments_valid(sys.argv):
        print(USAGE_MESSAGE)
        return ERROR_RETURN_CODE
    wanted_rival_ip = sys.argv[1]
    try:
        comm_handler, is_starting = init_communication_handler(wanted_rival_ip)
    except (socket.error, OSError) as connection_error:
        print("There was a connection error.")
        return ERROR_RETURN_CODE

    run_game(comm_handler, is_starting)
    return OK_RETURN_CODE


if __name__ == '__main__':
    main()
