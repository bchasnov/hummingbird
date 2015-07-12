__author__ = 'Apoorva Sharma'

# rcin.py
# Basic class to receive RC input at a fixed sampling rate over a serial port
# Interface for sensor input classes.

import serial
import threading


class RCIn(threading.Thread):
    def __init__(self, port_name, baud_rate, debug=False):
        # Debug Output Switch
        self.debug = debug

        # Port Setup
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.port = serial.Serial(self.port_name, self.baud_rate, timeout=.5)

        # Status Flags
        self.connected = False
        self.stop = threading.Event()


        # RC Data
        self.num_inputs = 8
        self.data = [0.0]*self.num_inputs

        # Calibration constants
        self.scales = [1024, 512, 512, 512, 512, 1024, 512, 512]
        self.offsets = [990, 1500, 1500, 1500, 1500, 990, 1500, 1500, 1500]
        self.switches = [4]

        super(RCIn, self).__init__()

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
            data_float = map(float, data.split(','))
            self.data = self.processData(data_float)
        except IndexError:
            if self.debug:
                print "RCIn: Couldn't read", self.num_inputs, "values"
        except ValueError:
            if self.debug:
                print "RCIn: Couldn't parse values into floats"


    def processData(self, data_float):
        """
        Scales the analog data and clips the switches
        :param data_float:
        :return:
        """

        data = [0]*self.num_inputs

        for i in range(self.num_inputs):
            data[i] = (data_float[ i + 1]-self.offsets[i])/self.scales[i]

        for key in self.switches:
            data[key] = round(data[key])

        saturate = lambda x: max(min(1.0,x),-1.0)
        data = map(saturate, data)

        return data
