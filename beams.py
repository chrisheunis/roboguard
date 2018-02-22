#!/usr/bin/python
# The script reads the signals sent from the Roboguard HQ and translates it into Slack messages.
# The Robguard HQ uses a RJ12 connector to interface with a Raspberry pi model 1b.
# Author: Chris Heunis
# Date: 21/02/2018

from time import sleep
import RPi.GPIO as GPIO
import urllib2
import json

# Global Variables
# zone1 = HQ white - pi pin 26
zone1 = 26 
# zone2 = HQ black - pi pin 24
zone2 = 24 
# zone3 = HQ red - pi pin 22. Zone 3 isn't configured and has been excluded from the code.
zone3 = 22 
# zone4 = HQ green - pi pin 18
zone4 = 18
# array of pins 
pins = [26, 24, 22, 18]
# Additional Variables 
zone_info = ""
zone = ""
zone_data = {} 
json_data = ""
url = 'enter-your-slack-webhook-url'

# Activate GPIO pins
GPIO.setmode(GPIO.BOARD)
for pin in pins:
  GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def notify_slack(data):
  print "Sending Slack message"
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  the_page = response.read()

while(1):
  try:
    # Check if Roboguard data cable is connected
    if GPIO.input(zone1) == 1 and GPIO.input(zone2) == 1 and GPIO.input(zone4) == 1:
    	print "Roboguard not connected"
    	sleep(5)
 	continue
    
    # Zone 1
    if GPIO.input(zone1) == 1: 
      zone = "1" 
      zone_info = "Garage"
      zone_data["text"] = zone_info + " - Zone" + zone
      json_data = (json.dumps(zone_data, ensure_ascii=False))

      print (zone_info + " - Zone" + zone)
      notify_slack(json_data)

    # Zone 2
    if GPIO.input(zone2) == 0: 
      zone = "2" 
      zone_info = "Kitchen"
      zone_data["text"] = zone_info + " - Zone" + zone
      json_data = (json.dumps(zone_data, ensure_ascii=False))

      print (zone_info + " - Zone" + zone)
      notify_slack(json_data)
      
    # Zone 4
    if GPIO.input(zone4) == 1: 
      zone = "4"
      zone_info = "Gym"
      zone_data["text"] = zone_info + " - Zone" + zone 
      json_data = (json.dumps(zone_data, ensure_ascii=False))

      print (zone_info + " - Zone" + zone)
      notify_slack(json_data) 

    sleep(1)
  
  except (KeyboardInterrupt, SystemExit):
    print "Quit"
    raise

  except Exception as e: print(e)
