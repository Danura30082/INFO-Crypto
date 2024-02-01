# Description: This file contains the functions to decode a message encoded with a Cesar algorithm with an unknown key
import matplotlib.pyplot as plt
from common import open_file, save, frequency_analysis


def decode(message, key):
    """
    Decodes a message using the Caesar cipher algorithm.

    Args:
        message (str): The message to be decoded.
        key (int): The key used for decoding.

    Returns:
        str: The decoded message.
    """
    newmessage = ""
    for letter in message:
        newmessage += chr(ord(letter) + key)
    return newmessage

def Cesar(message):
    """
    Decodes a message encrypted using the Caesar cipher with an unknown key.

    Parameters:
    message (str): The message to be decrypted.

    Returns:
    tuple: A tuple containing the decoded message and the key used for decoding.
    """
    key = frequency_analysis(message)
    return decode(message, key), key
    
if __name__ == "__main__":
    
    # decode the messages and save them
    
    path=r'.\Message\message2.txt'
    message = open_file(path)
    decoded_message = Cesar(message)
    save(decoded_message)
    
    path=r'.\Message\message3.txt'
    message = open_file(path)
    decoded_message = Cesar(message)
    save(decoded_message)
    