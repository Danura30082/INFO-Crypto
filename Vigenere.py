# Description: This file contains the functions to decode a message encoded with a Vignere algorithm with a different unknown key for even and odd letters
import matplotlib.pyplot as plt
from common import open_file, save, frequency_analysis

def find_Vigenere_key_length(message, max_key_length = 100, distance = 1): 
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def find_peaks(data, distance):
        peaks = []
        for i in range(len(data)):
            if all(data[i] > data[i+k] for k in range(-distance, distance+1) if i+k < len(data) and k != 0):
                peaks.append(i)
        if len(peaks) == 0:
            raise ValueError("No peak found in the data")
        return peaks
    fail_count = 0 # number of times the algorithm failed to find a key length
    possible_key_length = []
    for key in range(1,max_key_length):
        repetition = 0
        for letter_index in range (len(message)):
            if message[letter_index] == message[letter_index - key]:
                repetition+=1
        possible_key_length.append(repetition)
    
    peaks = find_peaks(possible_key_length, distance)
    print(peaks)
    gcd_value = peaks[0]+1
    for peak in peaks[1:]:
        gcd_value = gcd(gcd_value, peak+1)
    if gcd_value == 1 :
        if fail_count < 5:
            fail_count += 1
            print("No key length found for distance = ",distance," trying distance = ",distance+2)
            gcd_value = find_Vigenere_key_length(message, max_key_length, distance+2)
        else:
            raise ValueError("No key length found \n reassess if the message is long enough or try to increase max_key_length/distance \n check if the message is encoded with a Vigenere algorithm")
    print ("Most likely key length : ",gcd_value)
    return gcd_value


def Vigenere(message, max_key_length=100):
    key_lenth=find_Vigenere_key_length(message, max_key_length)
    separated_message = [] #list of messages separated by key length
    key=[]
    for i in range(key_lenth):
        separated_message.append(message[i::key_lenth])
        key.append(frequency_analysis(separated_message[i]))
    return decode(message, key), key
    

def decode(message, key):
    newmessage = ""
    for letter_index in range (len(message)):
        newmessage += chr(ord(message[letter_index]) + key[letter_index%len(key)])
    return newmessage

    
if __name__ == "__main__":
    path=r'.\Message\message4.txt'
    message = open_file(path)
    decoded_message, key = Vigenere(message)
    print(key)
    save(decoded_message)
    
    path=r'.\Message\message5.txt'
    message = open_file(path)
    decoded_message, key = Vigenere(message)
    print(key)
    save(decoded_message)
    
    path=r'.\Message\message6.txt' 
    message = open_file(path)
    decoded_message, key = Vigenere(message)
    print(key)
    save(decoded_message)
    
    
    #doesn't quite work
    """ path=r'.\Message\message7.txt'
    message = open_file(path)
    decoded_message, key = Vigenere(message)
    print(key)
    save(decoded_message) """