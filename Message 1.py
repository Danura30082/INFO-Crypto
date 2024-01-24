
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

def brutforce(message):
    current_width = 1
    possible_width = []
    if max_width > len(message):
        max_width = len(message)
        
    while current_width < max_width:
        newmessage = ""
        word_count = 0
        for loop in range(current_width):
            newmessage += message[loop::current_width]
        List_Word = newmessage.split()
        for word in List_Word:
            if word in dict:
                word_count += 1
        if word_count != 0:
            possible_width.append((current_width, word_count))
            print(current_width, word_count)
        
        current_width += 1
    return possible_width



for width, count in possible_width:
    plt.plot(width, count, 'r.')
plt.show(block=False)
newmessage = ""
for loop in range(334):
    newmessage += message[loop::334]
print(newmessage) 

plt.pause(1000)
    
# à partir d'ici, le fichier est fermé