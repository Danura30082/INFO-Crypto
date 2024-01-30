# Description: This file contains the functions to decode a message encoded with a Scytale algorithm with an unknown key
import matplotlib.pyplot as plt
from common import open_file, save, find_most_likely,number_of_words, common_word_list



def brutforce_Scytale(message, max_key = 500):
    current_key = 1
    possible_key = []
    if max_key > len(message): # si la largeur maximale est plus grande que la longueur du message, on la réduit
        max_key = len(message)
        
    for current_key in range (max_key): # on teste toutes les largeurs possibles
        newmessage = ""
        word_count = 0
        for loop in range(current_key): # on crée une nouvelle chaîne de caractère avec le message décalé
            newmessage += message[loop::current_key]
            
        word_count = number_of_words(newmessage)
        if word_count != 0:
            possible_key.append((current_key, word_count))
            print("Key = ",current_key," Word count = ", word_count)
        
        current_key += 1
    return possible_key

def plot (possible_key):
    for key, count in possible_key:
        plt.plot(key, count, 'r.')
    plt.show(block=False)

def decode_Scytale(message, key):
    newmessage = ""
    for loop in range(key):
        newmessage += message[loop::key]
    return newmessage

def Scytale(message,key=500):
    possible_key = brutforce_Scytale(message, key)
    if possible_key: #check if possible_key is not empty
        most_likely = find_most_likely(possible_key)
        return decode_Scytale(message, most_likely), possible_key
    else:
        raise ValueError("No Word found in decoded message \n Try to increase max_key, changing algorithm or increasingt the size of the dictionary")
    
if __name__ == "__main__":
    path=r'.\Message\message1.txt'
    message = open_file(path)
    message_decode, possible_key = Scytale(message)
    plot(possible_key)
    save (message_decode)
    plt.pause(1000)
    
# à partir d'ici, le fichier est fermé