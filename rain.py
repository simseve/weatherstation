import datetime
import time
import RPi.GPIO as GPIO

rain_tick = 0     # Used to count the number of times the wind speed input is triggered
interval = 3      # Seconds to be waited between speed measurements
rain_count = 240  # Measure rain over 1 hour - 240
midnight_rain = 0
r_readings = []
count_moving_avg = 0
rain_fall = 0
daily_rain = 0
midnight_rain = 0


GPIO.setmode(GPIO.BCM)
#For rain use pin GPIO23
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Event to detect wind (2 ticks per revolution)
GPIO.add_event_detect(17, GPIO.FALLING) 

def rain_trig(self):
    global rain_tick
    rain_tick += 1

def hours_from_midnight(current_time):
    midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    hours = (current_time - midnight).seconds // 3600
    return int(hours)
 
GPIO.add_event_callback(17, rain_trig)  

try:
    while True:
        now = datetime.datetime.now()
        time.sleep(interval)
        count_moving_avg +=1
        from_midnight = hours_from_midnight(now)
        print("Hourly rain is {:.2f}mm, Daily rain is {:.2f}mm, Rain from Midnight {:.2f}mm".format(rain_fall, daily_rain, midnight_rain))
        
        # Accumulated rain over previous (interval * rain_count)  seconds
        if count_moving_avg == rain_count: # It enters here every hour
            rain_fall = rain_tick * 0.2794
            r_readings.append(round(rain_fall,2))
            rain_tick = 0
            count_moving_avg = 0
            daily_rain = sum(r_readings)
            if len(r_readings) == 24:
                r_readings.pop(0)
            if len(r_readings) >= from_midnight:
                slice_obj = slice(-from_midnight, None)
                midnight_rain = sum(r_readings[slice_obj])


except KeyboardInterrupt:
    print("interrupted")
    GPIO.cleanup()
GPIO.cleanup()
