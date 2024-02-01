# Description: Common functions for the Code breaking project
import numpy as np
common_word_list = ["le", "de", "un", "être", "et", "à", "il", "avoir", "ne", "je", "son", "que", "se", "qui", "ce", "dans", "en", "du", "elle", "au", "bonjour","Joël","--"]

def save(message, File_name = None):
    if File_name==None:
        if input("Do you want to save the result ? (y/n)") == "y":
            print("File number?")
            number = input()
            with open('.\\Message\\decoded_message\\decoded_message{}.txt'.format(number), 'w',encoding='utf-8') as file:
                file.write(message)
            print("File saved")
        else:
            print("File NOT saved")
            
    else:
        with open('.\\Message\\{}'.format(File_name), 'w',encoding='utf-8') as file:
            file.write(message)
        print("File saved")

def open_file(path):
    with open(path, 'r',encoding='utf-8') as file:
        np.array(file)
        # on fait des choses avec le fichier
        message = file.read() # chaîne de caractère avec le contenu du fichier
    #print(message)
    return message

def find_most_likely(possible_width):
    most_likely = max(possible_width, key=lambda x: x[1])[0]
    return most_likely

def number_of_words(message):
    word_count = 0
    List_Word = message.split()
    for word in List_Word:
        if word in common_word_list:
            word_count += 1
    return word_count

def frequency_analysis(message):
    char_count = {}
    for letter in message:
        if letter in char_count:
            char_count[letter] += 1
        else:
            char_count[letter] = 1
    sorted_items = sorted(char_count.items(), key=lambda item: item[1], reverse=True)
    first_common_char = sorted_items[0][0]
    secound_common_char = sorted_items[1][0]
    if ord(" ") - ord(first_common_char) == ord("e") - ord(secound_common_char):  #check if the most common character is space and the secound most common is an 'e'
        key =  ord(" ") - ord(first_common_char)
        return key 
    else:
        print(ord(" ") - ord(first_common_char), ord("e") - ord(secound_common_char))
        raise ValueError("The message is probably not encoded with a Cesar algorithm/n the most common characters are not space or an 'e' in that order")