import numpy

onechardict = {} #stores punctuation, space, etc....er, catches useless chars actually
symboldict = {} #stores symbols, such as <X>, <SQUARE>
punctdict = {} #for "a, ", "a. " etc
twochardict = {} #everything else
jpnsdict = {} #to find the hex value of the bytes following 00FB
controlcodes = {"(F3FF)": "F3FF", "(F4FF)": "F4FF", "(FAFF)": "FAFF", "(FDFF)": "FDFF", "(FEFF)": "FEFF",
                "(FFFF)": "FFFF", "(00FB)": "00FB", "(FCFF)": "FCFF", "(00FB)": "00FB"}

with open("charactertables\\langvjapanese.tbl", mode="r", encoding="shift_JIS") as f:
    s = f.readline()
    while s:
        kvpair = s.split("=")
        kvpair[1] = kvpair[1][:-1]
        jpnsdict[kvpair[1]] = kvpair[0]
        s = f.readline()

with open("charactertables\\langvdual.tbl", mode="r", encoding="UTF-8") as f:
    s = f.readline()
    #s = f.readline() # skip the space character, it breaks everything and will not be used
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

print(onechardict)
#print(twochardict)
#print(punctdict)
#print(symboldict)
#print(jpnsdict)

hexstring = ""


def eng_to_hex(s):
    if s[-1] == "\n":
        #print("carriage removed")
        s = s[:-1]  # remove carriage return
        #print(f"string len after removal is {len(s)}")

    #print(f"String length is {len(s)}")
    #print(f"String: {s}")

    hexstring = ""

    # now must go through line by two char pairs
    i = 0
    while i < len(s):
        pair = s[i:i + 2]
        # check if there is only one char left in line
        if i + 1 == len(s):
            #print("2nd char does not exist")
            pair = s[i] + " "  # append space

        #print(f"pair is {pair}")
        #print(f"Loop iteration is {i / 2}")

        # check for symbol

        if "(" in pair:
            start = i + 1 if pair[1] == "(" else i
            #print("look for control code")

            if len(s) >= start+6: # check string size is large enough to contain control code

                cc = s[start:start+6] # potential control code

                if start+6 <= len(s) and cc in controlcodes:
                    #print(s[start:start+6])

                    if cc == "(00FB)":
                        hexstring += controlcodes[cc]

                    if pair[1] == '(':
                        i += 5
                        #print(f'i:{i}')
                        if cc == "(00FB)":
                            #print(s[i+2])
                            hexstring += controlcodes[cc]
                            hexstring += jpnsdict[s[i+2]]
                            i += 1
                        if i + 2 < len(s):
                            try:
                                #print("Try")
                                #put the normal character that was in the pair with the char that was after
                                #the control code argument
                                hexstring += eng_to_hex(pair[0] + s[i+2])
                                i += 1
                            except:
                                hexstring += eng_to_hex(pair[0] + " ")
                                #print(f"{pair[0] + s[i+2]} pair not possible, use {pair[0]}"+" ")
                        else:
                            hexstring += eng_to_hex(pair[0] + " ")
                        # makes it to where it puts the first char with the char after the code
                        # provided there is one and it results a valid pair
                    else:
                        i += 4
                        if cc == "(00FB)":
                            #print(s[i+2])
                            hexstring += jpnsdict[s[i+2]]
                            i += 1
                            # preserve argument for 00FB control code
                if cc != "(00FB)":
                    hexstring += controlcodes[cc]
                i += 2
                continue

        if pair[0] in onechardict:
            hexstring += onechardict[pair[0]]
            i -= 1 # make iteration advance by only one character
            #print("first char is onechar")
        elif pair[1] in onechardict:
            hexstring = eng_to_hex(pair[0]+" ") + onechardict[pair[1]]
            #print("second char is onechar")

        # check if control code

        # check punctdict
        elif pair in punctdict:
            hexstring += punctdict[pair]
            #print("punctuation")

        # check if the next word is an entry in symbol dict
        elif "<" in pair:
            start = 0
            if pair[1] == "<":
                start = 1
                hexstring += eng_to_hex(pair[0]+" ")
            symbol = ""
            end = 0
            while s[i+start+end] != ">":
                symbol += s[i+start+end]
                end += 1

            symbol += s[i + start + end]
            end += 1

            #print(f"symbol is {symbol}")
            if symbol in symboldict:
                hexstring += symboldict[symbol]
                #print("symbol found")
            else:
                raise Exception("symbol not found")

            i = i + start - 2 + end # increment by amount of remaining chars in the symbol text
        elif pair in twochardict:
            #print("Two char")
            hexstring += twochardict[pair]
        else:
            raise Exception(f"Character pair {pair} not found in table")
        i += 2
        bytestring = bytearray.fromhex(hexstring)
    return hexstring


"""with open("engscript/sc000.txt", mode="r", encoding="shift-jis") as f:
    s = f.readline()

    while s:
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
    #    print(len(x))"""

