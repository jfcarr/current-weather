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

	def get_apparent_temperature(self):
		temperature = float(self.get_element('temp_f'))
		wind_speed = float(self.get_element('wind_mph'))
		relative_humidity = float(self.get_element('relative_humidity'))

		apparent_temperature = temperature

		# Wind Chill (for colder temperatures)
		if temperature <= 50 and wind_speed >= 3:
			apparent_temperature = 35.74 + (0.6215*temperature) - 35.75*(wind_speed**0.16) + ((0.4275*temperature)*(wind_speed**0.16))
		
		# Heat Index (for warmer temperatures)
		if temperature >= 80:
			apparent_temperature = 0.5 * (temperature + 61.0 + ((temperature-68.0)*1.2) + (relative_humidity*0.094))
		
			if apparent_temperature >= 80:
				apparent_temperature = -42.379 + 2.04901523*temperature + 10.14333127*relative_humidity - .22475541*temperature*relative_humidity - .00683783*temperature*temperature - .05481717*relative_humidity*relative_humidity + .00122874*temperature*temperature*relative_humidity + .00085282*temperature*relative_humidity*relative_humidity - .00000199*temperature*temperature*relative_humidity*relative_humidity
				if relative_humidity < 13 and temperature >= 80 and temperature <= 112:
					apparent_temperature = apparent_temperature - ((13-relative_humidity)/4)*math.sqrt((17-math.fabs(temperature-95.))/17)
					if relative_humidity > 85 and temperature >= 80 and temperature <= 87:
						apparent_temperature = apparent_temperature + ((relative_humidity-85)/10) * ((87-temperature)/5)

		return round(apparent_temperature,1)

parser = argparse.ArgumentParser()
parser.add_argument("location_code", help="Location code, e.g., 'KDAY'")
args = parser.parse_args()

cw = CurrentWeather(args.location_code)

cw.get_current_weather()

current_temperature = float(cw.get_element('temp_f'))
apparent_temperature = cw.get_apparent_temperature()

apparent_temperature_string = "" if current_temperature == apparent_temperature else f" (feels like {apparent_temperature} F)"

print(f"{cw.get_element('weather')}, {cw.get_element('temp_f')} F{apparent_temperature_string}\nWind: {cw.get_element('wind_string')}\n{cw.get_element('observation_time')} (weather)")
