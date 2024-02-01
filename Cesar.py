# Description: This file contains the functions to decode a message encoded with a Cesar algorithm with an unknown key
import matplotlib.pyplot as plt
from common import open_file, save, frequency_analysis


def decode(message, key):
    newmessage = ""
    for letter in message:
            newmessage += chr(ord(letter) + key)
    return newmessage

def Cesar(message):
    key = frequency_analysis(message)
    return decode(message, key)
    
if __name__ == "__main__":
    path=r'.\Message\message2.txt'
    message = open_file(path)
    decoded_message2= Cesar(message)
    
    path=r'.\Message\message3.txt'
    message = open_file(path)
    decoded_message3 = Cesar(message)
    save(decoded_message2)
    save(decoded_message3)
    