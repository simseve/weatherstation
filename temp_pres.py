import board
import busio
import adafruit_bme280
import time

class get_temp_pres():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, address=0x76)

    def get_bme280(self):
        return self.sensor.temperature, self.sensor.pressure, self.sensor.altitude, self.sensor.humidity

    

