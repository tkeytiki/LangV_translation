from pathlib import Path

#run this after inserting the script

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
#change text box sizes
with open("gamefiles\\output\\SLPS_018.19", mode="r+b") as newf, \
        open("asm\\altfunc.bin", mode="rb") as af, \
        open("asm\\levelfunction.bin", mode="rb") as lf, \
        open("asm\\levelfunction2.bin", mode="rb") as lf2:
    newf.seek(beight_assign)
    newf.write(b'\xb8\x00\x02\x24') # b8 00 02 24 <-- instruction to load b8
    newf.seek(altered_func_addr)
    newf.write(af.read())
    #text box etc
    newf.seek(0xc576a)
    newf.write(b'\x08')
    newf.seek(0xc5782)
    newf.write(b'\x08')
    newf.seek(0xc579a)
    newf.write(b'\x08')
    newf.seek(0xc57a6)
    newf.write(b'\x0D')
    newf.seek(0xc57be)
    newf.write(b'\x02\x00\x02\x00\x0E')
    newf.seek(0xc57ec)
    newf.write(b'\x07')
    newf.seek(0xc57f4)
    newf.write(b'\x07')
    newf.seek(0xc57fc)
    newf.write(b'\x07')
    newf.seek(0xc580e)
    newf.write(b'\x01')
    newf.seek(0xc58ba)
    newf.write(b'\x07')
    newf.seek(0xc591e)
    newf.write(b'\x08')
    newf.seek(0xc62ab)
    newf.write(b'\x08')
    newf.seek(0xc62b4)
    newf.write(b'\x08')
    newf.seek(0xc7482)
    newf.write(b'\x1b')
    newf.seek(0xc749a)
    newf.write(b'\x18')
    newf.seek(0xc76c2)
    newf.write(b'\x12')
    newf.seek(0xcb465)
    newf.write(b'\x01\x00\x00\x00\x01')
    #level up screen modifications
    newf.seek(0x998c4)
    newf.write(b'\x00\x00\x02\x24')
    newf.seek(0x99a9c)
    newf.write(b'\x06\x46')
    newf.seek(0x99b00)
    newf.write(b'\x06\x46')
    #hook to rewrite stat ups
    newf.seek(0x99c1c)
    jump = b'\xe4\x68\x03\x08\x07\x00\x42\x24' #jump to da390 and add 7 to v0
    newf.write(jump)
    newf.seek(0x99cec)
    newf.write(jump)
    #write level disp function
    newf.seek(0xcab90)
    newf.write(lf.read())
    newf.seek(0x7f6e4)
    newf.write(b'\x0c\x69\x03\x08') #jump to da430
    newf.seek(0x99ad8)
    newf.write(b'\x1c\x69\x03\x08') #jump to da450
    #write "level increased" fix
    newf.seek(0xcac30)
    newf.write(lf2.read())
    #remove N character from scenario loading screen
    newf.seek(0x97058)
    newf.write(b'\x00')

#disables the naming screen
with open("gamefiles\\output\\SCEN.DAT", mode="rb") as f, open("gamefiles\\output\\SCEN.DAT", mode="r+b") as newf:
    newf.write(f.read())
    newf.seek(name_screen_args)
    new_args = bytearray(12)
    newf.write(new_args)