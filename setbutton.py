import pymongo
import RPi.GPIO as GPIO
import time
import threading
import socket
import ConfigParser
import fcntl
import requests
import json
from ConfigParser import SafeConfigParser

buttonactive1 = False
longpressactive1 = False
buttonactive2 = False
longpressactive2 = False
buttonactive3 = False
longpressactive3 = False
buttonactive4 = False
longpressactive4 = False
buttonactive5 = False
longpressactive5 = False
buttonactive6 = False
longpressactive6 = False
buttonactive7 = False
longpressactive7 = False
buttonactive8 = False
longpressactive8 = False
buttonactive9 = False
longpressactive9 = False
buttonactive0 = False
longpressactive0 = False

longpress = 3000
noise = 50
timer1 = 0
timer2 = 0
timer3 = 0
timer4 = 0
timer5 = 0
timer6 = 0
timer7 = 0
timer8 = 0
timer9 = 0
timer0 = 0
duration = 0
tombol1 = 0
tombol2 = 0
tombol3 = 0
tombol4 = 0
tombol5 = 0
tombol6 = 0
tombol7 = 0
tombol8 = 0
tombol9 = 0
tombol0 = 0
all = 0
all1 = 0
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
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(9, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN,pull_up_down=GPIO.PUD_UP)
myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]
relay = mydb["relaystatus"]

total_pin += 1

while True:
  if GPIO.input(18) == GPIO.LOW:
     if buttonactive1 == False:
        buttonactive1 = True
        timer1 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer1
     if (duration > longpress) and (longpressactive1 == False):
        longpressactive1 = True
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
        print('All Switch control')
  if (GPIO.input(18) == GPIO.HIGH) and (buttonactive1 == True):
     if buttonactive1 == True:
        if longpressactive1 == True:
           longpressactive1 = False
        else:
          if duration > noise:
             tombol1 += 1
             if tombol1 == 1:
                relayval = relay.find_one({'_id': 1})
                if relayval['status'] == 1:
                   myquery = {"_id": 1}
                   newvalues = {"$set": {"status": 0, "touched": 1}}
                   relay.update_one(myquery, newvalues)
                   print(myquery, newvalues)
                   time.sleep(0.5)
                   tombol1 = 0
                else:
                   myquery = {"_id": 1}
                   newvalues = {"$set": {"status": 1, "touched": 1}}
                   relay.update_one(myquery, newvalues)
                   print(myquery, newvalues)
                   time.sleep(0.5)
                   tombol1 = 0
        buttonactive1 = False

  if GPIO.input(23) == GPIO.LOW:
     if buttonactive2 == False:
        buttonactive2 = True
        timer2 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer2
     if (duration > longpress) and (longpressactive2 == False):
         longpressactive2= True
#        subprocess.check_output(["sudo", "cp", "/etc" "/network" "/interfaces.ap", "/etc" "/network" "/interfaces"])
#        subprocess.check_output(["sudo", "cp", "/home/pi/sitamoto/config.ini.example", "/home/pi/sitamoto/config.ini"])
#        subprocess.check_output(["sudo", "cp", "/etc/wpa_supplicant/wpa_supplicant.conf.ori",
#        "/etc/wpa_supplicant/supplicant.conf"])
#        subprocess.check_output(["sudo", "reboot"])
         print('Resetting Device SingleCCU...')
  if (GPIO.input(23) == GPIO.HIGH) and (buttonactive2 == True):
     if buttonactive2 == True:
        if longpressactive2 == True:
           longpressactive2 = False
        else:
           if duration > noise:
              tombol2 += 1
              if tombol2 == 1:
                 relayval = relay.find_one({'_id': 2})
                 if relayval['status'] == 1:
                    myquery = {"_id": 2}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol2 = 0
                 else:
                    myquery = {"_id": 2}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol2 = 0
                    time.sleep(0.5)
        buttonactive2 = False

  if GPIO.input(24) == GPIO.LOW:
     if buttonactive3 == False:
        buttonactive3 = True
        timer3 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer3
  if (GPIO.input(24) == GPIO.HIGH) and (buttonactive3 == True):
     if buttonactive3 == True:
        if longpressactive3 == True:
           longpressactive3 = False
        else:
           if duration > noise:
              tombol3 += 1
              if tombol3 == 1:
                 relayval = relay.find_one({'_id': 3})
                 if relayval['status'] == 1:
                    myquery = {"_id": 3}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol3 = 0
                 else:
                    myquery = {"_id": 3}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol3 = 0
                    time.sleep(0.5)
        buttonactive3 = False

  if GPIO.input(25) == GPIO.LOW:
     if buttonactive4 == False:
        buttonactive4 = True
        timer4 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer4
  if (GPIO.input(25) == GPIO.HIGH) and (buttonactive4 == True):
     if buttonactive4 == True:
        if longpressactive4 == True:
           longpressactive4 = False
        else:
           if duration > noise:
              tombol4 += 1
              if tombol4 == 1:
                 relayval = relay.find_one({'_id': 4})
                 if relayval['status'] == 1:
                    myquery = {"_id": 4}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol4 = 0
                 else:
                    myquery = {"_id": 4}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol4 = 0
                    time.sleep(0.5)
        buttonactive4 = False

  if GPIO.input(8) == GPIO.LOW:
     if buttonactive5 == False:
        buttonactive5 = True
        timer5 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer5
  if (GPIO.input(8) == GPIO.HIGH) and (buttonactive5 == True):
     if buttonactive5 == True:
        if longpressactive5 == True:
           longpressactive5 = False
        else:
           if duration > noise:
              tombol5 += 1
              if tombol5 == 1:
                 relayval = relay.find_one({'_id': 5})
                 if relayval['status'] == 1:
                    myquery = {"_id": 5}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol5 = 0
                 else:
                    myquery = {"_id": 5}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol5 = 0
                    time.sleep(0.5)
        buttonactive5 = False

  if GPIO.input(7) == GPIO.LOW:
     if buttonactive6 == False:
        buttonactive6 = True
        timer6 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer6
  if (GPIO.input(7) == GPIO.HIGH) and (buttonactive6 == True):
     if buttonactive6 == True:
        if longpressactive6 == True:
           longpressactive6 = False
        else:
           if duration > noise:
              tombol6 += 1
              if tombol6 == 1:
                 relayval = relay.find_one({'_id': 6})
                 if relayval['status'] == 1:
                    myquery = {"_id": 6}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol6 = 0
                 else:
                    myquery = {"_id": 6}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol6 = 0
                    time.sleep(0.5)
        buttonactive6 = False

  if GPIO.input(12) == GPIO.LOW:
     if buttonactive7 == False:
        buttonactive7 = True
        timer7 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer7
  if (GPIO.input(12) == GPIO.HIGH) and (buttonactive7 == True):
     if buttonactive7 == True:
        if longpressactive7 == True:
           longpressactive7 = False
        else:
           if duration > noise:
              tombol7 += 1
              if tombol7 == 1:
                 relayval = relay.find_one({'_id': 7})
                 if relayval['status'] == 1:
                    myquery = {"_id": 7}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol7 = 0
                 else:
                    myquery = {"_id": 7}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol7 = 0
                    time.sleep(0.5)
        buttonactive7 = False

  if GPIO.input(10) == GPIO.LOW:
     if buttonactive8 == False:
        buttonactive8 = True
        timer8 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer8
  if (GPIO.input(10) == GPIO.HIGH) and (buttonactive8 == True):
     if buttonactive8 == True:
        if longpressactive8 == True:
           longpressactive8 = False
        else:
           if duration > noise:
              tombol8 += 1
              if tombol8 == 1:
                 relayval = relay.find_one({'_id': 8})
                 if relayval['status'] == 1:
                    myquery = {"_id": 8}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol8 = 0
                 else:
                    myquery = {"_id": 8}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol8 = 0
                    time.sleep(0.5)
        buttonactive8 = False

  if GPIO.input(9) == GPIO.LOW:
     if buttonactive9 == False:
        buttonactive9 = True
        timer9 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer9
  if (GPIO.input(9) == GPIO.HIGH) and (buttonactive9 == True):
     if buttonactive9 == True:
        if longpressactive9 == True:
           longpressactive9 = False
        else:
           if duration > noise:
              tombol9 += 1
              if tombol9 == 1:
                 relayval = relay.find_one({'_id': 9})
                 if relayval['status'] == 1:
                    myquery = {"_id": 9}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol9 = 0
                 else:
                    myquery = {"_id": 9}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol9 = 0
                    time.sleep(0.5)
        buttonactive9 = False

  if GPIO.input(11) == GPIO.LOW:
     if buttonactive0 == False:
        buttonactive0 = True
        timer0 = (time.time() * 1000)
     duration = (time.time() * 1000) - timer0
  if (GPIO.input(11) == GPIO.HIGH) and (buttonactive0 == True):
     if buttonactive0 == True:
        if longpressactive0 == True:
           longpressactive0 = False
        else:
           if duration > noise:
              tombol0 += 1
              if tombol0 == 1:
                 relayval = relay.find_one({'_id': 10})
                 if relayval['status'] == 1:
                    myquery = {"_id": 10}
                    newvalues = {"$set": {"status": 0, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    time.sleep(0.5)
                    tombol0 = 0
                 else:
                    myquery = {"_id": 10}
                    newvalues = {"$set": {"status": 1, "touched": 1}}
                    relay.update_one(myquery, newvalues)
                    print(myquery, newvalues)
                    tombol0 = 0
                    time.sleep(0.5)
        buttonactive0 = False
