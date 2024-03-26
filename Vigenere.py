# Description: This file contains the functions to decode a message encoded with a Vignere algorithm with a different unknown key for even and odd letters
import matplotlib.pyplot as plt
from common import open_file, save, frequency_analysis
import logging

def find_Vigenere_key_length(message, distance, max_key_length=100,):
    """
    Finds the most likely key length for a Vigenere cipher given a message. The algorithm tries shifting the message by different key lengths and counts the number of repetitions. The most likely key length is the greatest common divisor of the number of repetitions for each shift. 

    If no key length is found, the algorithm tries again with a greater distance between peaks in the key length distribution. If no key length is found after multiple attempts, a ValueError is raised.

    Args:
        message (str): The message to analyze.
        max_key_length (int, optional): The maximum key length to consider. Defaults to 100.
        distance (int, optional): The distance between peaks in the key length distribution.
        max_fail_count (int, optional): The maximum number of times the algorithm can fail to find a key length before raising a ValueError.

    Returns:
        int: The most likely key length for the Vigenere cipher.

    Raises:
        ValueError: If no key length is found after multiple attempts.
    """
    def gcd(a, b):
        """
        Calculate the greatest common divisor (GCD) of two numbers.

        Parameters:
        a (int): The first number.
        b (int): The second number.

        Returns:
        int: The GCD of the two numbers.
        """
        while b != 0:
            a, b = b, a % b
        return a

    def find_peaks(data, distance):
        """
        Find peaks in the given data within a specified distance.

        Args:
            data (list): The data to search for peaks in.
            distance (int): The distance between a peak and its neighboring points for which the peak is the greatest.

        Returns:
            list: A list of indices where peaks are found.

        Raises:
            ValueError: If no peak is found in the data.
        """
        peaks = []  # list of indices where peaks are found
        for i in range(len(data)):
            # check if the current point is greater than all points within the specified distance
            if all(data[i] > data[i+k] for k in range(-distance, distance+1) if i+k < len(data) and k != 0 and i+k >= 0):
                peaks.append(i)
                
        if len(peaks) == 0:
            raise ValueError("No peak found in the data")
        return peaks

    possible_key_length = []

    # count the number of repetitions for each key length
    for key in range(1, max_key_length):
        repetition = 0
        for letter_index in range(len(message)):
            if message[letter_index] == message[letter_index - key]:
                repetition += 1
        possible_key_length.append(repetition)
        
    
        
    
    peaks = find_peaks(possible_key_length, distance)
    logging.debug(peaks)

    # find the greatest common divisor of the number of repetitions for each key length. We add 1 to each peak because index 0 corresponds to a key length of 1.
    gcd_value = peaks[0]+1
    for peak in peaks[1:]:
        gcd_value = gcd(gcd_value, peak+1)

    # if no key length is found, try again with a greater distance between peaks.
    if gcd_value == 1:
        raise ValueError(
            "No key length found \n reassess if the message is long enough or try to increase max_key_length/distance \n check if the message is encoded with a Vigenere algorithm")

    logging.info(f"Most likely key length : {gcd_value}")
    if logging.getLogger().getEffectiveLevel()==10:
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        logging.getLogger('PIL').setLevel(logging.WARNING)
        plt.figure()
        plt.plot(possible_key_length)
        plt.show()
    return gcd_value


def Vigenere(message, max_key_length=100, distance=1):
    """
    Decode a message encoded with a Vigenere algorithm with an unknown key (value and length).

    Args:
        message (str): The message to be encoded.
        max_key_length (int, optional): The maximum length of the Vigenere key. Defaults to 100.
        distance (int, optional): The distance between peaks in the key length distribution. Defaults to 1.
        max_fail_count (int, optional): The maximum number of times the algorithm can fail to find a key length before raising a ValueError. Defaults to 5.

    Returns:
        tuple: A tuple containing the decoded message and the Vigenere key used.
    """
    #TODO: fix this. Fuck spaghetti code. Also Fuck recursion. Fun fact NASA banned recursion in there codes because it was too error prone and too difficult for a human to follow/understand.
    if distance <= max_key_length: # a bit of a hack to avoid infinite recursion
        try:
            key_length = find_Vigenere_key_length(message, distance, max_key_length)
            separated_message,key = [],[]  # list of messages separated by key length

            # separate the message into as many messages as the key length. Each message is now encoded with a Caesar cipher with a different key. We can use frequency analysis to find the key for each message.
            for i in range(key_length):
                separated_message.append(message[i::key_length])
                key.append(frequency_analysis(separated_message[i]))
                
        except ValueError:
            # if no key is found, try again with a greater distance between peaks.
            logging.debug(f"No key length found with distance = {distance}")
            return Vigenere(message, max_key_length, distance*2)
    else:
        try:
            #desperate attempt to find the key. this just considers the most common letter is space and DOESN'T  check if the second most common letter is e
            logging.warning("Unable to find a key length with the given distance. Trying without checking if e and space are the most common letters.")
            key_length=find_Vigenere_key_length(message, max_key_length, max_key_length)
            separated_message,key = [],[]
            for i in range(key_length):
                separated_message.append(message[i::key_length])
                key.append(frequency_analysis(separated_message[i],False))
        except:
            raise ValueError("No key length found \n reassess if the message is long enough or try to increase max_key_length/distance \n check if the message is encoded with a Vigenere algorithm")

    
        

    return decode(message, key), key


def decode(message, key):
    """
    Decodes a message using the Vigenere cipher.

    Args:
        message (str): The message to be decoded.
        key (list): The key used for decoding.

    Returns:
        str: The decoded message.
    """
    newmessage = ""
    for letter_index in range(len(message)):
        newmessage += chr(ord(message[letter_index]) + key[letter_index % len(key)])
    return newmessage




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s-%(asctime)s : %(message)s', datefmt='%H:%M:%S')
    
    what_to_decode =[False,False,False,True]
    if what_to_decode[0]:
        path=r'.\Messages\Encoded_messages\message_4.txt'
        message = open_file(path)
        decoded_message, key = Vigenere(message)
        logging.info(f"{decoded_message[:100]} \n\n {decoded_message[-100:]} \n")
        logging.info(f"Key= {key}")
        save(decoded_message)

    if what_to_decode[1]:
        path=r'.\Messages\Encoded_messages\message_5.txt'
        message = open_file(path)
        decoded_message, key = Vigenere(message)
        logging.info(f"{decoded_message[:100]} \n\n {decoded_message[-100:]} \n")
        logging.info(f"Key= {key}")
        save(decoded_message)
        
    if what_to_decode[2]:
        path=r'.\Messages\Encoded_messages\message_6.txt'
        message = open_file(path)
        decoded_message, key = Vigenere(message)
        logging.info(f"{decoded_message[:100]} \n\n {decoded_message[-100:]} \n")
        logging.info(f"Key= {key}")
        save(decoded_message)
        
    if what_to_decode[3]:
        path=r'.\Messages\Encoded_messages\message_7.txt'
        message = open_file(path)
        decoded_message, key = Vigenere(message)
        logging.info(f"{decoded_message[:100]} \n\n {decoded_message[-100:]} \n")
        logging.info(f"Key= {key}")
        save(decoded_message)

    