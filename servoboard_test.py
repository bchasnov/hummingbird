__author__ = 'appi'

import time
from servoboard import ServoBoard
from controloutput import ControlOutput


servoboard = ServoBoard('/dev/ttyAMA0', 9600, 8, 0.5, debug=True)
throttle = ControlOutput(servoboard, 7)

throttle = 0.0
servoboard.push()

time.sleep(1)

throttle = 0.5
servoboard.push()

time.sleep(1)

throttle = 0.0
servoboard.push()

time.sleep(1)

throttle = 1.0
servoboard.push()

time.sleep(1)