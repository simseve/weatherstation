import time
import datetime
import RPi.GPIO as GPIO
from statistics import mean


class wind_speed():

    wind_tick = 0
    
    def __init__(self):
        # Initialization
        # self.wind_tick = 0   # Used to count the number of times the wind speed input is triggered
        self.interval = 3    # Seconds to be waited between speed measurements
        self.mov_avg = 8    # Every 24 second average
        self.ws_readings = []
        self.samples = 0

        # Setup input GPIO pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Event to detect wind (4 ticks per revolution)
        GPIO.add_event_detect(17, GPIO.BOTH) 
        GPIO.add_event_callback(17, self.wind_trig) 

    def wind_trig(self, pin):   # test is the pin number, in this case 17, passed by the callback function
        self.wind_tick += 1
        print(self.wind_tick)

    
    def run(self):
        while True:
            time.sleep(self.interval)
            self.wind_speed = (self.wind_tick * 1.2) / self.interval
            self.wind_tick = 0
            self.ws_readings.append(round(self.wind_speed, 2))
            self.samples +=1
            if len(self.ws_readings) == self.mov_avg: 
                self.avg_wind_speed = round(mean(self.ws_readings),2) # averaging over 8 sample of 3 second wind
                self.gust_speed = round(max(self.ws_readings),2)
                # print(self.ws_readings)
                self.ws_readings.pop(0)
                print(self.avg_wind_speed, self.gust_speed)
        

