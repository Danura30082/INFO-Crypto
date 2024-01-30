# Description: This file is used to decode all the messages in the folder Message
from common import open_file, save
from Scytale import Scytale
from Cesar import Cesar
from Even_Odd_Cesar import Even_Odd_Cesar

message_path=[]
message_decode_path=[]
for loop in range(1,9):
    message_path.append('.\\Message\\message{}.txt'.format(loop))
    message_decode_path.append('message{}_decode.txt'.format(loop))

decoding_functions = [Scytale, Cesar, Cesar, Even_Odd_Cesar]

for message_num, decode_func in enumerate(decoding_functions):
    try:
        save(decode_func(open_file(message_path[message_num]))[0], message_decode_path[message_num])
    except Exception as e:
        print(f"An error occurred while decoding message {message_num}: {e}")




