# servoboard.py
# Managers a servo board controlled via serial. Includes a ESC initialization sequence
# to ensure ESC doesn't enter calibration mode. Includes a watchdog thread that resets
# servos if no change in value is written for a set timeout

import serial
import threading
import time


class ServoBoard:
    def __init__(self, port_name, baud_rate, num_servos, watchdog_timeout, debug=False):
        # Debug Output Switch
        self.debug = debug

        # Port Setup
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.port = serial.Serial(self.port_name, self.baud_rate, timeout=None)

        # Servo value array
        self.num_servos = num_servos
        self.servo_vals = [0.0]*self.num_servos

        # Shutdown Signal
        self.stop = threading.Event()

        # ESC initialization stuff
        self.init_esc_thread = threading.Thread(target=self.init_esc)
        self.esc_init_timeout = 1.0  # seconds
        self.esc_initialized = threading.Event()

        # Watchdog stuff
        self.watchdog_thread = threading.Thread(target=self.watchdog)
        self.watchdog_timeout = watchdog_timeout
        self.wrote_value = threading.Event()

        # Start helper threads
        self.init_esc_thread.start()
        self.watchdog_thread.start()

    def push(self):
        """
        Push stored servo values to the servos over the serial port
        :return: None
        """
        self.esc_initialized.wait()

        self.wrote_value.set()  # tell the watchdog a value has been written

        command = "sa" + " ".join([str(int(1000*a)) for a in self.servo_vals]) + "\n"
        self.port.write(command)

    def init_esc(self):
        self.port.write("sa")
        time.sleep(self.esc_init_timeout)
        self.esc_initialized.set()

    def watchdog(self):
        while not self.stop.is_set():
            if not self.wrote_value.wait(self, self.watchdog_timeout):
                if self.debug:
                    print "ServoBoard Watchdog: No value written for a while, resetting servos."
                self.port.write("sa")




