import datetime
import time
import RPi.GPIO as GPIO

class get_rain():

    def __init__(self):
        self.rain_tick = 0     # Used to count the number of times the wind speed input is triggered
        self.interval = 3      # Seconds to be waited between speed measurements
        self.rain_count = 240  # Measure rain over 1 hour - 240
        self.midnight_rain = 0
        self.r_readings = []
        self.count_moving_avg = 0
        self.rain_fall = 0
        self.daily_rain = 0
        self.midnight_rain = 0

        GPIO.setmode(GPIO.BCM)

        #For rain use pin GPIO23
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Event to detect wind (2 ticks per revolution)
        GPIO.add_event_detect(17, GPIO.FALLING) 
        GPIO.add_event_callback(17, self.rain_trig)  

    def rain_trig(self, pin):
        global rain_tick
        self.rain_tick += 1

    def hours_from_midnight(self, current_time):
        self.current_time = current_time
        self.midnight = self.current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        self.hours = (self.current_time - self.midnight).seconds // 3600
        return int(self.hours)

    def run(self):
        while True:
            self.now = datetime.datetime.now()
            time.sleep(self.interval)
            self.count_moving_avg +=1
            self.from_midnight = self.hours_from_midnight(self.now)
            
            # Accumulated rain over previous (interval * rain_count)  seconds
            if self.count_moving_avg == self.rain_count: # It enters here every hour
                self.rain_fall = self.rain_tick * 0.2794
                self.r_readings.append(round(self.rain_fall,2))
                self.rain_tick = 0
                self.count_moving_avg = 0
                self.daily_rain = sum(self.r_readings)
                if len(self.r_readings) == 24:
                    self.r_readings.pop(0)
                if len(self.r_readings) >= self.from_midnight:
                    self.slice_obj = slice(-self.from_midnight, None)
                    self.midnight_rain = sum(self.r_readings[self.slice_obj])
                    print("Hourly rain is {:.2f}mm, Daily rain is {:.2f}mm, Rain from Midnight {:.2f}mm".format(self.rain_fall, self.daily_rain, self.midnight_rain))



