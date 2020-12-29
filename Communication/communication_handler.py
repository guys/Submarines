"""
    Name: communication_handler.py

    Description: This file has the class of the communication handler that works according to protocol.

    Usage: from Communication.communication_handler import CommunicationHandler

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Created
"""
from socket import socket
COMMUNICATION_PORT = 1234
FIELD_SIZE = 1
LOCAL_ADDRESS = "0.0.0.0"

CODES_TO_NUMBER_OF_ARGUMENTS = {
    100: 1,
    101: 0,
    102: 0,
    103: 0,
    110: 2,
    111: 1,
    50: 0,
    99: 1
}

HE_STARTS_CODE = 0
YOU_START_CODE = 1

MISS_CODE = 0
HIT_CODE = 1
SINK_CODE = 2
WIN_CODE = 3

INVALID_TYPE_ERROR_CODE = 0
INVALID_OFFER_ERROR_CODE = 1
INVALID_COORDINATES_ERROR_CODE = 2
INVALID_ANSWER_ERROR_CODE = 3


class CommunicationHandler:
    """
    a class that its instances help to control the communication according to the given protocol.
    """
    def __init__(self, comm_socket):
        """
        a C'tor for the handler - gets the socket on which the data will be transferred.
        :param socket comm_socket: the socket that will be used to communicate.
        :return: a new CommunicationHandler is created.
        """
        self.comm_socket = comm_socket
        self.game_socket = None

    def wait_for_player(self, wanted_ip):
        """
        this function is used when we are the host of the game. it waits for a specific ip to connect, initializes the
        communication and returns a code that represent the starting player
        :param str wanted_ip: the ip that we want to join us on a game
        :return:
        """
        connected_address = ""
        self.comm_socket.listen()
        while connected_address != wanted_ip:
            self.game_socket, (connected_address, _) = self.comm_socket.accept()

    def recv_message(self):
        """
        a function to receive a message from the other player.
        :return: a tuple of the message number and the list of the extra arguments
        """
        extra_arguments = []
        message_code = list(self.game_socket.recv(FIELD_SIZE))[0]  # done in order to convert from bytes to a number
        for _ in range(CODES_TO_NUMBER_OF_ARGUMENTS[message_code]):
            extra_arguments.append(list(self.game_socket.recv(FIELD_SIZE))[0])

        return message_code, extra_arguments


