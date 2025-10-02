class Block:

    def __init__(self):
        self.offsets = [bytearray(2)]
        self.lines = ""
        self.offset_table_len = 2
        self.lines_len = 0

    def add_offset(self, offset):
        self.offsets.append(offset)

    def add_line(self, line):
        self.lines_len += len(line)//2
        print(self.lines_len)
        self.lines += line
        ll = self.lines_len//2 #divide offset by two because for some reason system pointers are multiplied
        #by 2 to get the real offset
        self.add_offset(ll.to_bytes(length=2,byteorder="little"))
        self.offset_table_len += 2

    def print(self):
        print(f"Lines Length: {hex(self.lines_len)}")
        print(f"Offsets Length: {hex(self.offset_table_len)}")
        print(f"Offsets: {self.offsets}")
        print(f"Lines: {self.lines}")