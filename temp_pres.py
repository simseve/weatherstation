import board
import busio
import adafruit_bme280
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

while True:
    print("Temperature: {}, Pressure: {}, Altitude: {}".format(sensor.temperature, sensor.pressure, sensor.altitude))
    time.sleep(1)

