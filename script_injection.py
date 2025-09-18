from eng_to_hex import eng_to_hex as etoh
import scenario as dr
import math

#injects new script into data block

#### Constants
OFSP = 0x4 #offset to first script offset (the first halfword is the script length, so we just skip over it)

scenario_list = []
for i in range(len(dr.Scenario.pointers)):
    scenario_list.append(dr.Scenario(i))

with open("gamefiles\\input\\SCEN.DAT", mode="rb") as origin, \
        open("engscript\\sc000.txt", mode="r", encoding="shift-jis") as eng, open("gamefiles\\output\\SCEN.DAT", mode="wb") as new:

    #copy SCEN.DAT
    new.write(origin.read())

    scenario = scenario_list[0]
    origin.seek(scenario.script_pointer)
    original_script_len = int.from_bytes(origin.read(OFSP), byteorder='little')
    new_script_len = 4 # accounts for the 4 bytes holding the script length


    trans = eng.readline()
    offset = int.from_bytes(origin.read(2), byteorder='little')
    first_offset = offset
    offset_addr = origin.tell()

    numlines = 0
    trans_hex = ""
    offset_table = int.to_bytes(offset, 2, 'little').hex()


    while trans:
        numlines += 1
        current_line = etoh(trans)
        print(trans)
        print(current_line)
        trans_hex += current_line
        #print(trans_hex)
        l = math.floor(len(current_line)/2) #number of bits in script line
        #print(l)
        new_script_len += l
        new_script_len += 2 # accounts for the length in bytes of the offset being written

        new_offset = offset + l #calculate the next offset value
        new_offset = int.to_bytes(new_offset, 2, 'little') #convert to bytes


        trans = eng.readline()

        if offset_addr != first_offset+scenario.script_pointer:
            # stop it from writing another offset when it reaches the beginning of script
            # aka offset_addr = first offset in pointer table
            offset_table += new_offset.hex()
            new.seek(offset_addr)
            new.write(new_offset) #write new offset
            #print(f'new offset: {new_offset.hex()}')
            u = int.from_bytes(new_offset, byteorder='little') + scenario.script_pointer
            #print(f'absolute offset: {hex(u)}')



        new.seek(offset + scenario.script_pointer)
        new.write(bytearray.fromhex(current_line)) #write new script


        offset = int.from_bytes(new_offset, 'little') #new offset will be used to write next script and calculate the next offset
        offset_addr = offset_addr + 0x2 #increment through addresses of offsets


    # convert script length to bytes and write

    new.seek(scenario.script_pointer)
    new_script_len = new_script_len.to_bytes(4, byteorder='little')
    new.write(new_script_len)

    # push back the data that follows the script
    # -> change to appending the data that follows the script

    post_script_offset = scenario.script_pointer + original_script_len
    origin.seek(post_script_offset)
    post_script_data = origin.read(dr.Scenario.pointers[scenario.scenario_number + 1] - post_script_offset)

    offset_table = new_script_len.hex() + offset_table

    trans_hex += post_script_data.hex()
    trans_hex = offset_table + trans_hex
    trans_hex = bytearray.fromhex(trans_hex)
    scenario.add_script(trans_hex)
    scenario.repoint_next()

    with open("gamefiles\\output\\SCEN.DAT", mode="wb") as newdata:
        origin.seek(0)
        newdata.write(origin.read())
        newdata.seek(scenario.addr)
        erase = bytearray(dr.Scenario.pointers[scenario.scenario_number+1] - scenario.addr)
        newdata.write(erase)
        newdata.seek(dr.Scenario.new_pointers[scenario.scenario_number])
        newdata.write(scenario.data)
        newdata.write(scenario.script)
        newdata.seek(0)
        newdata.write(dr.Scenario.new_pointers[scenario.scenario_number].to_bytes(length=4, byteorder="little"))


