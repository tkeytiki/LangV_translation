from eng_to_hex import eng_to_hex as etoh
import math

#### First Scenario Script Pointer ####
FSSP = 0x22f4 #seems to be unique from subsequent scenario script offset calculations

#### Constants
OFSP = 0x4 #offset to first script offset (the first halfword is the script length, so we just skip over it)

with open("gamefiles\\input\\SCEN.DAT", mode="rb") as origin, \
        open("engscript\\sc000.txt", mode="r", encoding="shift-jis") as eng, open("gamefiles\\output\\SCEN.DAT", mode="wb") as new:

    #copy SCEN.DAT
    new.write(origin.read())

    origin.seek(FSSP)
    original_script_len = int.from_bytes(origin.read(4), byteorder='little')
    new_script_len = 0

    #o.seek(FSSP + original_script_len,0)
    #print(hex(o.tell()))
    #print(hex(original_script_len))


    trans = eng.readline()
    offset = int.from_bytes(origin.read(2), byteorder='little')
    first_offset = offset
    offset_addr = origin.tell()

    print(hex(offset_addr))

    while trans:
        trans_hex = etoh(trans)
        print(trans_hex)
        print(trans_hex)
        l = math.floor(len(trans_hex)/2) #number of bytes in script line
        new_script_len += l

        new_offset = offset + l #calculate the next offset value
        new_offset = int.to_bytes(new_offset, 2, 'little') #convert to bytes

        if offset_addr != first_offset:
            new.seek(offset_addr)
            new.write(new_offset) #write new offset

        new.seek(offset + FSSP)
        new.write(bytearray.fromhex(trans_hex)) #write new script

        offset = int.from_bytes(new_offset, 'little') #new offset will be used to write next script and calculate the next offset
        offset_addr = offset_addr + 0x2 #increment through addresses of offsets

        trans = eng.readline()

    #remember to write the new script length




