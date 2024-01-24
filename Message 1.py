
import numpy as np
import matplotlib.pyplot as plt
dict = ["le", "de", "un", "être", "et", "à", "il", "avoir", "ne", "je", "son", "que", "se", "qui", "ce", "dans", "en", "du", "elle", "au", "bonjour"]
#dict = ["Bonjour"]
path=r'.\Message Codee\message1.txt'
max_width = 500

def open_file(path):
    with open(path, 'r',encoding='utf-8') as file:
        np.array(file)
        # on fait des choses avec le fichier
        message = file.read() # chaîne de caractère avec le contenu du fichier
    #print(message)
    return message

def brutforce_Scytale(message, max_width = 500):
    current_width = 1
    possible_width = []
    if max_width > len(message): # si la largeur maximale est plus grande que la longueur du message, on la réduit
        max_width = len(message)
        
    for current_width in range (max_width): # on teste toutes les largeurs possibles
        newmessage = ""
        word_count = 0
        for loop in range(current_width): # on crée une nouvelle chaîne de caractère avec le message décalé
            newmessage += message[loop::current_width]
        List_Word = newmessage.split()
        for word in List_Word: # on compte le nombre de mots dans le message qui correspondent à un mot du dictionnaire
            if word in dict:
                word_count += 1
        if word_count != 0:
            possible_width.append((current_width, word_count))
            print(current_width, word_count)
        
        current_width += 1
    return possible_width

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
possible_width = brutforce_Scytale(message, max_width)
plot(possible_width)
most_likely = max(possible_width, key=lambda x: x[1])[0]
print(most_likely)
print(decode(message, most_likely))
if input("Do you want to save the result ? (y/n)") == "y":
    with open(r'.\Message Codee\message1_decode.txt', 'w',encoding='utf-8') as file:
        file.write(decode(message, most_likely))
    print("File saved")


plt.pause(1000)
    
# à partir d'ici, le fichier est fermé