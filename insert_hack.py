from pathlib import Path

func_addr_mem = 0xda200 #address of new function in memory
func_addr_f = func_addr_mem - 0xf800 #address of new function in file

altered_func_addr = 0x96024 #address of altered function in file

beight_assign = 0x94468 #address where 0xb8 will be assigned to variable

name_screen_args =  0x7903cc

try:
    Path("gamefiles\\output\\SLPS_018.19").unlink()
except FileNotFoundError as ex:
    print(ex)

#insert new function
with open("gamefiles\\input\\SLPS_018.19", mode="rb") as f, open("asm\\newfunction.bin", mode="rb") as fun, \
    open("gamefiles\\output\\SLPS_018.19", mode="wb") as newf:

    newf.write(f.read(func_addr_f)) #read up to addr new func
    funb = fun.read() #contains function
    newf.write(funb) #write function to file
    f.seek(len(funb), 1) #skip over length of function in og file
    newf.write(f.read()) #write the rest of the code

#insert altered function and b8 load
with open("gamefiles\\output\\SLPS_018.19", mode="r+b") as newf, open("asm\\altfunc.bin", mode="rb") as af:
    newf.seek(beight_assign)
    newf.write(b'\xb8\x00\x02\x24') # b8 00 02 24 <-- instruction to load b8
    newf.seek(altered_func_addr)
    newf.write(af.read())

#disables the naming screen
with open("gamefiles\\input\\SCEN.DAT", mode="rb") as f, open("gamefiles\\output\\SCEN.DAT", mode="r+b") as newf:
    newf.write(f.read())
    newf.seek(0x24e4)
    newf.write(b'\x29\x34\x36\x3b\x38\x3f') #29 34 36 3B 38 3F "Rachel" test string
    newf.seek(name_screen_args)
    new_args = bytearray(12)
    newf.write(new_args)