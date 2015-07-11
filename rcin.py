__author__ = 'Apoorva Sharma'

# rcin.py
# Basic class to receive RC input at a fixed sampling rate over a serial port
# Interface for sensor input classes.

import serial
import threading

class RCIn(threading.Thread):
    def __init__(self, port_name, baud_rate, debug=False):
        super(RCIn, self).__init__()
        # Debug Output Switch
        self.debug = debug

        # Port Setup
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.port = serial.Serial(self.port_name, self.baud_rate, timeout=0)

        # Status Flags
        self.connected = False
        self.stop = False

        # RC Data
        self.num_inputs = 8
        self.data = [0.0]*self.num_inputs

    def run(self):
        """
        Override Thread.run(), called when self.start() is called
        :return: None
        """
        while not self.stop:
            data = self.port.readline()
            if data:
                self.handleData(data)


    def handleData(self, data):
        """
        Updates self.data with the latest values from the Serial Port.
        :param data: Bytes of one line read in from the Serial Port
        :return: None
        """
        # Try getting self.num_inputs values as floats
        try:
            data_float = map(float, data.split(','))
            self.data = data_float[1:self.num_inputs+1]
        except IndexError:
            if self.debug:
                print "RCIn: Couldn't read", self.num_inputs, "values"
        except ValueError:
            if self.debug:
                print "RCIn: Couldn't parse values into floats"

    def shutdown(self):
        """
        Called from main loop upon shutdown, giving the thread a chance to cleanly exit
        :return: None
        """
        self.stop = True
        self.port.close()







