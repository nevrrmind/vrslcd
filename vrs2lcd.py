#!/usr/bin/python
from __future__ import print_function
import time
import socket
import fcntl
import struct
import urllib2
import base64
import json

station="<StationID>" #In my case it is EDDT
url="<VRS-URL>/AircraftList.json"
login="on" #Change to "off" if your VRS is public.
username="<Username>" #Only needed if Login=on
password="<Password>" #Only needed if Login=on
testing="off" #On, if you have no display so far.
refresh=0 #Disply-Update rate in seconds. Can also be 0.

if testing == "off":
	import I2C_LCD_driver
	mylcd = I2C_LCD_driver.lcd()	

while True:
		def readvrs():
			if login == "on":
				request=urllib2.Request(url)
				base64string=base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
				request.add_header("Authorization", "Basic %s" % base64string)
				response=urllib2.urlopen(request)
			else:
				request=urllib2.Request(url)
				response=urllib2.urlopen(request)
			flights=json.load(response)
			flightscount=flights['totalAc']
			flieger=flights['acList']
			mil_list = list()
			mlat_list = list()
			heli_list = list()
			for each in flieger:
				try:
					mil_list.append(each['Mil'])
				except KeyError:
					continue	
			for each in flieger:
				try:
					mlat_list.append(each['Mlat'])
				except KeyError:
					continue
			for each in flieger:
				try:
					heli_list.append(each['Species'])
				except KeyError:
					continue
			milflights=mil_list.count(True)
			mlatflights=mlat_list.count(True)
			heliflights=heli_list.count(4)
			if testing == "on":
				print("Station:%s"%station)
				print("%s" %time.strftime("%d.%b.%y %H:%M:%S"))
				print("AC:%s"%flightscount)
				print("MIL:%s"%milflights)
				print("Mlat:%s"%mlatflights)
				print("Heli:%s"%heliflights)
				time.sleep (1)
			else:
				def runlcd():
					mylcd.lcd_display_string("Station:%s"%station, 1,4)
					mylcd.lcd_display_string("%s" %time.strftime("%d.%b.%y %H:%M:%S"), 2)
					mylcd.lcd_display_string("AC:", 3)
					mylcd.lcd_display_string("MIL:",3,8)
					mylcd.lcd_display_string("Mlat:", 4)
					mylcd.lcd_display_string("Heli:", 4,8)
				if flightscount <10:
					mylcd.lcd_display_string("0%s"%flightscount, 3, 3)
				else:
					mylcd.lcd_display_string("%s"%flightscount, 3, 3)
				if milflights <10:
					mylcd.lcd_display_string("0%s"%milflights, 3, 13)
				else:
					mylcd.lcd_display_string("%s"%milflights, 3, 13)
				if mlatflights <10:
					mylcd.lcd_display_string("0%s"%mlatflights, 4, 5)
				else:
					mylcd.lcd_display_string("%s"%mlatflights, 4, 5)
				if heliflights <10:
					mylcd.lcd_display_string("0%s"%heliflights, 4, 13)
				else:
					mylcd.lcd_display_string("%s"%heliflights, 4, 13)
				runlcd()
			time.sleep(refresh)
		readvrs()
