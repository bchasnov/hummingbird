import imu
import time
from quat import *




if __name__ == "__main__":
    imux = imu.IMU("/dev/ttyUSB0", True)
    imux.start()
    time.sleep(1)

    try:
        while imux.data is None:
            pass
        qref = imux.data['quat'] 
        print 'qref: ',qref  
    except(KeyboardInterrupt):
	imux.halt()
    try:
        f = open('qref.conf','w')
        f.write('qref = '+str(qref))
        f.close()
    except:
        pass

    imux.halt()





