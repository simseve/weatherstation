import time
import datetime
import RPi.GPIO as GPIO
from statistics import mean

# Initialization
wind_tick = 0   # Used to count the number of times the wind speed input is triggered
interval = 3    # Seconds to be waited between speed measurements
mov_avg = 8    # Every 24 second average
ws_readings = []
samples = 0

# Setup input GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Event to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH) 

def wind_trig(self):
    global wind_tick
    wind_tick += 1
 
GPIO.add_event_callback(17, wind_trig)  

try:
    while True:
        time.sleep(interval)
        wind_speed = (wind_tick * 1.2) / interval
        wind_tick = 0
        ws_readings.append(round(wind_speed, 2))
        samples +=1
        if len(ws_readings) == mov_avg: 
            avg_wind_speed = mean(ws_readings) # averaging over 8 sample of 3 second wind
            gust_speed = max(ws_readings)
            print(ws_readings)
            ws_readings.pop(0)
            print("Average Wind Speed: {:.2f} km/h and Wind Gust {}".format(round(avg_wind_speed, 2), round(gust_speed, 2)))
            #TODO: Tx with Direwolf
            
except KeyboardInterrupt:
    print("interrupted")
    GPIO.cleanup()

