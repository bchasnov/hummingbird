import imu
import time

if __name__ == "__main__":
    imux = imu.IMU("/dev/ttyUSB0", True)
    imux.start()
    time.sleep(1)

    print imux.data

    imux.halt()
