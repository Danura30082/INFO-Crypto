# Description: Common functions for the Code breaking project
import numpy as np


def save(message, File_name=None):
    """
    Saves the given message to a file.

    Parameters:
    - message (str): The message to be saved.
    - File_name (str, optional): The name of the file to save the message to. If not provided, the user will be prompted to enter a file number and the message will be saved to a file named 'decoded_message_{number}.txt' in the './Message/decoded_message/' directory. The number may be a string.

    Returns:
    None
    """
    if File_name == None:
        if input("Do you want to save the result? (y/n)") == "y":
            print("File number?")
            number = input()
            with open('.\\Message\\decoded_message\\decoded_message_{}.txt'.format(number), 'w', encoding='utf-8' ) as file:
                file.write(message)

            print("File saved")
        else:
            print("File NOT saved")

    else:
        with open('.\\Message\\{}'.format(File_name), 'w', encoding='utf-8') as file:
            file.write(message)
        print("File saved")


def open_file(path):
    """
    Opens a file and returns its content as a string.

    Parameters:
    path (str): The path to the file.

    Returns:
    str: The content of the file as a string.
    """
    with open(path, 'r', encoding='utf-8') as file:
        np.array(file)
        message = file.read()  # read the file
    return message


def frequency_analysis(message):
    """
    Performs frequency analysis on a given message to determine the key used in a Caesar cipher.

    Args:
        message (str): The message to analyze.

    Returns:
        int: The key used in the Caesar cipher.

    Raises:
        ValueError: If the message is not encoded with a Caesar algorithm or the most common characters are not space or 'e' in that order.
    """

    char_count = {}
    for letter in message:
        if letter in char_count:
            char_count[letter] += 1
        else:
            char_count[letter] = 1
    sorted_items = sorted(char_count.items(),
                          key=lambda item: item[1], reverse=True)
    first_common_char = sorted_items[0][0]
    secound_common_char = sorted_items[1][0]
    
    # check if the most common character is space and the secound most common is an 'e'
    if ord(" ") - ord(first_common_char) == ord("e") - ord(secound_common_char):
        key = ord(" ") - ord(first_common_char)
        return key
    
    else:
        print(ord(" ") - ord(first_common_char),
              ord("e") - ord(secound_common_char))
        raise ValueError(
            "The message is probably not encoded with a Cesar algorithm/n the most common characters are not space or an 'e' in that order")


def frequency_analysis_no_safety(message):
    """
    Performs frequency analysis on a given message to determine the key used in a Caesar cipher.

    Args:
        message (str): The message to analyze.

    Returns:
        int: The key used in the Caesar cipher.

    Raises:
        ValueError: If the message is not encoded with a Caesar algorithm or the most common characters are not space or 'e' in that order.
    """

    char_count = {}
    for letter in message:
        if letter in char_count:
            char_count[letter] += 1
        else:
            char_count[letter] = 1
    sorted_items = sorted(char_count.items(),
                          key=lambda item: item[1], reverse=True)
    first_common_char = sorted_items[0][0]
    secound_common_char = sorted_items[1][0]
    
    # check if the most common character is space and the secound most common is an 'e'
    key = ord(" ") - ord(first_common_char)
    return key
