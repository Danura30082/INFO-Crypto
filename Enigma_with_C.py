from rotor_enigma import rotor, rotor_inverser
from common import open_file, save
import multiprocessing
import logging
import ctypes

# Load the shared library
libc = ctypes.CDLL('./Enigma.so')

# Define the argument types and return type
libc.brute_force_enigma.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int]
libc.brute_force_enigma.restype = None


# Now you can call the function with your parameters
def call_brute_force_enigma(message, rotor_num, position=[0,0,0], attempts=256**3):
    message_c = (ctypes.c_int * len(message))(*message)
    rotor_num_c = (ctypes.POINTER(ctypes.c_int) * len(rotor_num))()
    position_c = (ctypes.POINTER(ctypes.c_int) * len(position))()

    for i in range(len(rotor_num)):
        rotor_num_c[i] = ctypes.pointer(ctypes.c_int(rotor_num[i]))

    for i in range(len(position)):
        position_c[i] = ctypes.pointer(ctypes.c_int(position[i]))

    attempts = ctypes.c_int(attempts)
    libc.brute_force_enigma(message_c, rotor_num_c, position_c, attempts)

    if rotor_num_c[0].contents.value == -1:
        return None

    return [[rotor_num_c[i].contents.value for i in range(3)], [position_c[i].contents.value for i in range(3)]]

def addition_long(number_in_base, number_to_add, base=256):
    """an addition function with different base

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


def decode_enigma(rotor_num, decode_position, message, radius=256):
    """a function to decode a message using the enigma machine

    Parameters
    ----------
    rotor_num : list of int
        the numbers of the rotors to use
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
        char = ord(char)
        for i in range(len(rotor_num)-1, -1, -1):
            rotor_i = rotor_num[i]
            char = (char+decode_position[i]) % radius
            char = (rotor_inverser[rotor_i][char])
            char = (char-decode_position[i]) % radius
        newchar = chr(char)
        newmessage += newchar
        decode_position = addition_long(decode_position, 1)
    return newmessage, decode_position, rotor_num

def Enigma(message):
    """This function tries to decode a message using the Enigma machine

    Parameters
    ----------
    message : str
        the message to decode
    """
    rotor_nums = [[0, 1, 2]]

    # Generate all possible rotor_num permutations
    for _ in range(8*7*6-1):
        # Get the next rotor_num
        rotor_num = addition_long(rotor_nums[-1].copy(), 1, 8)

        # Ensure that the rotor_num does not contain duplicate numbers
        while rotor_num[0] == rotor_num[1] or rotor_num[1] == rotor_num[2] or rotor_num[2] == rotor_num[0]:
            rotor_num = addition_long(rotor_num, 1, 8)

        # Add the rotor_num to the list
        rotor_nums.append(rotor_num)

   
    short_message = message[-4::]
    short_message = [ord(char) for char in short_message]
    results = []
    rotor_nums = [[0, 1, 2], [0, 2, 1], [1, 0, 2],[5,1,7],[1, 2, 0], [2, 0, 1], [2, 1, 0]]
    for rotor_num in rotor_nums:
        results.append(call_brute_force_enigma(short_message, rotor_num))
        
    # results = [None, ('Joël', [5, 1, 7], [64, 109, 126])]
    # Override the results for testing
    post_process_results(results, message)

def post_process_results(results, message):
    """This function processes the results of the Enigma function. When exploring the rotor_num and position, we only decoded the last 4 characters of the message. This function decodes the entire message and saves it to a file.

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
            rotor_num, position = result[0], result[1]

            # Adjust the position based on the length of the decoded message
            # 256**3 is the maximum value for a position, so we can use the complement to make a subtraction
            position = addition_long(
                position, 256**3 - length + 4)

            # Decode the message using the Enigma machine
            decoded_message, position, rotor_num = decode_enigma(
                rotor_num, position, message)

            # Print the last 300 characters of the decoded message and the final rotor_num and position
            logging.info(f"{decoded_message[:100]} \n[...]\n {decoded_message[-100:]} \n")
            logging.info(f"Key= {position} {rotor_num}")

            # Save the decoded message
            save(result[0])






if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format='%(levelname)s-%(asctime)s : %(message)s', datefmt='%H:%M:%S')
    __path__ = r'.\Messages\Encoded_messages\message_8.txt'
    
    message = open_file(__path__)
    Enigma(message)
