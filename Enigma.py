from rotor_enigma import rotor, rotor_inverser, message_test
from common import open_file, save

def increment_position(position, direction=1,rayon = 256):
    position[0]+=direction
    for i in range(len(position)):
        if position[i] == rayon and direction == 1:
            position[i] = 0
            if i != len(position)-1:
                position[i+1] += 1
        if position[i] == -1 and direction == -1:
            position[i] = rayon-1
            if i != len(position)-1:
                position[i+1] -= 1
    return position


def encode_enigma(rotor_num, position, message, rayon = 256):
    newmessage = ""
    for char in message:
        num_char = ord(char)
        for i in range(len(rotor_num)):
            rotor_i = rotor_num[i]
            num_char=(num_char+position[i])%rayon
            num_char=(rotor[rotor_i][num_char])
            num_char=(num_char-position[i])%rayon
        newmessage += chr(num_char)
        position = increment_position(position)
    return newmessage

def decode_enigma(rotor_num, position, message, rayon = 256):
    newmessage = ""
    for char in message:
        num_char = ord(char)
        for i in range(len(rotor_num)):
            rotor_i = rotor_num[i]
            num_char=(num_char+position[i])%rayon
            num_char=(rotor_inverser[rotor_i][num_char])
            num_char=(num_char-position[i])%rayon
        newmessage += chr(num_char)
        position = increment_position(position,-1)
    return newmessage






if __name__ == "__main__":
    clear_message = open_file(r'.\\Message\\decoded_message\\message_7_enigma.txt')
    message = message_test #open_file(r'.\\Message\\message7_enigma.txt')
    rotor_num = [0,1,2]
    position_init = [0, 0, 0]
    encrypted_message= encode_enigma(rotor_num, position_init, clear_message)
    print(encrypted_message)
    print(encrypted_message == message)

    