#!/usr/bin/python3

import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument("location_code", help="Location code, e.g., 'KDAY'")
args = parser.parse_args()

cw = CurrentWeather(args.location_code)

cw.get_current_weather()

print(f"{cw.get_element('weather')}, {cw.get_element('temp_f')} F (windchill {cw.get_element('windchill_f')} F)\nWind: {cw.get_element('wind_string')}\n(Weather) {cw.get_element('observation_time')}")
