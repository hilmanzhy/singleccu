import time
import RPi.GPIO as GPIO
import pymongo
import threading
import socket
import ConfigParser
import fcntl
import requests
import json
import math
import subprocess
from ConfigParser import SafeConfigParser

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

pin1 = 18
pin2 = 23
pin3 = 24
pin4 = 10
pin5 = 9
pin6 = 25
pin7 = 11
pin8 = 8
pin9 = 7
pin0 = 12

GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

actif1 = 0
actif2 = 0
actif3 = 0
actif4 = 0
actif5 = 0
actif6 = 0
actif7 = 0
actif8 = 0
actif9 = 0
actif0 = 0

myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]
relay = mydb["relaystatus"]

while True:
  if GPIO.input(pin1) == GPIO.HIGH and actif1 == 0:
     relayval = relay.find_one({'_id' : 1})
     myquery = {"_id": 1}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif1 = 1

  if GPIO.input(pin1) == GPIO.LOW and actif1 == 1:
     relayval = relay.find_one({'_id' : 1})
     myquery = {"_id": 1}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif1 = 0

  if GPIO.input(pin2) == GPIO.HIGH and actif2 == 0:
     relayval = relay.find_one({'_id' : 2})
     myquery = {"_id": 2}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif2 = 1

  if GPIO.input(pin2) == GPIO.LOW and actif2 == 1:
     relayval = relay.find_one({'_id' : 2})
     myquery = {"_id": 2}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif2 = 0

  if GPIO.input(pin3) == GPIO.HIGH and actif3 == 0:
     relayval = relay.find_one({'_id' : 3})
     myquery = {"_id": 3}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif3 = 1

  if GPIO.input(pin3) == GPIO.LOW and actif3 == 1:
     relayval = relay.find_one({'_id' : 3})
     myquery = {"_id": 3}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif3 = 0

  if GPIO.input(pin4) == GPIO.HIGH and actif4 == 0:
     relayval = relay.find_one({'_id' : 4})
     myquery = {"_id": 4}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif4 = 1

  if GPIO.input(pin4) == GPIO.LOW and actif4 == 1:
     relayval = relay.find_one({'_id' : 4})
     myquery = {"_id": 4}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif4 = 0

  if GPIO.input(pin5) == GPIO.HIGH and actif5 == 0:
     relayval = relay.find_one({'_id' : 5})
     myquery = {"_id": 5}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif5 = 1

  if GPIO.input(pin5) == GPIO.LOW and actif5 == 1:
     relayval = relay.find_one({'_id' : 5})
     myquery = {"_id": 5}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif5 = 0

  if GPIO.input(pin6) == GPIO.HIGH and actif6 == 0:
     relayval = relay.find_one({'_id' : 6})
     myquery = {"_id": 6}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif6 = 1

  if GPIO.input(pin6) == GPIO.LOW and actif6 == 1:
     relayval = relay.find_one({'_id' : 6})
     myquery = {"_id": 6}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif6 = 0

  if GPIO.input(pin7) == GPIO.HIGH and actif7 == 0:
     relayval = relay.find_one({'_id' : 7})
     myquery = {"_id": 7}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif7 = 1

  if GPIO.input(pin7) == GPIO.LOW and actif7 == 1:
     relayval = relay.find_one({'_id' : 7})
     myquery = {"_id": 7}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif7 = 0

  if GPIO.input(pin8) == GPIO.HIGH and actif8 == 0:
     relayval = relay.find_one({'_id' : 8})
     myquery = {"_id": 8}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif8 = 1

  if GPIO.input(pin8) == GPIO.LOW and actif8 == 1:
     relayval = relay.find_one({'_id' : 8})
     myquery = {"_id": 8}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif8 = 0

  if GPIO.input(pin9) == GPIO.HIGH and actif9 == 0:
     relayval = relay.find_one({'_id' : 9})
     myquery = {"_id": 9}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif9 = 1

  if GPIO.input(pin9) == GPIO.LOW and actif9 == 1:
     relayval = relay.find_one({'_id' : 9})
     myquery = {"_id": 9}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif9 = 0

  if GPIO.input(pin0) == GPIO.HIGH and actif0 == 0:
     relayval = relay.find_one({'_id' : 10})
     myquery = {"_id": 10}
     newvalues = {"$set": {"status": 1, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch On')
     actif0 = 1

  if GPIO.input(pin0) == GPIO.LOW and actif0 == 1:
     relayval = relay.find_one({'_id' : 10})
     myquery = {"_id": 10}
     newvalues = {"$set": {"status": 0, "touched": 1, "command": 1}}
     relay.update_one(myquery, newvalues)
     print(myquery, newvalues)
     print('Switch Off')
     actif0 = 0
