from rotor_enigma import rotor, rotor_inverser
from common import open_file, save
import multiprocessing

def worker(args):
    message, rotor_num = args
    result=brute_force_enigma(message,rotor_num)
    return result
 
def multithreaded(rotor_nums):
    # Create a list of arguments to pass to the worker function
    args = [(message, rotor_num) for rotor_num in rotor_nums]
    
    # Create a multiprocessing pool
    with multiprocessing.Pool() as pool:
        # Use map to run the worker function on each rotor_num in parallel
        results = pool.map(worker, args)
    return results


def addition(position,b,rayon = 256):
    retenue
    for i in range(len(position)):
        s = position[i] + retenue
        position[i], retenue = s % rayon, s//rayon
    return position
      
        
def increment_position(position, rayon = 256):
    position[0]+=1
    for i in range(len(position)):
        if position[i] == rayon :
            position[i] = 0
            if i != len(position)-1:
                position[i+1] += 1
    return position


def decode_enigma(rotor_num, decode_position, message, rayon = 256):
    newmessage = ""
    for char in message:
        num_char = ord(char)
        for i in range(len(rotor_num)-1,-1,-1):
            rotor_i = rotor_num[i]
            num_char=(num_char+decode_position[i])%rayon
            num_char=(rotor_inverser[rotor_i][num_char])
            num_char=(num_char-decode_position[i])%rayon
        newmessage += chr(num_char)
        decode_position = increment_position(decode_position)
    return newmessage , decode_position, rotor_num

def brute_force_enigma(message,rotor_num = [0, 1, 2],position = [0]*3,attempts = (256**3)*8*7*6):
    print("Starting on",rotor_num)
    for i in range(attempts):
        message_test = decode_enigma(rotor_num, position.copy(), message)[0] #copy to avoid modifying the original list
        if "Joël" in message_test:
            print("\"Joël\" found in the message with position = ",position,"and rotor_num = ",rotor_num)
            return message_test, rotor_num.copy(), position.copy()
        position = increment_position(position)
        if position==[0,0,0]:
            print(rotor_num,"is done")
            return None
            
        
    return "No solution found"

def post_process_results(results):
    # Process the results
    for result in results:
        if result is not None:
            
            # Reopen the message file
            message = open_file(__path__)
            length = len(message)
            
            # Get the rotor_num and position from the result
            rotor_num, position = result[1], result[2]
            
            # Adjust the position based on the length of the decoded message
            position[0] += len(result[0])
            
            # Find the position for the beginning of the message
            for i in range(3):
                position[i] = position[i] - length // (256 ** i) % 256
                if position[i] < 0:
                    if i < 2:
                        position[i] += 256
                        position[i + 1] -= 1
                    else:
                        raise ValueError("position is negative in the last digit")
                    
            
            # Decode the message using the Enigma machine
            result = decode_enigma(rotor_num, position, message)
            
            # Print the last 100 characters of the decoded message and the final rotor_num and position
            print(result[0][-300:], "\n", result[1], "\n", result[2])
            
            # Save the decoded message
            save(result[0])


if __name__ == "__main__":
    __path__ = r'.\\Message\\message8.txt'
    # Open the last 4 char message file
    message = open_file(__path__)[-4::]

    # Initialize the list of rotor numbers
    rotor_nums = [[0, 1, 2]]
    
    # Generate all possible rotor_num permutations
    for loop in range(8*7*6-1):
        # Get the next rotor_num
        rotor_num = increment_position(rotor_nums[-1].copy(), 8)
        
        # Ensure that the rotor_num does not contain duplicate numbers
        while rotor_num[0] == rotor_num[1] or rotor_num[1] == rotor_num[2] or rotor_num[2] == rotor_num[0]:
            rotor_num = increment_position(rotor_num, 8)
        
        # Add the rotor_num to the list
        rotor_nums.append(rotor_num)
        
    # Override the rotor_nums for testing
    rotor_nums = [[4, 1, 7], [5, 1, 7], [6, 1, 7],[7 ,6 ,0],[2 ,3 ,7]]
    results = multithreaded(rotor_nums)
        
    # Override the results for testing
    post_process_results(results)
    