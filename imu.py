import serial
import threading


class IMU(threading.Thread):
    def __init__(self, port_name, debug=False):
        # Debug Output Switch
        self.debug = debug

        # Port Setup
        self.port_name = port_name

        self.port = serial.Serial(self.port_name, 115200, timeout=None)
        self.port.write("$VNWRG,05,460800*XX\n")
        self.port.close()
        self.port = serial.Serial(self.port_name, 460800, timeout=None)
        self.port.write("$VNWRG,06,8*XX\n")
        self.port.write("$VNWRG,07,200*XX\n")

        # Status Flags
        self.connected = False
        self.stop = threading.Event()

        # IMU Data
        self.data = None

        super(IMU, self).__init__()

    def run(self):
        """
        Override Thread.run(), called when self.start() is called
        :return: None
        """
        while not self.stop.isSet():
            data = self.port.readline()
            if data:
                self.handleData(data)

    def halt(self):
        """
        Called from main loop upon shutdown, giving the thread a chance to cleanly exit
        :return: None
        """
        self.stop.set()
        self.port.close()
        self.join()

    def handleData(self, data):
        """
        Updates self.data with the latest values from the Serial Port.
        :param data: Bytes of one line read in from the Serial Port
        :return: None
        """
        # Try getting self.num_inputs values as floats
        try:
            if data[-1] != '\n' or data[0] != '$':
                return
            data = data.rstrip().split(",")
            if data[0] != "$VNQMR":
                if self.debug:
                    print data
                return
            data = data[1:]
            data[-1] = data[-1].split("*")[0]
            data = map(float, data)
            if len(data) != 13:
                return
            d = {
                    "quat0": data[0],
                    "quat1": data[1],
                    "quat2": data[2],
                    "quat3": data[3],
                    "magx": data[4],
                    "magy": data[5],
                    "magx": data[6],
                    "accelx": data[7],
                    "accely": data[8],
                    "accelx": data[9],
                    "gyrox": data[10],
                    "gyroy": data[11],
                    "gyrox": data[12],
                    }
            self.data = d
        except IndexError:
            if self.debug:
                print "RCIn: Couldn't read", self.num_inputs, "values"
        except ValueError:
            if self.debug:
                print "RCIn: Couldn't parse values into floats"








