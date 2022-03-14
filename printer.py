
from serial import Serial

HOME="G28"

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
            else:
                print(data)
        print("END OF READ")

    def home(self):
        self.write(HOME)

    def move_x(self, pos):
        self.write('G91')
        move = "G0 X"+str(pos)
        self.write(move)

    def move_y(self, pos):
        self.write('G91')
        move = "G0 Y"+str(pos)
        self.write(move)

    def move_z(self, pos):
        self.write('G91')
        move = "G0 Z"+str(pos)
        self.write(move)
    
    def move_x_absolute(self, pos):
        self.write('G90')
        move = "G1 X"+str(pos)
        self.write(move)

    def move_y_absolute(self, pos):
        self.write('G90')
        move = "G1 Y"+str(pos)
        self.write(move)

    def move_z_absolute(self, pos):
        self.write('G90')
        move = "G1 Z"+str(pos)
        self.write(move)
    
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
