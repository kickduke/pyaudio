#!/usr/bin/python3
import time

runnable = 1
FRAMERATE = 60
frame_period = 1.0/FRAMERATE
while(runnable != 0) :
    start_time = time.time()
    pass
    end_time = time.time()
    sleep_time = frame_period - (end_time - start_time)
    print(frame_period)
    if(sleep_time > 0) :
        time.sleep(sleep_time)
        
    
