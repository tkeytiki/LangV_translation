import numpy

#bytes = numpy.fromfile("C:\\Users\\whopo\\Desktop\\lang V rip\\L5\\SYSTEM.BIN")

with open("C:\\Users\\whopo\\Downloads\\fonttest.bin", mode="rb") as f, \
        open("C:\\Users\\whopo\\Desktop\\lang V rip\\L5\\SYSTEM.BIN", mode="rb") as syst, \
        open("C:\\Users\\whopo\\Downloads\\SYSTEM.BIN", mode="wb") as newsys:
    font = f.read()
    syst.seek(int(len(font)))
    systr = syst.read()
    print(len(systr))
    newsys.write(font+systr)

