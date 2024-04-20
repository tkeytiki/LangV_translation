import io

with open("font\\font.bin", mode="rb") as f, \
        open("gamefiles\\input\\SYSTEM.BIN", mode="rb") as syst, \
        open("gamefiles\\output\\SYSTEM.BIN", mode="wb") as newsys:
    font = f.read()
    syst.seek(int(len(font)))
    systr = syst.read()
    print(len(systr))
    newsys.write(font+systr)

