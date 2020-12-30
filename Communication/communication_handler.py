"""
    Name: communication_handler.py

    Description: This file has the class of the communication handler that works according to protocol.

    Usage: from Communication.communication_handler import CommunicationHandler

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Created
"""
import socket
COMMUNICATION_PORT = 1234
FIELD_SIZE = 1


OFFER_CODE = 100
OFFER_ACCEPTED_CODE = 101
OFFER_DECLINED_CODE = 102
READY_CODE = 103
GUESS_CODE = 110
GUESS_ANSWER_CODE = 111
CONNECTION_CLOSED_CODE = 50
ERROR_CODE = 99

CODES_TO_NUMBER_OF_ARGUMENTS = {
    OFFER_CODE: 1,
    OFFER_ACCEPTED_CODE: 0,
    OFFER_DECLINED_CODE: 0,
    READY_CODE: 0,
    GUESS_CODE: 2,
    GUESS_ANSWER_CODE: 1,
    CONNECTION_CLOSED_CODE: 0,
    ERROR_CODE: 1
}

GUEST_STARTS_CODE = 0
HOST_STARTS_CODE = 1

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
        :param socket.socket comm_socket: the socket that will be used to communicate.
        :return: a new CommunicationHandler is created.
        """
        self.comm_socket = comm_socket
        self.game_socket = None

    def wait_for_player(self, wanted_ip):
        """
        this function is used when we are the host of the game. it waits for a specific ip to connect, initializes the
        communication and returns a code that represent the starting player
        :param str wanted_ip: the ip that we want to join us on a game
        :return: a code that represent the starting player.
        """
        connected_address = ""
        self.comm_socket.listen()
        while connected_address != wanted_ip:
            self.game_socket, (connected_address, _) = self.comm_socket.accept()
        return self._init_game_as_host()

    def _init_game_as_host(self):
        """
        a function to start the game as a host - needs to get the offer message from the other player and send response.
        :return: a code that represent the starting player.
        """
        message_code, arguments = self.recv_message()
        while message_code != OFFER_CODE or (arguments[0] != HOST_STARTS_CODE and arguments[0] != GUEST_STARTS_CODE):
            if message_code == OFFER_CODE:
                self.send_message(ERROR_CODE, [INVALID_OFFER_ERROR_CODE])
            else:
                self.send_message(ERROR_CODE, [INVALID_TYPE_ERROR_CODE])
            message_code, arguments = self.recv_message()

        self.send_message(OFFER_ACCEPTED_CODE, [])
        return arguments[0]

    def init_game_as_guest(self, ip_address, host_starts):
        """
        This function initializes the game as a guest - connects to a given ip and tries to initialize the game.
        :param str ip_address: the ip address of the host we want to connect to.
        :param bool host_starts: True if the user wants to start, False otherwise.
        :return: True if the game was initialized correctly, False otherwise.
        """
        self.game_socket = self.comm_socket
        self.game_socket.connect((ip_address, COMMUNICATION_PORT))
        self.send_message(OFFER_CODE, [host_starts])
        message_code, arguments = self.recv_message()
        while message_code != OFFER_ACCEPTED_CODE and message_code != OFFER_DECLINED_CODE:
            self.send_message(ERROR_CODE, [INVALID_TYPE_ERROR_CODE])
            message_code, arguments = self.recv_message()

        if message_code == OFFER_ACCEPTED_CODE:
            return True
        return False

    def recv_message(self):
        """
        a function to receive a message from the other player.
        :return: a tuple of the message number and the list of the extra arguments
        """
        extra_arguments = []
        try:
            message_code = list(self.game_socket.recv(FIELD_SIZE))[0]  # done in order to convert from bytes to a number
        except (socket.error, socket.timeout) as socket_exception:
            return CONNECTION_CLOSED_CODE, []
        for _ in range(CODES_TO_NUMBER_OF_ARGUMENTS[message_code]):
            try:
                extra_arguments.append(list(self.game_socket.recv(FIELD_SIZE))[0])
            except (socket.error, socket.timeout) as socket_exception:
                return CONNECTION_CLOSED_CODE, []

        return message_code, extra_arguments

    def send_message(self, message_code, extra_arguments):
        """
        a function to send a message on the socket.
        :param int message_code: the decimal code of the message
        :param list extra_arguments: the extra arguments given in this message.
        :return: True if the sending was successful, False otherwise.
        """
        message_to_send = bytes([message_code] + extra_arguments)
        try:
            self.game_socket.send(message_to_send)
        except (socket.error, socket.timeout) as socket_exception:
            return False
        return True

    def send_wait_ready(self):
        """
        a function used when the user is ready, sends a ready message to the rival and waits for his response.
        """
        self.send_message(READY_CODE, [])
        message_code, arguments = self.recv_message()
        while message_code != READY_CODE:
            self.send_message(ERROR_CODE, [INVALID_TYPE_ERROR_CODE])
            message_code, arguments = self.recv_message()

    def close_communication(self):
        """
        a function used to close the sockets for the cleanup of resources.
        """
        self.game_socket.close()
        if self.comm_socket != self.game_socket:
            self.comm_socket.close()

