"""
    Name: submarines.py

    Description: This program initializes everything for the submarine game and starts it according to the user wishes.

    Usage: python submarines.py [ip_address]

    Author: Guy Sugbeker

    Change Log:
    30/12/2020 - Created
"""
import sys
USAGE_MESSAGE = "Incorrect Usage.\nThe correct usage is:\npython submarines.py [ip address of the other player]"
ERROR_RETURN_CODE = -1
OK_RETURN_CODE = 0
LOCAL_ADDRESS = "0.0.0.0"


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


def main():
    if not are_arguments_valid(sys.argv):
        print(USAGE_MESSAGE)
        return ERROR_RETURN_CODE
    return OK_RETURN_CODE


if __name__ == '__main__':
    main()
