import re
from serial import Serial

HOME="G28"
ABSOLUTE_POS="G90"
RELATIVE_POS="G91"
FLOWRATE_BASE="M221 S"  #flowrate percentage
FEEDRATE_BASE="M203 E"  #max feedrate

GET_TEMP="M105"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print("X: " + str(self.x) + "\tY: " + str(self.y))


class Printer:
    def __init__(self, port, baudrate):
        self.ser = Serial(port, baudrate)

    def write(self, data):
        self.ser.write(str(data+'\r\n').encode('utf-8'))

    def read(self):
        stop = False
        while not stop:
            data = self.ser.readline().decode('utf-8')
            if data == "ok\n":
                stop = True
            elif data[:2] == "ok": #used to read format of type "ok T:24.34 /0.00 B:24.22 /0.00 @:0 B@:0 " returned from M105
                stop = True
                return data[2:]
            else:
                print(data)
        print("END OF READ")

    def home(self):
        self.write(HOME)

    def move_x(self, pos):
        self.write(RELATIVE_POS)
        move = "G0 X"+str(pos)
        self.write(move)

    def move_y(self, pos):
        self.write(RELATIVE_POS)
        move = "G0 Y"+str(pos)
        self.write(move)

    def move_z(self, pos):
        self.write(RELATIVE_POS)
        move = "G0 Z"+str(pos)
        self.write(move)
    
    def move_x_absolute(self, pos):
        self.write(ABSOLUTE_POS)
        move = "G1 X"+str(pos)
        self.write(move)

    def move_y_absolute(self, pos):
        self.write(ABSOLUTE_POS)
        move = "G1 Y"+str(pos)
        self.write(move)

    def move_z_absolute(self, pos):
        self.write(ABSOLUTE_POS)
        move = "G1 Z"+str(pos)
        self.write(move)

    def move_extruder(self, pos):
        self.write(RELATIVE_POS)
        move = "G0 E"+str(pos)
        self.write(move)
    
    def set_nozzle_temp(self, pos):
        temperature = "M104 S"+str(pos)
        self.write(temperature)

    def set_bed_temp(self, pos):
        temperature = "M140 S"+str(pos)
        self.write(temperature)

    def set_feedrate(self, pos):
        feedrate = FEEDRATE_BASE+str(pos)
        self.write(feedrate)

    def get_temp(self):
        try:
            self.write(GET_TEMP)
            data = self.read()
            nozzle_temp = re.search(r'T:\d+.\d+', data).group(0)[2:]                                                            
            bed_temp = re.search(r'B:\d+.\d+', data).group(0)[2:]
        except TypeError:
            nozzle_temp = 0
            bed_temp = 0
        return (nozzle_temp, bed_temp)

    def get_pos(self):
        self.write('M114')
        self.read()

        

if __name__ == "__main__":
    printer = Printer("/dev/ttyUSB0", 250000)
    while True:
        cmd = input().upper()
        if cmd[0] == 'X':
            printer.move_x(cmd[1:])

        elif  cmd[0] == 'Y':
            printer.move_y(cmd[1:])

        elif  cmd[0] == 'Z':
            printer.move_z(cmd[1:])

        if cmd  == "READ":
            printer.write("M503")
            printer.read()
        elif cmd == "M114":
            printer.get_pos()
        else:
            printer.write(cmd)
