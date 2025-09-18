import os

#text dumps from the game are initially all on one line and it's very unreadable
#this script formats the file to have line breaks after every FEFF and FFFF control code

dump = "system1.txt"
ndump = "system1.txt"

newstr = ""

with open(dump, mode="r", encoding="shift-jis") as f:
    file = f.read()

    i = 0

    while i < len(file):
        if(file[i:i+6]) == "(FEFF)":
            newstr += ("(FEFF)\n")
            i += 6
        elif (file[i:i + 6]) == "(FFFF)":
            newstr += ("(FFFF)\n")
            i += 6
        else:
            newstr += (file[i])
            i += 1

    newstr = newstr[0:len(newstr)-1] #remove final trailing \n

with open(ndump, mode="w", encoding="shift-jis") as n:
    n.write(newstr)