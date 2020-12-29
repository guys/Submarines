"""
    Name: submarine.py

    Description: This file has the implementation of a submarine class that represent a submarine in the game.
                 the submarine has an amount of parts set in the C'tor and each time it gets hit the counter of parts
                 goes down by 1.

    Usage: from Game.submarine import Submarine

    Author: Guy Sugbeker

    Change Log:
    29/12/2020 - Crates
"""


class Submarine:
    """
    this class is a representation of a submarine in the game that has a number of parts and can get hit.
    """

    def __init__(self, number_of_parts):
        """
        C'tor for the Submarine - sets the parts to be the given value
        :param int number_of_parts: the amount of parts the submarine has.
        :return: a new submarine instance is created.
        """
        self.parts = number_of_parts

    def take_hit(self):
        """
        a function called when the submarine gets a hit - the number of parts is reduced by 1.
        """
        self.parts -= 1
