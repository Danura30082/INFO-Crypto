# Description: This file contains the functions to decode a message encoded with a Cesar algorithm with an unknown key
import matplotlib.pyplot as plt
from common import open_file, save, find_most_likely,number_of_words, common_word_list





def find_smallest_char(message):
    smallest_char = ord(message[0])
    for letter in message:
        if ord(letter) < smallest_char:
            smallest_char = ord(letter)
    return smallest_char

def brutforce_Cesar(message,key=500):
    possible_key=[]
    smallest_key = find_smallest_char(message) # on cherche le plus petit caractère du message
    for current_key in range(-smallest_key,key):
        newmessage = ""
        word_count = 0
        for letter in message:
            newmessage += chr(ord(letter)+current_key)
            
        word_count = number_of_words(newmessage)
        
        if word_count != 0:
            possible_key.append((current_key, word_count))
            print("Key = ",current_key," Word count = ", word_count)
    return possible_key
    

def plot (possible_key):
    for key, count in possible_key:
        plt.plot(key, count, 'r.')
    plt.show(block=False)

def decode(message, key):
    newmessage = ""
    for letter in message:
            newmessage += chr(ord(letter) + key)
    return newmessage

def Cesar(message, key=500):
    possible_key = brutforce_Cesar(message, key)
    if possible_key: #check if possible_key is not empty
        most_likely = find_most_likely(possible_key)
        return decode(message, most_likely), possible_key
    else:
        raise ValueError("No Word found in decoded message \n Try to increase key, changing algorithm or increasingt the size of the dictionary")
    
if __name__ == "__main__":
    
    path=r'.\Message\message2.txt'
    message = open_file(path)
    message_decode2, possible_key = Cesar(message)
    #plot(possible_key)
    
    #plt.pause(1000)
    path=r'.\Message\message3.txt'
    message = open_file(path)
    message_decode3, possible_key = Cesar(message)
    save(message_decode2)
    save(message_decode3)
    
# à partir d'ici, le fichier est fermé