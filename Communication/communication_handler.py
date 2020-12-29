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

TYPES_TO_CODES = {
    "offer": 100,
    "offer accepted": 101,
    "offer denied": 102,
    "ready": 103,
    "guess": 110,
    "guess_answer": 111,
    "closing connection": 50,
    "error": 99
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


