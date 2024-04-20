import io
import sys
import numpy
from pathlib import Path

numpy.set_printoptions(threshold=sys.maxsize)

with open("font\\psx6x12dualtry.bmp", mode="rb") as i:
    i.seek(0x0A) #offset that contains start addr of pixel array
    offset = i.read(1)[0]
    i.seek(offset)
    with open("font\\noheader.bin", mode="wb") as o:
        o.write(i.read())

bytes = numpy.fromfile("font\\noheader.bin", dtype="uint8")

#bmp image data is stored upside down, have to flip it over each axis

bits = numpy.unpackbits(bytes)[::-1] #vertical flip

newbits = list()

for r in range(int(len(bits)/2304)):
    for x in range(16):
        for y in range(12):
            row = list()
            for xy in range(r*2304+x*12+y*192, r*2304+x*12+12+y*192):
                #newbits.append(bits[xy])
                row.append(bits[xy]) #form a pixel row
            newbits.append(row[::-1]) #horizontal flip on the row

#x is column, y is row
#r is CHAR row

newbits = numpy.array(newbits)
newbytes = numpy.packbits(newbits)

newbytes.tofile("font\\font.bin")

Path("font\\noheader.bin").unlink()