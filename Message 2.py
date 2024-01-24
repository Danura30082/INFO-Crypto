
import numpy as np
import matplotlib.pyplot as plt
dict = ["le", "de", "un", "être", "et", "à", "il", "avoir", "ne", "je", "son", "que", "se", "qui", "ce", "dans", "en", "du", "elle", "au", "bonjour"]
#dict = ["Bonjour"]
path=r'.\Message Codee\message1.txt'
delta = 500
possible_delta=[]
def open_file(path):
    with open(path, 'r',encoding='utf-8') as file:
        np.array(file)
        # on fait des choses avec le fichier
        message = file.read() # chaîne de caractère avec le contenu du fichier
    #print(message)
    return message

def brutforce_Cesar(message,delta):
    for loop in range(delta):
        newmessage = ""
        word_count = 0
        for letter in message:
            newmessage += chr(ord(letter)+loop)
        List_Word = newmessage.split()
        for word in List_Word:
            if word in dict:
                word_count += 1
        if word_count != 0:
            possible_delta.append((loop, word_count))
            print(loop, word_count)
    return possible_delta
    

def plot (possible_width):
    for width, count in possible_width:
        plt.plot(width, count, 'r.')
    plt.show(block=False)

def decode(message, width):
    newmessage = ""
    for loop in range(width):
        newmessage += message[loop::width]
    return newmessage

message = open_file(path)
possible_delta = brutforce_Cesar(message, delta)
plot(possible_delta)
most_likely = max(possible_delta, key=lambda x: x[1])[0]
print(most_likely)
print(decode(message, most_likely))
if input("Do you want to save the result ? (y/n)") == "y":
    with open(r'.\Message Codee\message1_decode.txt', 'w',encoding='utf-8') as file:
        file.write(decode(message, most_likely))
    print("File saved")


plt.pause(1000)
    
# à partir d'ici, le fichier est fermé