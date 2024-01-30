# Description: This file contains the functions to decode a message encoded with a Cesar algorithm with a different unknown key for even and odd letters
import matplotlib.pyplot as plt
from common import open_file, save, find_most_likely,number_of_words, common_word_list



def find_smallest_char(message):
    smallest_char_even, smallest_char_odd = ord(message[0]), ord(message[1])
    for letter_index in range(len(message)):
        if letter_index%2 == 0:
            if ord(message[letter_index]) < smallest_char_even:
                smallest_char_even = ord(message[letter_index])
        else:
            if ord(message[letter_index]) < smallest_char_odd:
                smallest_char_odd = ord(message[letter_index])     
    return smallest_char_even, smallest_char_odd

def brutforce_Cesar(message,key=500):
    possible_key=[]
    smallest_even_key, smallest_odd_key = find_smallest_char(message) # on cherche le plus petit caractère du message
    for current_odd_key in range(-smallest_odd_key,key-smallest_odd_key):
        for current_even_key in range(-smallest_even_key,key-smallest_even_key):
            newmessage = ""
            word_count = 0
            for letter_index in range(len(message)):
                if letter_index%2 == 0:
                    current_key = current_even_key
                else:
                    current_key = current_odd_key
                newmessage += chr(max(ord(message[letter_index])+current_key,0))
            word_count = number_of_words(newmessage)
            if word_count != 0:
                possible_key.append(((current_even_key,current_odd_key), word_count))
                print("Key = ",(current_even_key,current_odd_key)," Word count = ", word_count)
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

def Even_Odd_Cesar(message, key=10):
    possible_key = brutforce_Cesar(message, key)
    if possible_key: #check if possible_key is not empty
        most_likely = find_most_likely(possible_key)
        return decode(message, most_likely), possible_key
    else:
        raise ValueError("No Word found in decoded message \n Try to increase key, changing algorithm or increasingt the size of the dictionary")
    
if __name__ == "__main__":
    path=r'.\Message\message4.txt'
    message = open_file(path)
    message_decode, possible_key = Even_Odd_Cesar(message,50)
    plot(possible_key)
    save(message_decode)
    #plt.pause(1000)
    
# à partir d'ici, le fichier est fermé