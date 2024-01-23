import os
# […]
path=r'.\New folder\message1.txt'
with open(path, 'r') as file:
    # on fait des choses avec le fichier
    message = file.read() # chaîne de caractère avec le contenu du fichier
    print(message)
# à partir d'ici, le fichier est fermé