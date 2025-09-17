import io
import sys
import numpy
from pathlib import Path

numpy.set_printoptions(threshold=sys.maxsize)

def format_bmp():
    bytes = []

    with open("font\\psx6x12dualtry.bmp", mode="rb") as i:
        i.seek(0x0A) #offset that contains start addr of pixel array
        offset = i.read(1)[0]
        i.seek(offset)
        with open("font\\noheader.bin", mode="wb") as o:
            o.write(i.read())

    bytes = numpy.fromfile("font\\noheader.bin", dtype="uint8")

    #bmp image data is stored upside down, have to flip it rightside up

    bits = numpy.unpackbits(bytes)[::-1] #flips over both axes

    newbits = list()

    #2304 = 192 (image width) * 12 (character width)
    #16 = number of columns in the bmp
    for r in range(int(len(bits)/2304)):
        row = list()
        for x in range(16):
            char = list()
            for y in range(12):
                charrow = list()
                for xy in range(r*2304+x*12+y*192, r*2304+x*12+12+y*192):
                    #newbits.append(bits[xy])
                    charrow.append(bits[xy]) #add a pixel to a row of the char
                char.append(charrow[::-1]) #add a row of the char to the char, flipped horizontally
            row.append(char) #add the completed char to the char row
        newbits.append(row[::-1]) #flip row horizontally

    #x is column, y is row
    #r is CHAR row

    newbits = numpy.array(newbits)
    newbytes = numpy.packbits(newbits)

    newbytes.tofile("font\\font.bin")

    Path("font\\noheader.bin").unlink()