
import numpy as np
import matplotlib.pyplot as plt
from common import open_file, save, find_most_likely
common_word_list = ["Joël"]

def find_smallest_char(message):
    smallest_char = ord(message[0])
    for letter in message:
        if ord(letter) < smallest_char:
            smallest_char = ord(letter)
    return smallest_char

def brutforce_Cesar(message,key=500):
    possible_key=[]
    smallest_key = find_smallest_char(message) # on cherche le plus petit caractère du message
    for current_odd_key in range(-smallest_key,key):
        for current_even_key in range(-smallest_key,key):
            newmessage = ""
            word_count = 0
            for letter_index in range(len(message)):
                if letter_index%2 == 0:
                    current_key = current_even_key
                else:
                    current_key = current_odd_key
                newmessage += chr(ord(message[letter_index])+current_key)
            List_Word = newmessage.split()
            for word in List_Word:
                if word in common_word_list:
                    word_count += 1
            if word_count != 0:
                possible_key.append(((current_even_key,current_odd_key), word_count))
                print("Key = ",(current_even_key,current_odd_key)," Word count = ", word_count)
            print("\rWorking on keys: ({}, {})".format(current_even_key, current_odd_key), end='', flush=True)
    print("\rDone working on keys.                ")  # Extra spaces to overwrite previous output
    return possible_key

def plot (possible_key):
    for key, count in possible_key:
        plt.plot(key[0], count, 'r.')
        plt.plot(key[1], count, 'b.')
    plt.show(block=False)

def decode(message, key):
    newmessage = ""
    for letter_index in range (len(message)):
        if letter_index%2 == 0:
            current_key = key[0]
        else:
            current_key = key[1]
        newmessage += chr(ord(message[letter_index]) + current_key)
    return newmessage

def Cesar(message, key=50):
    possible_key = brutforce_Cesar(message, key)
    if possible_key: #check if possible_key is not empty
        most_likely = find_most_likely(possible_key)
        return decode(message, most_likely), possible_key
    else:
        raise ValueError("No Word found in decoded message \n Try to increase key, changing algorithm or increasingt the size of the dictionary")
    
if __name__ == "__main__":
    
    path=r'Message Codee\Test Cesar Odd Even copy.txt'
    message = open_file(path)
    message_decode, possible_key = Cesar(message,len(message))
    plot(possible_key)
    save(message_decode)
    #plt.pause(1000)
    