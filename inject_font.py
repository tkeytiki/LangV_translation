import io

def inject_font():
    with open("font\\font.bin", mode="rb") as f, \
            open("gamefiles\\input\\SYSTEM.BIN", mode="rb") as syst, \
            open("gamefiles\\output\\SYSTEM.BIN", mode="wb") as newsys:
        font = f.read()
        syst.seek(int(len(font)))
        systr = syst.read()
        newsys.write(font+systr)

def inject_font_oneletter():
    with open("font\\oneletterfont.bin", mode="rb") as f, \
            open("font\\fontextension.bin", mode="rb") as fe, \
            open("gamefiles\\input\\SYSTEM.BIN", mode="rb") as syst, \
            open("gamefiles\\output\\SYSTEM.BIN", mode="wb") as newsys:
        font = f.read()
        font += fe.read()
        print(font)
        syst.seek(int(len(font)))
        systr = syst.read()
        newsys.write(font+systr)
        #insert blank space for B8 "character"
        newsys.seek(0xb8*18)
        newsys.write(bytearray(18)) #write 144 blank 0 bits
