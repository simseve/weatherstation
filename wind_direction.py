#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wind_direction.py
#  
#  Copyright 2020  <Simone Severini>
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
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class wind_direction():
    def __init__(self):

        # create i2c bus
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.gain = 1

    def get_wind_dir(self):
        # Calculate wind direction based on ADC reading
        self.chan = AnalogIn(self.ads, ADS.P0)
        self.val = self.chan.value
        self.windDir = "Not Connected"
        self.windDeg = 999

        if 20000 <= self.val <= 20500:
            self.windDir = "N"
            self.windDeg = 0

        if 10000 <= self.val <= 10500:
            self.windDir = "NNE"
            self.windDeg = 22.5

        if 11500 <= self.val <= 12000:
            self.windDir = "NE"
            self.windDeg = 45

        if 2000 <= self.val <= 2250:
            self.windDir = "ENE"
            self.windDeg = 67.5

        if 2300 <= self.val <= 2500:
            self.windDir = "E"
            self.windDeg = 90

        if 1500 <= self.val <= 1950:
            self.windDir = "ESE"
            self.windDeg = 112.5

        if 4500 <= self.val <= 4900:
            self.windDir = "SE"
            self.windDeg = 135

        if 3000 <= self.val <= 3500:
            self.windDir = "SSE"
            self.windDeg = 157.5

        if 7000 <= self.val <= 7500:
            self.windDir = "S"
            self.windDeg = 180

        if 6000 <= self.val <= 6500:
            self.windDir = "SSW"
            self.windDeg = 202.5

        if 16000 <= self.val <= 16500:
            self.windDir = "SW"
            self.windDeg = 225

        if 15000 <= self.val <= 15500:
            self.windDir = "WSW"
            self.windDeg = 247.5

        if 24000 <= self.val <= 24500:
            self.windDir = "W"
            self.windDeg = 270

        if 21000 <= self.val <= 21500:
            self.windDir = "WNW"
            self.windDeg = 292.5

        if 22500 <= self.val <= 23000:
            self.windDir = "NW"
            self.windDeg = 315

        if 17500 <= self.val <= 18500:
            self.windDir = "NNW"
            self.windDeg = 337.5

        return self.windDir, self.windDeg


