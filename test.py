import time
import datetime
import RPi.GPIO as GPIO

# Initialization
wind_tick = 0   # Used to count the number of times the wind speed input is triggered
interval = 3    # Seconds to be waited between speed measurements


# Setup input GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Event to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH) 

def wind_trig(self):   # test is the pin number, in this case 17, passed by the callback function
    global wind_tick
    wind_tick += 1
    # print(wind_tick)

GPIO.add_event_callback(17, wind_trig) 

while True:
    time.sleep(interval)
    wind_speed = (wind_tick * 1.2) / interval
    wind_tick = 0
    print(wind_speed)