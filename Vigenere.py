# Description: This file contains the functions to decode a message encoded with a Vignere algorithm with a different unknown key for even and odd letters
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from common import open_file, save, find_most_likely,number_of_words, common_word_list
import itertools

def find_smallest_char(message, key_length = 1):
    smallest_key = [ord(message[i]) for i in range(key_length)]
    for letter_index in range(len(message)): # on parcourt le message
        if ord(message[letter_index]) < smallest_key[letter_index%key_length]:
            smallest_key[letter_index%key_length] = ord(message[letter_index])
    return smallest_key

def find_Vigenere_key_length(message, max_key_length = 100): 
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def find_peaks(data):
        peaks = []
        for i in range(1, len(data)-1):  # Skip the first and last element
            if data[i] > data[i-1] and data[i] > data[i+1]:  # If the current element is a peak
                peaks.append(i)
        if len(peaks) == 0:
            raise ValueError("No peak found in the data")
        return peaks

    possible_key_length = []
    for key in range(1,max_key_length):
        repetition = 0
        for letter_index in range (len(message)):
            if message[letter_index] == message[letter_index - key]:
                repetition+=1
        possible_key_length.append(repetition)
    
    peaks = find_peaks(possible_key_length)

    gcd_value = peaks[0]+1
    for peak in peaks[1:]:
        gcd_value = gcd(gcd_value, peak+1)
    if gcd_value == 1:
        raise ValueError("No possible key length found \n reassess if the message is long enough or try to increase max_key_length \n check if the message is encoded with a Vigenere algorithm")
    print ("Most likely key length : ",gcd_value)
    return gcd_value

def brutforce_Vigenere(message,key_length,smallest_char,max_key):
    possible_key=[]  
    for current_key in itertools.product(range(max_key), repeat=key_length):
        for loop in range (len(smallest_char)):
            current_key = list(current_key)
            current_key[loop] = current_key[loop]-smallest_char[loop]
        decoded_message = decode(message, current_key)
        word_count = number_of_words(decoded_message)
        if word_count != 0:
            possible_key.append((current_key,word_count))
            print("Key = ",current_key," Word count = ", word_count)
            
    return possible_key
    


def Vigenere(message, max_key=15, max_key_length=100):
    key_lenth=find_Vigenere_key_length(message, max_key_length)
    smallest_char = find_smallest_char(message, key_lenth)
    possible_key = brutforce_Vigenere(message,key_lenth,smallest_char, max_key)
    if possible_key: #check if possible_key is not empty
        most_likely = find_most_likely(possible_key)
        return decode(message, most_likely), possible_key
    else:
        raise ValueError("No Word found in decoded message \n Try to increase key, changing algorithm or increasingt the size of the dictionary")
    
def plot (possible_key):
    for i in range(len(possible_key)):
        plt.plot(i, possible_key[i][1], 'r.')
    plt.show(block=False)
    plt.pause(1000)

def decode(message, key):
    newmessage = ""
    for letter_index in range (len(message)):
        newmessage += chr(ord(message[letter_index]) + key[letter_index%len(key)])
    return newmessage

    
if __name__ == "__main__":
    path=r'.\Message\message5.txt'
    message = open_file(path)
    max_key, max_key_length = 11, 5
    try:
        decoded_message, possible_key = Vigenere(message,max_key,max_key_length)
        print(find_most_likely(possible_key))
        plot(possible_key)
        save(decoded_message)
        
    except ValueError as error:
        print(error)
    
