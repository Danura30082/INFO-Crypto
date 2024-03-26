# Description: This file contains the functions to decode a message encoded with a Scytale algorithm with an unknown key
import matplotlib.pyplot as plt
from common import open_file, save
import logging
common_word_list = ["le", "de", "un", "être", "et", "à", "il", "avoir", "ne", "je", "son", "que", "se", "qui", "ce", "dans", "en", "du", "elle", "au", "bonjour","Joël","--"]

def find_most_likely(possible_width):
    """
    Finds the most likely key from a list of possible keys.

    Args:
        possible_width (list): A list of tuples containing possible widths and their corresponding scores.

    Returns:
        int: The most likely width.
    """
    most_likely = max(possible_width, key=lambda x: x[1])[0]
    return most_likely

def number_of_words(message):
    """
    Counts the number of common words in a given message.

    Parameters:
    message (str): The input message to count the words from.

    Returns:
    int: The number of common words in the message.
    """
    word_count = 0
    List_Word = message.split()
    for word in List_Word:
        if word in common_word_list:
            word_count += 1
    return word_count

def brutforce_Scytale(message, max_key):
    """
    Brute force method to decrypt a Scytale cipher. It tests all possible key sizes and returns a list of possible keys and their corresponding word count.

    Args:
        message (str): The encrypted message.
        max_key (int, optional): The maximum key size to test.

    Returns:
        list: A list of tuples containing possible keys and the corresponding word count.
    """
    current_key = 1
    possible_key = []
    
    if max_key > len(message):  # if the maximum width is greater than the length of the message, reduce it
        max_key = len(message)

    for current_key in range(max_key):  # test all possible widths
        word_count = 0
        
        newmessage = decode_Scytale(message, current_key)
        word_count = number_of_words(newmessage)
        
        if word_count != 0:
            possible_key.append((current_key, word_count))
            logging.debug("Key= " +str(current_key)+ " Word count= "+ str(word_count))

    return possible_key



def decode_Scytale(message, key):
    """
    Decode a message encrypted using the Scytale cipher.

    Args:
        message (str): The encrypted message.
        key (int): The key used for encryption.

    Returns:
        str: The decoded message.
    """
    newmessage = ""
    
    for loop in range(key):
        newmessage += message[loop::key]
    return newmessage

def Scytale(message, max_key=500):
    """
    Decode a message encrypted using the Scytale cipher with an unknown key.

    Args:
        message (str): The message to be decoded.
        key (int, optional): The key used for the Scytale cipher. Defaults to 500.

    Returns:
        tuple: A tuple containing the decoded message and the key used for decoding.

    Raises:
        ValueError: If no word is found in the all possible decoded message. Try increasing the max_key, changing the algorithm, or increasing the size of the dictionary.
    """
    possible_key = brutforce_Scytale(message, max_key)
    
    if possible_key: #check if possible_key is not empty
        most_likely = find_most_likely(possible_key)
        return decode_Scytale(message, most_likely), most_likely
    else:
        raise ValueError("No word found in all possible decoded message. Try to increase max_key, changing algorithm, or increasing the size of the dictionary")
    
if __name__ == "__main__":
    
    # decode the message and save it
    logging.basicConfig(level=logging.INFO, format='%(levelname)s-%(asctime)s : %(message)s', datefmt='%H:%M:%S')
    path=r'.\Messages\Encoded_messages\message_1.txt'
    message = open_file(path)
    decoded_message, key = Scytale(message)
    logging.info(f"{decoded_message[:100]} \n\n {decoded_message[-100:]} \n")
    logging.info(f"Key= {key}")
    save (decoded_message)
    
    
    
# def plot(possible_key):
#     """
#     Plot the possible key values. It is non-blocking, so the program will continue to run after the plot is shown.

#     Parameters:
#     possible_key (list): A list of tuples containing the key and count values.

#     Returns:
#     None
#     """
#     for key, count in possible_key:
#         plt.plot(key, count, 'r.')
#     plt.show(block=False)