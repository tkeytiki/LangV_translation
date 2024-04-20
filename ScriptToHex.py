import numpy

onechardict = {} #stores punctuation, space, etc....er, catches useless chars actually
symboldict = {} #stores symbols, such as <X>, <SQUARE>
twochardict = {}
punctdict = {} #for "a, ", "a. " can just make 2char..check this dict first bc every sentence has punct, likely case
controlcodes = {"(F3FF)": "F3FF", "(F4FF)": "F4FF", "(FAFF)": "FAFF", "(FDFF)": "FDFF", "(FEFF)": "FEFF",
                "(FFFF)": "FFFF", "(00FB)": "00FB", "(FCFF)": "FCFF"}

with open("C:\\Users\\whopo\\Downloads\\langvdualtable.tbl", mode="r", encoding="UTF-8") as f:
    s = f.readline()
    while s:
        kvpair = s.split("=")
        kvpair[1] = kvpair[1][:-1] #remove terminal return

        if len(kvpair[1]) == 1:
            onechardict[kvpair[1]] = kvpair[0]
        elif kvpair[1][0] == "<":
            symboldict[kvpair[1]] = kvpair[0]
        elif (kvpair[1][1] in [".", ",", "!", "?"]) or (kvpair[1][0] in [".", ",", "!", "?"]):
            punctdict[kvpair[1]] = kvpair[0]
        else:
            twochardict[kvpair[1]] = kvpair[0]
        s = f.readline()

#print(onechardict)
#print(twochardict)
print(punctdict)
print(symboldict)

hexstring = ""



with open("engscript/sc000 (1).txt", mode="r", encoding="shift-jis") as f:
    s = f.readline()
    while s:
        if s in controlcodes:
            hexstring += controlcodes[s]
            if s == "(00FB)":
                t = f.readline() # read next line for argument for 00FB
                hexstring += t.upper()
        #now must go through line by two char pairs
        else:
            for i in range(len(s)-1):
                pass
         #if s in punctdict:
        #case for if second char is space or /n
        #   hexstring += punctdict[s]
        #in twochardict have to check for ". " and ", " case if it's /n
        #nah put this in puncdict
        s = f.readline()



#first check control code
#if control code is 00fb then check next line for arg
#first check one char for the rare elusive one char? or tell ollie to not use
#actually do that otherwise symboldict useless
#first check punct dict
#then check twochardict
#then symboldict

test = bytearray.fromhex("000001000200")

with open("C:\\Users\\whopo\\Downloads\\hexscript.bin", mode="wb") as f:
    f.write(test)
    #for x in kvpair:
    #    print(x)
    #    print(len(x))

