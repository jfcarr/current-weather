#!/usr/bin/python3

import argparse
import requests
import xml.etree.ElementTree as ET

def get_current_weather(location_code):
	r = requests.get(f'https://w1.weather.gov/xml/current_obs/{location_code}.xml')
	return r.text

def get_element(root, element_name):
	element_data = root.find(element_name)
	return element_data.text

parser = argparse.ArgumentParser()
parser.add_argument("location_code", help="Location code, e.g., 'KDAY'")
args = parser.parse_args()

content = get_current_weather(args.location_code)

root = ET.fromstring(content)

print(f"{get_element(root,'weather')}, {get_element(root,'temperature_string')}\nWind: {get_element(root,'wind_string')}\n(Weather) {get_element(root,'observation_time')}")
