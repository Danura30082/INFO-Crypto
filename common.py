# Description: Common functions for the Code breaking project
import numpy as np
common_word_list = ["le", "de", "un", "être", "et", "à", "il", "avoir", "ne", "je", "son", "que", "se", "qui", "ce", "dans", "en", "du", "elle", "au", "bonjour","joël"]

def save(message, File_name = None):
    if File_name==None:
        if input("Do you want to save the result ? (y/n)") == "y":
            print("File number?")
            number = input()
            with open('.\\Message Codee\\message{}_decode.txt'.format(number), 'w',encoding='utf-8') as file:
                file.write(message)
            print("File saved")
        exit()
            
    else:
        with open('.\\Message Codee\\{}'.format(File_name), 'w',encoding='utf-8') as file:
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