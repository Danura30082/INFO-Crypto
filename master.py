from common import open_file, save
from Scytale import Scytale
from Cesar import Cesar

message_path=[]
message_decode_path=[]
for loop in range(1,9):
    message_path.append('.\\Message Codee\\message{}.txt'.format(loop))
for loop in range(1,9):
    message_decode_path.append('message{}_decode.txt'.format(loop))

message_num = 0
save(Scytale(open_file(message_path[message_num]))[0],message_decode_path[message_num])

message_num = 1
save(Cesar(open_file(message_path[message_num]))[0],message_decode_path[message_num])

message_num = 2
save(Cesar(open_file(message_path[message_num]))[0],message_decode_path[message_num])




