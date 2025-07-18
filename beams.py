#!/usr/bin/env python3

from time import sleep
import RPi.GPIO as GPIO
import urllib.request
import json

# Global Variables
# zone1 = white
zone1 = 26
# zone2 = black
zone2 = 24
# zone3 = red
zone3 = 22
# zone4 = green
zone4 = 18
# array of pins
pins = [26, 24, 22, 18]
# Additional Variables
zone_info = ""
zone = ""
zone_data = {}
json_data = ""
url = 'https://hooks.slack.com/services/YOUR_SLACK_ID'

# Activate GPIO pins
GPIO.setmode(GPIO.BOARD)
for pin in pins:
  GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def notify_slack(data):
  print("Sending Slack message")
  req = urllib.request.Request(url, data.encode('utf-8'), headers={'Content-Type': 'application/json'})
  response = urllib.request.urlopen(req)
  the_page = response.read()

while(1):
  try:
    if GPIO.input(zone1) == 0 and GPIO.input(zone2) == 0 and GPIO.input(zone3) == 0 and GPIO.input(zone4) == 0:
        print("Roboguard not connected")
        sleep(5)
        continue
    
    if GPIO.input(zone1) == 0:
      zone = "1"
      zone_info = "Zone 1"
      zone_data["text"] = zone_info + " - Zone" + zone
      json_data = (json.dumps(zone_data, ensure_ascii=False))

      print (zone_info + " - Zone" + zone)
      notify_slack(json_data)

    if GPIO.input(zone2) == 0:
      zone = "2"
      zone_info = "Zone 2"
      zone_data["text"] = zone_info + " - Zone" + zone
      json_data = (json.dumps(zone_data, ensure_ascii=False))

      print (zone_info + " - Zone" + zone)
      notify_slack(json_data)
    
    if GPIO.input(zone3) == 0: 
      zone = "3" 
      zone_info = "Zone 3"
      zone_data["text"] = zone_info + " - Zone" + zone
      json_data = (json.dumps(zone_data, ensure_ascii=False))

      print (zone_info + " - Zone" + zone)
      notify_slack(json_data)
      
    if GPIO.input(zone4) == 0:
      zone = "4"
      zone_info = "Zone 4"
      zone_data["text"] = zone_info + " - Zone" + zone
      json_data = (json.dumps(zone_data, ensure_ascii=False))

      print (zone_info + " - Zone" + zone)
      notify_slack(json_data)

    sleep(1)
  
  except (KeyboardInterrupt, SystemExit):
    print("Quit")
    raise

  except Exception as e: print(e)
