#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2020  <Simone Severini HB9HCM
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import time
import datetime
import RPi.GPIO as GPIO
from statistics import mean

# Initialization
wind_tick = 0   # Used to count the number of times the wind speed input is triggered
rain_tick = 0     # Used to count the number of times the wind speed input is triggered
interval = 3    # Seconds to be waited between speed measurements
mov_avg = 8    # Every 24 second average
ws_readings = []
samples = 0
rain_count = 240  # Measure rain over 1 hour - 240
midnight_rain = 0
r_readings = []
count_moving_avg = 0
rain_fall = 0
daily_rain = 0
midnight_rain = 0

# Setup input GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Event to detect wind (4 ticks per revolution)
GPIO.add_event_detect(17, GPIO.BOTH) 

#For rain use pin GPIO23
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Event to detect rain reed switch
GPIO.add_event_detect(17, GPIO.FALLING) 

def wind_trig(self):
    global wind_tick
    wind_tick += 1
 
GPIO.add_event_callback(17, wind_trig)  

def rain_trig(self):
    global rain_tick
    rain_tick += 1

def hours_from_midnight(current_time):
    midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    hours = (current_time - midnight).seconds // 3600
    return int(hours)
 
GPIO.add_event_callback(17, rain_trig)  

def get_wind_speed():
    time.sleep(interval)
    wind_speed = (wind_tick * 1.2) / interval
    wind_tick = 0
    ws_readings.append(round(wind_speed, 2))
    samples +=1
    if len(ws_readings) == mov_avg: 
        avg_wind_speed = round(mean(ws_readings), 2) # averaging over 8 sample of 3 second wind
        gust_speed = round(max(ws_readings), 2)
        ws_readings.pop(0)
        print("Average Wind Speed: {:.2f} km/h and Wind Gust {}".format(round(avg_wind_speed, 2), round(gust_speed, 2)))
    return avg_wind_speed, gust_speed

def get_rain(): 
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
    return rain_fall, daily_rain, midnight_rain

if __name__ == '__main__':
    get_wind_speed()
    get_rain()
    
    
