import temp_pres
import wind_direction
import wind_speed
import rain


# Read Wind Spedd
# anemometer = wind_speed.wind_speed()
# anemometer.run()

# Read Wind Direction
direction = wind_direction.wind_direction()
w_dir, w_deg = direction.get_wind_dir()
print(w_dir, w_deg)

# Read Temperature, Pressure, Barometric Altitude
t_p = temp_pres.get_temp_pres()
temp, press, alt, hum = t_p.get_bme280() 
print(temp, press, alt, hum)

#Read Rain
# rain = rain.get_rain()
# rain.run()


