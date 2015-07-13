import imu
import time
from quat import *


first = True
qref = [1,0,0,0]

def process(q):
    global first, qref

    if first:
	qref = q
        first = False


    return euler_from_quaternion(quaternion_multiply(q,quaternion_conjugate(qref)))



if __name__ == "__main__":
    imux = imu.IMU("/dev/ttyUSB0", True)
    imux.start()
    time.sleep(1)

    try:
        while True:
            print process(imux.data['quat'])
            time.sleep(1/100)
    except(KeyboardInterrupt):
	imux.halt()





