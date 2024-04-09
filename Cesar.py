# Description: This file contains the functions to decode a message encoded with a Cesar algorithm with an unknown key
import matplotlib.pyplot as plt
from common import open_file, save, frequency_analysis
import logging


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
    logging.basicConfig(level=logging.INFO, format='%(levelname)s-%(asctime)s : %(message)s', datefmt='%H:%M:%S')
    # decode the messages and save them
    
    path=r'.\Messages\Encoded_messages\message_2.txt'
    message = open_file(path)
    decoded_message,key = Cesar(message)
    logging.info(f"{decoded_message[:100]} \n[...]\n {decoded_message[-100:]} \n")
    logging.info(f"Key= {key}")
    save(decoded_message)
    
    path=r'.\Messages\Encoded_messages\message_3.txt'
    message = open_file(path)
    decoded_message,key = Cesar(message)
    logging.info(f"{decoded_message[:100]} \n[...]\n {decoded_message[-100:]} \n")
    logging.info(f"Key= {key}")
    save(decoded_message)
    