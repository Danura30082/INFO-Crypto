from rotor_enigma import rotor, rotor_inverser
from common import open_file, save

def increment_position(position, rayon = 256):
    position[0]+=1
    for i in range(len(position)):
        if position[i] == rayon :
            position[i] = 0
            if i != len(position)-1:
                position[i+1] += 1
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
        for i in range(len(rotor_num)-1,-1,-1):
            rotor_i = rotor_num[i]
            num_char=(num_char+position[i])%rayon
            num_char=(rotor_inverser[rotor_i][num_char])
            num_char=(num_char-position[i])%rayon
        newmessage += chr(num_char)
        position = increment_position(position)
    return newmessage






if __name__ == "__main__":
    #check decode and encode working properly
    rotor_num = [0,1,2]
    position_init = [0, 0, 0]
    clear_message = open_file(r'.\\Message\\decoded_message\\message_7_enigma.txt')
    from rotor_enigma import message_test
    assert clear_message == decode_enigma(rotor_num, position_init, message_test)
    position_init = [0, 0, 0]
    assert message_test == encode_enigma(rotor_num, position_init, clear_message)
    
    
    