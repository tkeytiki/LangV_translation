#injects translations into SYSTEM.BIN file
#which is formatted a little differently from the scenarios so it gets its own script
import system_block as sb
import eng_to_hex as etoh
## MASTER POINTER TABLE START ADDRESS
mp_start = 0x8010
mp_table = [] #contains all pointers in the master table
new_mp_table = []

blocks = [] #each block contains a pointer table and the strings that the pointer table points to

with open("gamefiles\\output\\SYSTEM.BIN", mode="rb") as o:
    o.seek(mp_start)
    mp_end = o.read(2)  # first offset in the master table
    # which will stay the same as it's the table length as well

    mp_table.append(mp_end)

    while o.tell() != mp_start + int.from_bytes(mp_end, byteorder="little"):
        mp_table.append(o.read(2))

#create block objects from translation files
i = 0
while i < len(mp_table):
    try:
        with open(f"engscript\\system\\system{i}.txt", mode="r", encoding="shift-jis") as s:
            l = s.readline()
            blocks.append(sb.Block())

            while l:
                blocks[i].add_line(etoh.eng_to_hex(l))
                l = s.readline()

            print(blocks[i].lines)
            for x in blocks[i].offsets:
                print(x.hex())

    except FileNotFoundError as fnf:
        print(str(fnf))
    i += 1


#generate new pointers for the master table
i = 0
new_mp_table.append(mp_end) #first two pointers stay the same
new_mp_table.append(mp_table[i+1])
while i < len(blocks):


    #keep commented until all system blocks are translated

    offsets_start = blocks[i].lines_len + int.from_bytes(new_mp_table[i+1], byteorder="little")
    new_mp_table.append(offsets_start.to_bytes(length=2, byteorder="little"))
    if i != len(blocks) - 1:
        lines_start = blocks[i+1].offset_table_len + int.from_bytes(new_mp_table[i+2], byteorder="little")
        new_mp_table.append(lines_start.to_bytes(length=2, byteorder="little"))
    i += 1





#pushes back all the original pointers
#this is only for testing purposes while i don't have all system blocks translated
#later all original pointers will be overwritten
i = len(new_mp_table)
print(i)

total_len = 0
for b in blocks:
    total_len += b.lines_len + b.offset_table_len

print(mp_table)

original_len = int.from_bytes(mp_table[i-1], byteorder="little") - int.from_bytes(mp_table[0], byteorder="little")
print(original_len)
total_len = int.from_bytes(new_mp_table[i-1], byteorder="little") - int.from_bytes(mp_table[0], byteorder="little")
offset_amt = total_len - original_len
while i < len(mp_table) - 1:
    new_addr = int.from_bytes(mp_table[i], byteorder="little") + offset_amt
    new_mp_table.append(new_addr.to_bytes(length=2, byteorder="little"))
    i += 1

for e in new_mp_table:
    print(e.hex())

print(len(new_mp_table))
print(len(mp_table))

print(blocks[0].print())