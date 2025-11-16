#injects translations into SYSTEM.BIN file
#which is formatted a little differently from the scenarios so it gets its own script
import system_block as sb
from eng_to_hex import eng_to_hex_single as etoh
import glob
## MASTER POINTER TABLE START ADDRESS
mp_start = 0x8010
mp_table = [] #contains all pointers in the master table
#the master pointer contains 2 pointers for each block, one pointing to the block's pointers, the other pointing to the
#beginning of the text
new_mp_table = []
end_of_data = 0x179ac

blocks = [] #each block contains a pointer table and the strings that the pointer table points to
num_translated_blocks = len(glob.glob("engscript\\system\\*.txt"))
#num_translated_blocks = 12
def btoi(bytes):
    return int.from_bytes(bytes, byteorder="little")
def itob(num):
    return num.to_bytes(length=2, byteorder="little")

with open("gamefiles\\input\\SYSTEM.BIN", mode="rb") as o:
    o.seek(mp_start)
    mp_end = o.read(2)  # first offset in the master table
    # which will stay the same as it's the table length as well

    mp_table.append(mp_end)

    while o.tell() != mp_start + int.from_bytes(mp_end, byteorder="little"):
        mp_table.append(o.read(2))

#create block objects from translation files
#will need to have some if statement for when it gets to the 000000 111111 222222 weirdo "offsets"
i = 0
system14 = b''

while i < num_translated_blocks:

    try:
        #exception for the non-text data without a pointer table in system14.txt
        if i == 14:
            with open("engscript\\system\\system14.txt", mode="rb") as f:
                blocks.append(sb.Block())
                system14 = f.read()
        else:
            with open(f"engscript\\system\\system{i}.txt", mode="r") as s:
                l = s.readline()
                blocks.append(sb.Block())

                while l:
                    blocks[i].add_line(etoh(l))
                    print(l)
                    print(etoh(l))
                    l = s.readline()
                blocks[i].remove_last_offset()
                #print(blocks[i].lines)
                #for x in blocks[i].offsets:
                    #print(x.hex())

    except FileNotFoundError as fnf:
        print(str(fnf))
    i += 1

# put back in any untranslated blocks
'''
with open("gamefiles\\input\\SYSTEM.BIN", mode="rb") as f:
    while i < len(mp_table)/2 - 1:
        blocks.append(sb.Block())

        #first read the offsets
        #print(hex(btoi(mp_table[i*2])))
        f.seek(btoi(mp_table[i*2])+mp_start)
        offsets = f.read(btoi(mp_table[i*2+1]) - btoi(mp_table[i*2]))
        #now read the text
        text = f.read(btoi(mp_table[i*2+2]) - btoi(mp_table[i*2+1])) #uses beginning addr of the next offset table to calculate length

        blocks[i].from_untranslated_block(offsets, text.hex())
        #blocks[i].print()

        i += 1
    blocks.append(sb.Block())
    f.seek(btoi(mp_table[i * 2]) + mp_start)
    blocks[i].from_untranslated_block(f.read(), "")
'''
#for block in blocks:
#    block.print()

#generate new pointers for the master table
i = 0
new_mp_table.append(mp_end) #first two pointers stay the same
new_mp_table.append(mp_table[i+1])
offset = btoi(new_mp_table[i+1])
offset = offset + blocks[i].lines_len
new_mp_table.append(itob(offset))
i += 1

while i < len(blocks):

    if i == 14:
        offset = offset + len(system14)
        new_mp_table.append(itob(offset))
    else:
        offset = offset + blocks[i].offset_table_len
        new_mp_table.append(itob(offset))
        offset = offset + blocks[i].lines_len
        new_mp_table.append(itob(offset))
    i += 1

new_mp_table.pop()

if len(mp_table) == len(new_mp_table): print("yep")


for pointer in new_mp_table:
    print(hex(btoi(pointer)))

#write everything to SYSTEM.BIN
with open("gamefiles\\output\\SYSTEM.BIN", mode="rb+") as s:
    s.seek(mp_start)
    for pointer in new_mp_table:
        s.write(pointer)
    i = 0
    while i < len(blocks):
        blocks[i].print()
        if i == 14:
            s.write(system14)
        else:
            for offset in blocks[i].offsets:
                s.write(offset)
            s.write(bytearray.fromhex(blocks[i].lines))
        i += 1

#write everything to new SYSTEM.BIN
#with open as ns, open old as o
#ns.seek(mp_start)
#ns.write(new_mp_table)
#for b in blocks:
#ns.write(b.offsets)
#ns.write(bytearray.fromhex(b.lines))
#o.seek(original_data_start)
#original_data = o.read()
#ns.write(original_data)
