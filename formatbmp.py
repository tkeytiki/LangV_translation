import io
import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

 #with open("C:\\Users\\whopo\\Downloads\\font.bin", mode="rb") as i,\
 #       open("C:\\Users\\whopo\\Downloads\\fonttest.bin", mode="wb") as o:
 #   inputbits = struct.unpack("@x", i.read())
#    print(inputbits)



bytes = numpy.fromfile("C:\\Users\\whopo\\Downloads\\psx6x12dualtryflipnoheader", dtype="uint8")

testy = numpy.fromfile("C:\\Users\\whopo\\Downloads\\psx6x12dualtryflip.bmp", dtype="uint8")
tbits = numpy.unpackbits(testy)
val = ""
for x in range(0xA*8, 0xB*8):

#bytes = numpy.flip(bytes, axis=None)
#print(bytes)
bits = numpy.unpackbits(bytes)
#print(bits)
#bits = numpy.flip(bits, axis=None)
#print(bits)
#bitstranspose = list()
#for x in range(int(len(bits)/2304)):
#    t = bits[x*2304:x*2304+2304]
#    #print(t)
#    numpy.flip(t, axis=None)
#    tp = numpy.packbits(t)
#    tp.tofile("C:\\Users\\whopo\\Downloads\\fliptest.bin")
    #print(t)
#    bitstranspose.append(t)
#bitstranspose = numpy.asarray(bitstranspose, dtype="uint8")
#bitstranspose = bitstranspose.flatten(order="C")
#print(bitstranspose)
#print(len(bitstranspose))
#bits = bitstranspose

newbits = list()

for r in range(int(len(bits)/2304)):
    #print(r)
    for x in range(16):
        for y in range(12):
            #print(bits[(192+x*192):(12+192+x*192)])
            for xy in range(r*2304+x*12+y*192, r*2304+x*12+12+y*192):
                newbits.append(bits[xy])
            #for xy in range(r*2304+x*12+12+y*192, r*2304+x*12+y*192, -1):
             #   print(bits[xy])
              #  newbits.append(bits[xy])
#x is column, y is row
#r is CHAR row
newbits = numpy.array(newbits)
#print(newbits)
newbytes = numpy.packbits(newbits)

newbytes.tofile("C:\\Users\\whopo\\Downloads\\fonttest.bin")