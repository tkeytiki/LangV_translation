import numpy

onechardict = {} #stores punctuation, space, etc....er, catches useless chars actually
symboldict = {} #stores symbols, such as <X>, <SQUARE>
punctdict = {} #for "a, ", "a. " etc
twochardict = {} #everything else
controlcodes = {"(F3FF)": "F3FF", "(F4FF)": "F4FF", "(FAFF)": "FAFF", "(FDFF)": "FDFF", "(FEFF)": "FEFF",
                "(FFFF)": "FFFF", "(00FB)": "00FB", "(FCFF)": "FCFF"}

with open("charactertables\\langvdual.tbl", mode="r", encoding="UTF-8") as f:
    s = f.readline()
    while s:
        kvpair = s.split("=")
        kvpair[1] = kvpair[1][:-1] #remove carriage return

        if len(kvpair[1]) == 1:
            onechardict[kvpair[1]] = kvpair[0]
        elif kvpair[1][0] == "<":
            symboldict[kvpair[1]] = kvpair[0]
        elif (kvpair[1][1] in [".", ",", "!", "?"]) or (kvpair[1][0] in [".", ",", "!", "?"]):
            punctdict[kvpair[1]] = kvpair[0]
            #account for new lines in english translation file
            #if kvpair[1][1] == " ":

        else:
            twochardict[kvpair[1]] = kvpair[0]
        s = f.readline()

#print(onechardict)
print(twochardict)
#print(punctdict)
#print(symboldict)

hexstring = ""



with open("engscript/sc000.txt", mode="r", encoding="shift-jis") as f:
    s = f.readline()

    for line in range(0,20): # while s: in production
        print(f"String length is {len(s)}")
        print(f"String: {s}")

        if s[-1] == "\n":
            print("carriage removed")
            s = s[:-1]  # remove carriage return
            print(f"string len after removal is {len(s)}")
        if s in controlcodes:
            print("string is control code")
            hexstring += controlcodes[s]
            if s == "(00FB)":
                t = f.readline() # read next line for argument for 00FB
                hexstring += t.upper()

        # now must go through line by two char pairs
        else:
            i = 0
            while i < len(s):
                pair = s[i:i+2]
                #check if there is only one char left in line
                if i+1 == len(s):
                    print("2nd char does not exist")
                    pair = s[i] + " " #append space

                print(f"pair is {pair}")
                print(f"Loop iteration is {i/2}")

                # check punctdict
                if pair in punctdict:
                    hexstring += punctdict[pair]
                    print("punctuation")

                # check if the next word is an entry in symbol dict
                elif "<" in pair:
                    start = i + 1 if pair[1] == "<" else i
                    end = 2 if pair[1] == "<" else 1
                    #if pair[1] == "<": # start changes based on which of the pair is open bracket
                     #   start += 1
                     #   end += 1
                    while s[start+end]:
                        if s[start+end] == ">":
                            break
                        end += 1
                    symbol = s[start:start+end+1]
                    print(f"symbol is {symbol}")
                    if symbol in symboldict:
                        hexstring += symboldict[symbol]
                        print("symbol found")
                    else:
                        raise Exception("symbol not found")
                    i += end # increment by amount of remaining chars in the symbol text
                elif pair in twochardict:
                    hexstring += twochardict[pair]
                else:
                    raise Exception("characters not found")
                i += 2
        s = f.readline()

print(hexstring)

#first check control code
#if control code is 00fb then check next line for arg
#first check one char for the rare elusive one char? or tell ollie to not use
#actually do that otherwise symboldict useless
#first check punct dict
#then check twochardict
#then symboldict

#test = bytearray.fromhex("000001000200")
bytestring = bytearray.fromhex(hexstring)

with open("hexscript/hexscript.bin", mode="wb") as f:
    f.write(bytestring)
    #for x in kvpair:
    #    print(x)
    #    print(len(x))

