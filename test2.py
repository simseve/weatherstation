#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import time, math

dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 17
pulse = 0
start_timer = time.perf_counter()
speed = 0


def init_GPIO():					# initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def calculate_elapse(channel):				# callback function
    global pulse, start_timer, elapse, speed
    pulse += 1								# increase pulse by 1 whenever interrupt occurred
    if pulse == 4:        
        elapse = time.perf_counter() - start_timer		# elapse for every 1 complete rotation made!
        print(elapse)
        start_timer = time.perf_counter()				# let current time equals to start_timer
        print(start_timer)
        speed = pulse * 2.4 / elapse
        pulse = 0



# def calculate_speed():
#     global pulse,elapse,rpm,dist_km,dist_meas,km_per_sec,km_per_hour
#     if elapse !=0:							# to avoid DivisionByZero error
#         rpm = 1/elapse * 60
#     # return km_per_hour


def init_interrupt():
    GPIO.add_event_detect(sensor, GPIO.BOTH, callback = calculate_elapse, bouncetime = 20)


if __name__ == '__main__':
    init_GPIO()
    init_interrupt()

while True:
    print("Current speed is {} km/h".format(speed))
	# calculate_speed()	# call this function with wheel radius as parameter
	# print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(rpm,km_per_hour,dist_meas,pulse))
    sleep(0.1)