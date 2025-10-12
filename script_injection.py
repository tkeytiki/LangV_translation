from eng_to_hex import eng_to_hex_single as etoh
import scenario as dr
import glob
import math
from pathlib import Path

#injects new script into data block

#### Constants
OFSP = 0x4 #offset to first script offset (the first halfword is the script length, so we just skip over it)

scenario_list = []
for i in range(len(dr.Scenario.pointers)):
    scenario_list.append(dr.Scenario(i))

num_translated_scenes = len(glob.glob("engscript\\scen\\*.txt"))

try:
    Path("gamefiles\\output\\SCEN.DAT").unlink()
except FileNotFoundError as ex:
    print(ex)
except PermissionError as ex:
    print(ex)

i = 0
with open("gamefiles\\input\\SCEN.DAT", mode="rb") as origin:
    while i < num_translated_scenes:
        with open(f"engscript\\scen\\sc{i}.txt", mode="r", encoding="shift_jis") as eng:
            scenario = scenario_list[i]
            origin.seek(scenario.script_pointer)
            original_script_len = int.from_bytes(origin.read(OFSP), byteorder='little')
            new_script_len = 4  # accounts for the 4 bytes holding the script length

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

                trans_hex += current_line
                # print(trans_hex)
                l = len(current_line) // 2  # number of bytes in script line
                # print(l)
                # print(trans)
                # print(current_line)
                new_script_len += l
                new_script_len += 2  # accounts for the length in bytes of the offset being written

                new_offset = offset + l  # calculate the next offset value
                new_offset = int.to_bytes(new_offset, 2, 'little')  # convert to bytes

                trans = eng.readline()

                if offset_addr != first_offset + scenario.script_pointer:
                    # stop it from writing another offset when it reaches the beginning of script
                    # aka offset_addr = first offset in pointer table
                    offset_table += new_offset.hex()
                    # print(f'new offset: {new_offset.hex()}')
                    u = int.from_bytes(new_offset, byteorder='little') + scenario.script_pointer
                    # print(f'absolute offset: {hex(u)}')

                offset = int.from_bytes(new_offset,
                                        'little')  # new offset will be used to write next script and calculate the next offset
                offset_addr = offset_addr + 0x2  # increment through addresses of offsets

                # check if script is word-aligned
            if new_script_len % 4 != 0:
                trans_hex += "0000"  # pad end of script with zeros to make the next word word-aligned
                new_script_len += 2

            new_script_len = new_script_len.to_bytes(4, byteorder='little')

            #get the data that comes after the script
            post_script_offset = scenario.script_pointer + original_script_len
            origin.seek(post_script_offset)
            post_script_data = origin.read(dr.Scenario.pointers[scenario.scenario_number + 1] - post_script_offset)

            offset_table = new_script_len.hex() + offset_table

            trans_hex += post_script_data.hex()
            trans_hex = offset_table + trans_hex
            trans_hex = bytearray.fromhex(trans_hex)
            scenario.add_script(trans_hex)

            i += 1


for scen in scenario_list:
    scen.repoint_next()

for pointer in dr.Scenario.new_pointers:
    print(hex(pointer))

    #print(scenario_list[1].data)

with open("gamefiles\\output\\SCEN.DAT", mode="wb") as newdata:
    i = 0
    while i < len(scenario_list):
        scenario = scenario_list[i]
        newdata.seek(scenario.addr)
        if i + 1 != len(scenario_list): #do if not final scenario
            erase = bytearray(dr.Scenario.new_pointers[scenario.scenario_number+1] - scenario.addr)
            newdata.write(erase)
        newdata.seek(dr.Scenario.new_pointers[scenario.scenario_number])
        newdata.write(scenario.data)
        if i < num_translated_scenes: #if not translated block, don't try to write script since it's empty
            #and causes type error because it's a string not bytearray
            newdata.write(scenario.script)
        i += 1

    newdata.seek(0)
        #write new pointers to beginning of file
    for pointer in dr.Scenario.new_pointers:
        newdata.write(pointer.to_bytes(length=4, byteorder="little"))


