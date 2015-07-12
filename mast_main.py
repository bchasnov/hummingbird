from rcin import RCIn
import time
import imu

rc_input = RCIn('COM22', 9600, debug=True)

Ts = 1./100

class State:
    def __init__(self, imu_data):
        self.quaternion = imu_data['quat']
        self.theta = euler_from_quaternion(self.quaternion);
        self.inttheta = 0

    def update(self, x_ref, imu_data):
        pass

class ErrorIntegrator:
    """ integrator without Anti-Windup"""
    def __init__(self, start_val, time):
        self.value = start_val # the current value of the integrator
        self.prev_error = start_val # the previous error measurement
        self.prev_time = time # the last time we have a measurement for

    def update(self, error, time):
        Ts = time - self.prev_time
        self.prev_time = time
        self.value += Ts*1.0/2*(error+self.prev_error) # trapezoidal integration
        return self.value


class gains:
    kp = 1
    ki = 1

def setup():
    # initialize everything
    rc_input.start()
    imu = IMU("COM21")
    imu.start()

    while imu.data is None:
        pass

    x = State(imu.data)

    try:
        while True:
            loop(imu, x)
    except KeyboardInterrupt:
        shutdown()

def shutdown():
    print "Shutting down"
    rc_input.halt()


def updateState(x, x_ref, imu_data):
    """

    :param x: x.quaternion and x.theta and x.IntTheta
    :param imu_data:
    :return:
    """
    q_ref = x_ref.quaternion
    q_new = imu_data["quat"]

    angle

    euler_angles = euler_from_quaternion(q_new)
    x.theta = euler_angles[0]

    q_error = quaternion_multiply(q_ref, quaternion_conjugate(q_new))
    euler_angles_error = euler_from_quaternion(q_error)

    x.inttheta = x(x.inttheta + euler_angles_error[0]) /Ts / 2.0

    return x

def controlTheta(x, x_ref):
    global gains
    u = gains.kp * (x.theta - x_ref.theta) + gains.ki * x.inttheta

    return u

def loop(imu):
    global x
    tic = time.time()

    #get RC inputs
    print rc_input.data
    
    #get IMU

    #compute outputs


    #determine failsafe
        #throttle failsafe


    #if failsafe
            #override outputs
    #perform outputs

    toc = time.time()
    tictoc = toc-tic
    if tictoc > Ts:
        print tictoc, "Frame took too long"
            
    #wait for next frame
    while(time.time() - tic < Ts):
        pass
	
if __name__ == '__main__':
    setup()