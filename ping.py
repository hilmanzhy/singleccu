import os
import threading
import subprocess
import time
import RPi.GPIO as GPIO
import pymongo
import ConfigParser
import fcntl
#import request
import json
from ConfigParser import SafeConfigParser

#Setup Config
parser = SafeConfigParser()
parser.read('config.ini')
#User Conf
total_pin = int(parser.get('USER_CONF','total_pin'))
total_pin += 1
#Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, False)
hostname = "8.8.8.8"

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sitamoto"]
sensor = mydb["sensorvalue"]
relay = mydb["relaystatus"]

active = 0
flag = 0
on = 0
off = 1
data = []

def database():
    for i in range(1, total_pin):
       query = {"_id": i}
       values = {"$set": {"true": 0}}
       sensor.update(query, values)

def indicator():
   GPIO.output(17, True)
   time.sleep(0.1)
   GPIO.output(17, False)
   time.sleep(0.1)

while True:
   global active
   global flag
   response = os.system("ping -c3 " + hostname)
   time.sleep(5)
   if response == 0 and active == 0:
      GPIO.output(17, True)
      print hostname, 'Server Connected!!!'
      subprocess.Popen(["sudo", "python", "/home/pi/sitamoto/socketclientpi.py"])
      subprocess.check_output(["sudo", "pkill", "-f", "commandbackup.py"])
      flag = 0
      active = 1

   if response != 0 and flag == 0:
      threading.Thread(target=indicator).start()
      print hostname, 'Server  Down!!!'
      subprocess.check_output(["sudo", "pkill", "-f", "socketclientpi.py"])
      subprocess.Popen(["sudo", "python", "/home/pi/sitamoto/commandbackup.py"])
      for i in range(1, total_pin):
          relayval = relay.find_one({'_id': i})
          sensorval = sensor.find_one({'_id': i})
          if relayval['status'] == 1:
             query = {"_id": i}
             values = {"$set": {"true": 1}}
             sensor.update_one(query, values)
          if relayval['status'] == 0:
             query = {"_id": i}
             values = {"$set": {"true": 0}}
             sensor.update_one(query, values)
      flag = 1
      active = 0
