import io
import sys
import numpy
from pathlib import Path

numpy.set_printoptions(threshold=sys.maxsize)

def create_font_extension():
    #Path("font\\fontextension.bin").unlink()

    #bullet character
    bullet = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                          ])
    bullet = numpy.packbits(bullet, axis=None)
    print(bullet)
    bullet.tofile("font\\fontextension.bin")
    #with open("font\\fontextension.bin", mode="wb") as f:

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
    image_width = 192
    useful_number = image_width * 12
    #2304 = 192 (image width) * 12 (character width)
    #16 = number of columns in the bmp
    '''
    for r in range(int(len(bits)/useful_number)):
        row = list()
        for x in range(16):
            char = list()
            for y in range(12):
                charrow = list()
                for xy in range(r*useful_number+x*12+y*image_width, r*useful_number+x*12+12+y*image_width):
                    #newbits.append(bits[xy])
                    charrow.append(bits[xy]) #add a pixel to a row of the char
                char.append(charrow[::-1]) #add a row of the char to the char, flipped horizontally
            row.append(char) #add the completed char to the char row
        newbits.append(row[::-1]) #flip row horizontally
    '''
    #x is column, y is row
    #r is CHAR row

    newbits = numpy.array(bits)
    #newbits = numpy.array(newbits)
    newbytes = numpy.packbits(newbits)

    newbytes.tofile("font\\font.bin")

    #Path("font\\noheader.bin").unlink()