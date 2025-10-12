import numpy

#remember to keep a blank empty line at the end of all font tables

onechardict = {} #stores punctuation, space, etc....er, catches useless chars actually
symboldict = {} #stores symbols, such as <X>, <SQUARE>
punctdict = {} #for "a, ", "a. " etc
twochardict = {} #everything else
jpnsdict = {} #to find the hex value of the bytes following 00FB
controlcodes = {"(F3FF)": "F3FF", "(F4FF)": "F4FF", "(FAFF)": "FAFF", "(FDFF)": "FDFF", "(FEFF)": "FEFF",
                "(FFFF)": "FFFF", "(00FB)": "00FB", "(FCFF)": "FCFF", "(00FB)": "00FB"}

singlefontdict = {}

with open("charactertables\\langvsingle.tbl", mode="r") as f:
    s = f.readline()
    while s:
        kvpair = s.split("=")
        kvpair[1] = kvpair[1][:-1]
        singlefontdict[kvpair[1]] = kvpair[0]
        s = f.readline()


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

#print(onechardict)
#print(twochardict)
#print(punctdict)
#print(symboldict)
#print(jpnsdict)

hexstring = ""


def eng_to_hex_single(s): #converts ascii string to the single character font encoding
    if s[-1] == "\n":
        s = s[:-1]  # remove carriage return

    hexstring = ""

    i = 0
    while i < len(s):
        if s[i] == "(" and len(s) >= i+6: #check for control code
            cc_string = s[i:i+6].upper()

            if cc_string in controlcodes:
                if len(hexstring) % 4 != 0:
                    hexstring += "B8" #make sure control codes are byte aligned

                try:
                    hexstring += controlcodes[cc_string]
                except KeyError as e:
                    print(f'{cc_string} not found in control codes')

                i += 6

                if cc_string == "(00FB)": #add halfword containing voice line offset
                    hexstring += jpnsdict[s[i]]
                    i += 1
            else:
                hexstring += singlefontdict[s[i]]
                i += 1
        elif s[i] == "<": #catches symbols
            embed_len = 1
            closing_bracket = s[i+embed_len]
            while closing_bracket != ">":
                embed_len += 1
                closing_bracket = s[i+embed_len]
            embed_len += 1
            embed = s[i:embed_len]
            try:
                hexstring += singlefontdict[embed]
            except KeyError as e:
                print(f'{embed} not found in font table')
            i += embed_len

        else: #normal character
            try:
                hexstring += singlefontdict[s[i]]
            except KeyError as e:
                print(f'{s[i]} not found in font table')
            i += 1
    return hexstring

#print(eng_to_hex_single("<BULLET>"))

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
        #print(pair)
        if "(" in pair:
            start = i + 1 if pair[1] == "(" else i
            #print("look for control code")

            if len(s) >= start+6: # check string size is large enough to contain control code

                cc = s[start:start+6] # potential control code
                #print(s)
                if start+6 <= len(s) and cc in controlcodes:
                    s = s[start + 6::]
                    i = 0

                    if cc == "(00FB)":
                        hexstring += controlcodes[cc]

                    if pair[1] == '(':
                        #i += 5
                        #print(f'i:{i}')
                        if cc == "(00FB)":
                            #print(s[i+2])
                            #hexstring += controlcodes[cc]
                            hexstring += jpnsdict[s[i]]
                            i += 1
                        if len(s) == 0:
                            #if end of line, control code needs to be at the end

                            hexstring += eng_to_hex(pair[0] + " ")
                        elif cc == "(F3FF)":
                            #control code needs to be after the character to highlight it
                            if s[0] == " ":
                                hexstring += eng_to_hex(pair[0]+s[0])
                                i += 1
                            else:
                                hexstring += eng_to_hex(pair[0] + " ")
                        else:
                            try:
                                eng_to_hex(pair[0]+s)
                                s = pair[0] + s
                            except:
                                s = pair[0] + " " + s
                        # makes it to where it puts the first char with the char after the code
                        # provided there is one and it results a valid pair
                    else:
                        #i += 4
                        if cc == "(00FB)":
                            #print(s[i+2])
                            #print(s[i])
                            #print(i+2)
                            hexstring += jpnsdict[s[i]]
                            i += 1
                            # preserve argument for 00FB control code
                if cc != "(00FB)":
                    hexstring += controlcodes[cc]
                #i += 2

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
            e = f"Character pair {pair} not found in table"
            raise Exception(e)
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

