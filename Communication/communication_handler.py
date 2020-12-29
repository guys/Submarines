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


