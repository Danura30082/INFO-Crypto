# Description: This file is used to decode all the messages in the folder Message
from common import open_file, save
from Scytale import Scytale
from Cesar import Cesar
from Vigenere import Vigenere
from Enigma import Enigma
import logging

message_path = []
message_decode_path = []
for loop in range(1, 9): #creates a list of paths to the messages and a list of paths to the decoded messages
    message_path.append('.\\Messages\\Encoded_messages\\message_{}.txt'.format(loop))
    message_decode_path.append('\\Decoded_messages\\message_{}.txt'.format(loop))

decoding_functions = [Scytale, Cesar, Cesar, Vigenere, Vigenere, Vigenere, Vigenere,Enigma] # list of decoding functions for each message

for message_num, decode_func in enumerate(decoding_functions):
    
    try:
        message=open_file(message_path[message_num])
        save(decode_func(message)[0], message_decode_path[message_num])
        
    except Exception as e:
        logging.error(f"An error occurred while decoding message {message_num}: {e}")
