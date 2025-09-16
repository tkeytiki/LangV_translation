
class Scenario:
    pointers = []
    new_pointers = [0x220]
    with open("gamefiles\\input\\SCEN.DAT", mode="rb") as origin:
        t = origin.read(4)
        while t != bytearray([0,0,0,0]):
            pointers.append(int.from_bytes(t, byteorder='little'))
            t = origin.read(4)
    num_scenarios = len(pointers)
    script_pointers = [0]*num_scenarios
    script_pointers[0] = 0x22f4

    def __init__(self, scenario_number):
        self.scenario_number = scenario_number
        self.addr = Scenario.pointers[scenario_number]
        self.script_pointer = Scenario.script_pointers[scenario_number]
        self.script_len = 0
        self.data_len = self.script_pointer - self.addr
        self.data = ""
        self.script = "" #named for brevity but includes all data PAST the script as well
        with open("gamefiles\\input\\SCEN.DAT", mode="rb") as origin:
            origin.seek(self.addr)
            if self.data_len > 0:
                self.data = origin.read(self.data_len)
                origin.seek(self.script_pointer)
                #if not final scenario
                if self.scenario_number < Scenario.num_scenarios - 1:
                    self.script = origin.read(Scenario.pointers[self.scenario_number + 1] - self.script_pointer)
                else:
                    self.script = origin.read()
            else:
                if self.scenario_number < Scenario.num_scenarios - 1:
                    self.data_len = Scenario.pointers[self.scenario_number +1] - Scenario.pointers[self.scenario_number]
                    self.data = origin.read()
                else:
                    self.data = origin.read()
                    self.data_len = len(self.data)

    def add_script(self, script):
        self.script = script
        self.script_len = len(script)

    def repoint_next(self):
        #if scenario is not final scenario
        if self.scenario_number < Scenario.num_scenarios - 1:
            #cut down trailing zeros
            script = self.script.hex().rstrip('0')
            if len(script) % 2 != 0:
                script += '0'  # add a 0 if it results in the final byte being split in half
            self.script = bytearray.fromhex(script)
            self.script_len = len(self.script)
            end_of_data = Scenario.new_pointers[self.scenario_number] + self.data_len + self.script_len
            #pad with zeroes to make sure the 16s place is 16
            new_end = ((end_of_data - 1) // 0x10 + 1) * 0x10
            for i in range(new_end - end_of_data):
                self.script.append(0)
            print(end_of_data)
            print(new_end)
            Scenario.new_pointers.append(new_end)

#scen1 = Scenario(0)
#scen2 = Scenario(1)
#print(f'scen1: {scen1.data}')
#scen1.repoint_next()
