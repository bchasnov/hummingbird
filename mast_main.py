import serial
import threading
import time

rc_in_connected = False
rc_in_port_name = 'COM22'
baud = 9600

rc_in_port = serial.Serial(rc_in_port_name, baud, timeout=0)
rc_in_port_stop = False

def handle_rc_in(data):
    data_split = data.split(',')
    data_float = map(float,data_split)
    for i in range(int(data_float[0])):
        rc_vals[i] = data_float[i+1]
    rc_in_port_stop = True


def read_rc_port(ser):
    while not rc_in_port_stop:
       reading = ser.readline()
       if reading:
           handle_rc_in(reading)


rc_inputs_n = 8;
rc_vals = [0.0]*rc_inputs_n
rc_in_thread = threading.Thread(target=read_rc_port, args=(rc_in_port,))


Ts = 1/100;


def setup():
    rc_in_thread.start()
    #imu_in_thread.start()

    try:
        while True:
            loop()
    except(KeyboardInterrupt):
        shutdown()

def shutdown():
    print "Shutting down"
    
    rc_in_port_stop = True
    rc_in_port.close()
    
    #imu_in_thread.stop();


def loop():
    tic = time.time()

    #get RC inputs
    print rc_vals
    
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
            pass
            #took too long!
            
    #wait for next frame
    while(time.time()-tic < Ts):
        pass
	
