from rcin import RCIn
import time

rc_input = RCIn('COM22', 9600, debug=True)

Ts = 1/100


def setup():
    # initialize everything
    rc_input.start()

    try:
        while True:
            loop()
    except KeyboardInterrupt:
        shutdown()

def shutdown():
    print "Shutting down"
    rc_input.shutdown()


def loop():
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
        pass
        #took too long!
            
    #wait for next frame
    while(time.time()-tic < Ts):
        pass
	
