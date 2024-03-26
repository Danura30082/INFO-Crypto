from rotor_enigma import rotor, rotor_inverser
from common import open_file, save
import multiprocessing
import logging


def worker(args):
    """This function is used to run the brute_force_enigma function in parallel using the multiprocessing library.

    Parameters
    ----------
    args : list of tuples (str, list)
        a list of the message to decode and the rotor_num to test

    Returns
    -------
    tuple (str, list, list)
        the decoded message, the rotor_num and the position
    """
    message, rotor_num = args
    result = brute_force_enigma(message, rotor_num)
    return result


def multithreaded(message,rotor_nums):
    """Search for the correct rotor_num and position in parallel using the multiprocessing library.

    Parameters
    ----------
    message : str
        the message to decode
    rotor_nums : list
        a list of all rotor combinations to test

    Returns
    -------
    list of tuples (str, list, list)
        the decoded message, the rotor_num and the position
    """
    # Create a list of arguments to pass to the worker function
    args = [(message, rotor_num) for rotor_num in rotor_nums]

    # Create a multiprocessing pool
    with multiprocessing.Pool() as pool:
        # Use map to run the worker function on each rotor_num in parallel
        results = pool.map(worker, args)
    return results


def addition_long(number_in_base, number_to_add, base=256):
    """an addition function with diffrent base

    Parameters
    ----------
    number_in_base : list of int
        a list of ints that represent the number the base
    number_to_add : int
        The number to add in base 10
    base : int, optional
        The base in which the addition is done, by default 256
    """
    def convert_to_base(n, base=256):
        """Converts a number in base 10 to a number in a given base.

        Parameters
        ----------
        n : int
            the number to convert
        base : int, optional
            the base in which to convert n, by default 256

        Returns
        -------
        list of int
            the number n in the given base. Less significant digit first 
        """
        position = []
        d = n
        while d > 0:
            position.append(d % base)
            d = d // base
        return position
    number_to_add_in_base = convert_to_base(number_to_add, base)
    if len(number_to_add_in_base) > len(number_in_base):
        raise ValueError("b is longer than the number_in_base, this is not supported yet.")
    for i in range(len(number_to_add_in_base)):
        number_in_base[i] += number_to_add_in_base[i]
    remainder = 0
    for i in range(len(number_in_base)):
        s = number_in_base[i] + remainder
        number_in_base[i], remainder = s % base, s//base
    return number_in_base


def encode_enigma(rotor_num, encode_position, message, radius=256):
    """a function to encode a message using the enigma machine

    Parameters
    ----------
    rotor_num : list of int
        the numers of the rotors to use
    encode_position : list of int
        the initial position of the rotors
    message : str
        the message to encode
    radius : int, optional
        the radius of the rotors, by default 256

    Returns
    -------
    str
        the encoded message
    """
    newmessage = ""
    for char in message:
        for i in range(len(rotor_num)):
            rotor_i = rotor_num[i]
            char = (char+encode_position[i]) % radius
            char = (rotor[rotor_i][char])
            char = (char-encode_position[i]) % radius
        newmessage += chr(char)
        encode_position = addition_long(encode_position, 1)
    return newmessage


def decode_enigma(rotor_num, decode_position, message, radius=256):
    """a function to decode a message using the enigma machine

    Parameters
    ----------
    rotor_num : list of int
        the numers of the rotors to use
    encode_position : list of int
        the initial position of the rotors
    message : str
        the message to decode
    radius : int, optional
        the radius of the rotors, by default 256

    Returns
    -------
    str
        the decoded message
    """
    newmessage = ""
    for char in message:
        for i in range(len(rotor_num)-1, -1, -1):
            rotor_i = rotor_num[i]
            char = (char+decode_position[i]) % radius
            char = (rotor_inverser[rotor_i][char])
            char = (char-decode_position[i]) % radius
        newchar = chr(char)
        newmessage += newchar
        decode_position = addition_long(decode_position, 1)
    return newmessage, decode_position, rotor_num


def brute_force_enigma(message, rotor_num=[0, 1, 2], position=[0]*3, attempts=(256**3)):
    """This functions tries all possible positions for given rotors to decode the message

    Parameters
    ----------
    message : str
        the message to decode
    rotor_num : list of ints, optional
        the numbers of the rotors that are used, by default [0, 1, 2]
    position : list of ints, optional
        The position at which to start, by default [0]*3
    attempts : tuple, optional
        the number of positions to explore, by default (256**3)

    Returns
    -------
    tuple (str, list, list) or None
        returns the decoded message, the rotor_num and the position if the message contains "Joël", otherwise None
    """
    logging.debug(f"Starting on {rotor_num}")
    for i in range(attempts):
        message_test = decode_enigma(rotor_num, position.copy(), message)[
            0]  # copy to avoid modifying the original list
        if "Joël" in message_test:
            logging.info(
                f"\"Joël\" found in the message with position = {position} and rotor_num = {rotor_num}")
            return message_test, rotor_num.copy(), position.copy()
        position = addition_long(position, 1)
        if position == [0, 0, 0]:
            logging.info(f"{rotor_num} is done")
            return None

    return "No solution found"


def Enigma(message):
    """This function tries to decode a message using the Enigma machine

    Parameters
    ----------
    message : str
        the message to decode
    """
    rotor_nums = [[0, 1, 2]]

    # Generate all possible rotor_num permutations
    for loop in range(8*7*6-1):
        # Get the next rotor_num
        rotor_num = addition_long(rotor_nums[-1].copy(), 1, 8)

        # Ensure that the rotor_num does not contain duplicate numbers
        while rotor_num[0] == rotor_num[1] or rotor_num[1] == rotor_num[2] or rotor_num[2] == rotor_num[0]:
            rotor_num = addition_long(rotor_num, 1, 8)

        # Add the rotor_num to the list
        rotor_nums.append(rotor_num)

    # Override the rotor_nums for testing
    # rotor_nums = [[4, 1, 7], [5, 1, 7], [6, 1, 7],[7 ,6 ,0],[2 ,3 ,7]]
    results = multithreaded(message[-4::], rotor_nums)
    logging.debug(results)
    # results = [None, ('Joël', [5, 1, 7], [64, 109, 126])]
    # Override the results for testing
    post_process_results(results, message)


def post_process_results(results, message):
    """This fucntion processes the results of the Enigma function. When exploring the rotor_num and position, we only decoded the last 4 characters of the message. This function decodes the entire message and saves it to a file.

    Parameters
    ----------
    results : list of tuples (str, list, list)
        the results of exploration of the rotor_num and position. Each tuple contains the decoded message, the rotor_num and the position
    message : str
        the message to decode
    """
    # Process the results
    length = len(message)
    for result in results:
        if result is not None:

        
            # Get the rotor_num and position from the result
            rotor_num, position = result[1], result[2]

            # Adjust the position based on the length of the decoded message
            # 256**3 is the maximum value for a position, so we can use the complement to make a subtraction
            position = addition_long(
                position, 256**3 - length + len(result[0]))

            # Decode the message using the Enigma machine
            decoded_message, position, rotor_num = decode_enigma(
                rotor_num, position, message)

            # Print the last 300 characters of the decoded message and the final rotor_num and position
            logging.info(f"{decoded_message[:100]} \n\n {decoded_message[-100:]} \n")
            logging.info(f"Key= {position} {rotor_num}")

            # Save the decoded message
            save(result[0])


def check_decode():
    """This function checks if the decode_enigma function is working properly
    """
    clear_message = open_file(
        r'.\Messages\Decoded_messages\message_7_enigma.txt')
    from rotor_enigma import message_test

    message_test = check_message_format(message_test)

    # check decode working properly
    assert clear_message == decode_enigma(
        [0, 1, 2], [0, 0, 0], message_test)[0]
    logging.info("decode_enigma working properly")


def check_message_format(message):
    """this function checks if the message is in the correct format. If the message is a string, it converts it to a list of integers

    Parameters
    ----------
    message : str or list of int
        the message to check

    Returns
    -------
    list of int
        the message as a list of integers, ready to decode

    Raises
    ------
    ValueError
        the message is not a string or a list
    ValueError
        the message is a list but not all elements are integers
    """
    if isinstance(message, str):
        message = [ord(i) for i in message]
        return message
    elif isinstance(message, list):
        # check if all elements of the list are integers
        if not (all(isinstance(item, int) for item in message)):
            raise ValueError("not all elements of the list are numbers")
    else:
        raise ValueError("message is neither a string nor a list")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s-%(asctime)s : %(message)s', datefmt='%H:%M:%S')
    check_decode()
    __path__ = r'.\Messages\Encoded_messages\message_8.txt'
    # Open the last 4 char message file
    message = open_file(__path__)
    message = check_message_format(message)
    Enigma(message)
