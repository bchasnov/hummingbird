__author__ = 'appi'

import time
from servoboard import ServoBoard
from controloutput import ControlOutput


servoboard = ServoBoard('/dev/ttyAMA0', 9600, 8, 1, debug=True)
throttle = ControlOutput(servoboard, 7)

for i in range(10):
    throttle.set(0.0)
    servoboard.push()

    time.sleep(0.2)

    throttle.set(1.0)
    servoboard.push()

    time.sleep(0.2)

time.sleep(3)

servoboard.halt()
