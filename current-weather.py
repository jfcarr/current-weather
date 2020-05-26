#!/usr/bin/python3

import argparse
import math
import requests
import xml.etree.ElementTree as ET

class CurrentWeather:
	def __init__(self, location_code):
		self.location_code = location_code

	def get_current_weather(self):
		r = requests.get(f'https://w1.weather.gov/xml/current_obs/{self.location_code}.xml')
		self.weather_info = r.text

		return self.weather_info

	def get_element(self, element_name):
		try:
			root = ET.fromstring(self.weather_info)
			element_data = root.find(element_name)
			return element_data.text
		except:
			return "N/A"

	def get_feels_like_temp(self):
		temperature = float(self.get_element('temp_f'))
		wind_speed = float(self.get_element('wind_mph'))
		relative_humidity = float(self.get_element('relative_humidity'))

		# Try Wind Chill first
		if temperature <= 50 and wind_speed >= 3:
			feels_like = 35.74 + (0.6215*temperature) - 35.75*(wind_speed**0.16) + ((0.4275*temperature)*(wind_speed**0.16))
		else:
			feels_like = temperature
		
		# Replace it with the Heat Index, if necessary
		if feels_like == temperature and temperature >= 80:
			feels_like = 0.5 * (temperature + 61.0 + ((temperature-68.0)*1.2) + (relative_humidity*0.094))
		
			if feels_like >= 80:
				feels_like = -42.379 + 2.04901523*temperature + 10.14333127*relative_humidity - .22475541*temperature*relative_humidity - .00683783*temperature*temperature - .05481717*relative_humidity*relative_humidity + .00122874*temperature*temperature*relative_humidity + .00085282*temperature*relative_humidity*relative_humidity - .00000199*temperature*temperature*relative_humidity*relative_humidity
				if relative_humidity < 13 and temperature >= 80 and temperature <= 112:
					feels_like = feels_like - ((13-relative_humidity)/4)*math.sqrt((17-math.fabs(temperature-95.))/17)
					if relative_humidity > 85 and temperature >= 80 and temperature <= 87:
						feels_like = feels_like + ((relative_humidity-85)/10) * ((87-temperature)/5)

		return round(feels_like,1)

parser = argparse.ArgumentParser()
parser.add_argument("location_code", help="Location code, e.g., 'KDAY'")
args = parser.parse_args()

cw = CurrentWeather(args.location_code)

cw.get_current_weather()

current_temperature = float(cw.get_element('temp_f'))
feels_like = cw.get_feels_like_temp()

feels_like_string = "" if current_temperature == feels_like else f" (feels like {feels_like} F)"

print(f"{cw.get_element('weather')}, {cw.get_element('temp_f')} F{feels_like_string}\nWind: {cw.get_element('wind_string')}\n(Weather) {cw.get_element('observation_time')}")
