from rcin import RCIn
import time
from imu import IMU
from servoboard import ServoBoard
from controloutput import ControlOutput
from transformations import *

rc_input = RCIn('COM22', 9600, debug=True)
imu = IMU("COM21", debug=True)

servoboard = ServoBoard('ttyAMA0', 9600, 8, 0.5, debug=True)
throttle = ControlOutput(servoboard, 0)


class Gains:
    def __init__(self):
        self.kp = 1
        self.ki = 1

gains = Gains()

Ts = 1./100

class State:
    def __init__(self, imu_data):
        self.quaternion = imu_data['quat']
        #self.theta = euler_from_quaternion(self.quaternion);
        self.IntThetaError = ErrorIntegrator(0) # TODO

    def update(self, x_ref, imu_data):
        pass

class ErrorIntegrator:
    """ integrator without Anti-Windup"""
    global Ts

    def __init__(self, start_val):
        self.value = start_val # the current value of the integrator
        self.prev_error = start_val # the previous error measurement

    def update(self, error):
        self.value += Ts*1.0/2*(error+self.prev_error) # trapezoidal integration
        return self.value


def setup():
    # initialize everything
    rc_input.start()
    imu.start()

    while imu.data is None:
        pass

    x = State(imu.data) # Quaternions, -> Theta, IntTheta

    try:
        while True:
            x = loop(x)
    except KeyboardInterrupt:
        shutdown()


def shutdown():
    print "Shutting down"
    rc_input.halt()
    imu.halt()


def updateState(x, x_ref, imu_data):
    """
    :param x: x.quaternion and x.theta and x.IntTheta
    :param imu_data:
    :return:
    """
    q_ref = x_ref.quaternion
    q_new = imu_data["quat"]

    euler_angles = euler_from_quaternion(q_new)
    x.theta = euler_angles[0]

    q_error = quaternion_multiply(q_ref, quaternion_conjugate(q_new))
    euler_angles_error = euler_from_quaternion(q_error)
    x.theta_error = euler_angles_error[0]

    x.State.IntThetaError.update(x.theta_error)

    return x


def computeOutputs(x):
    global gains


    u = gains.kp * x.theta_error + gains.ki * x.IntThetaError
    if u < 0:
        u = 0
    elif u > 1:
        u = 1

    return u


def loop(x):
    global imu, rc_input
    tic = time.time()
    #get RC inputs
    print rc_input.data
    
    #get IMU
    print imu.data

    #compute outputs
    q_ref = [1, 0, 0, 0]
    x = updateState(x, q_ref, imu.data)
    throttle = computeOutputs(x)


    #perform failsafe
    if rc_input.data[5] == -1.0:
        throttle = 0

    #perform outputs

    servoboard.push()
    toc = time.time()


    tictoc = toc-tic
    if tictoc > Ts:
        print tictoc, "Frame took too long"
            
    #wait for next frame
    while(time.time() - tic < Ts):
        pass

    return x
if __name__ == '__main__':
    setup()