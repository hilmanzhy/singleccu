import pymongo
import RPi.GPIO as GPIO
import time
import threading
import subprocess
import ConfigParser
import fcntl
import requests
import json
import math
import ast
import ssl
import struct
from ConfigParser import SafeConfigParser

buttonactive1 = False
longpressactive1 = False
pressed = 1000
longpress = 5000
longpressed = 10000
noise = 100
timer = 0
timer1 = 0
duration = 0
millis = 0
all = 0
blinkled = 18
flag = 0
button = 3

#Setup Config
parser = SafeConfigParser()
parser.read('config.ini')
#User Conf
total_pin = int(parser.get('USER_CONF','total_pin'))
#Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(blinkled, GPIO.OUT)
GPIO.output(blinkled, False)
GPIO.setup(button, GPIO.IN,pull_up_down=GPIO.PUD_UP)

myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]
relay = mydb["relaystatus"]
a = 0
total_pin += 1

def thread():
  subprocess.check_output(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])

def indicator(delay):
  GPIO.output(blinkled, True)
  time.sleep(delay)
  GPIO.output(blinkled, False)
  time.sleep(delay)

def led():
  if duration > longpress and duration < 6000:
     indicator(0.1)

while True:
############################ Reset Factory ##################################
  if GPIO.input(17) == GPIO.LOW:
  if GPIO.input(button) == GPIO.LOW:
     threading.Thread(target=led).start()
     timer = time.time()
     if (timer - millis) >= 2:
        millis = timer
        flag = 0
     if buttonactive1 == False:
        buttonactive1 = True
        timer1 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer1
     if (duration > longpressed) and (longpressactive1 == False):
        longpressactive1 = True
        subprocess.check_output(["sudo", "cp", "/etc" "/network" "/interfaces.ap", "/etc" "/network" "/interfaces"])
        subprocess.check_output(["sudo", "cp", "/home/pi/sitamoto/config.ini.example", "/home/pi/sitamoto/config.ini"])
        subprocess.check_output(["sudo", "cp", "/etc/wpa_supplicant/wpa_supplicant.conf.ori",
        "/etc/wpa_supplicant/wpa_supplicant.conf"])
        subprocess.check_output(["sudo", "reboot"])
        for i in range (10):
           indicator(0.05)
        print('Resetting Mode')

  if (GPIO.input(17) == GPIO.HIGH) and (buttonactive1 == True):
############################ Rebooting Device ###########################
     flag += 1
     if flag == 3:
        subprocess.check_output(["sudo", "reboot"])
        print('Rebotting Device...')
        flag = 0
     print(flag)
  if (GPIO.input(button) == GPIO.HIGH) and (buttonactive1 == True):
     if buttonactive1 == True:
        if longpressactive1 == True:
           longpressactive1 = False
        else:
############################# Control Relay ##############################
          if duration > pressed and duration < longpress:
             all += 1
             if all == 1:
                for i in range (1, total_pin):
                  relayval = relay.find_one({'_id' : i})
                  myquery = {"_id" : i}
                  newvalues = {"$set": {"status": 0, "touched": 1}}
                  relay.update_one(myquery, newvalues)
                  print(myquery, newvalues)
             elif all == 2:
                for i in range (1, total_pin):
                  relayval = relay.find_one({'_id' : i})
                  myquery = {"_id": i}
                  newvalues = {"$set": {"status": 1, "touched": 1}}
                  relay.update_one(myquery, newvalues)
                  print(myquery, newvalues)
                  all = 0
             print('All Switch Controlling...')
             for i in range (1):
               indicator(0.2)
             timer1 = 0
############################### Change AP ###############################
          if duration > longpress and duration < longpressed:
             time.sleep(1)
             for i in range (3):
                indicator(0.1)
             subprocess.check_output(["sudo", "pkill", "-f", "ping.py"])
             subprocess.check_output(["sudo", "cp", "/etc/wpa_supplicant/wpa_supplicant.conf.ori",
             "/etc/wpa_supplicant/wpa_supplicant.conf"])
             subprocess.check_output(["sudo", "cp", "/etc/network/interfaces.ap", "/etc/network/interfaces"])
             print('Copy Networking')
             subprocess.check_output(["sudo", "service", "networking", "restart"])
             threading.Thread(target=thread).start()
             print('Restart Networking')
             subprocess.check_output(["sudo", "service", "hostapd", "restart"])
             subprocess.check_output(["sudo", "service", "dnsmasq", "restart"])
             print('Restart hostapd & dnsmasq')
             subprocess.check_output(["sudo", "python", "/home/pi/sitamoto/apiAP.py"])
             print('API Server')
             print('AP Mode')
             timer1 = 0
        buttonactive1 = False
