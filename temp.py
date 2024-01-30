""" str="bonjour"
newmessage = ""
for i in range(3):
    newmessage += str[i::3]
print(newmessage)
newnewmessage = ""
for i in range(3):
    newnewmessage += newmessage[i::3-len(newmessage)%3]
print(newnewmessage) """

str= "I am hurt very badly help le de un être et à il avoir ne je son que se qui ce dans en du elle au "
encoded= ""
for loop in range(len(str)):
    if loop%2 == 0:
        key=3
    else:
        key=2
    encoded += chr(ord(str[loop])+key)
print(encoded)