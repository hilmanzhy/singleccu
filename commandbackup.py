import threading
import serial
import os
import time
import pymongo
import json
import math
import ast
import struct
from datetime import datetime as dt
from configparser import ConfigParser

# Setup Database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sitamoto"]
mycol = mydb["sensorvalue"]
relay = mydb["relaystatus"]
#sensor = mydb["sensorvalue"]
backups = mydb["sensorbackup"]

x = backups.find_one()

parser = ConfigParser()
parser.read('config.ini')

total_pin = int(parser.get('USER_CONF', 'total_pin'))
flag = str(parser.get('BACKUP_DATA', 'backup'))

total_pin += 1
backup = []

number = int(flag)

def commanddb():
    for i in range(1, total_pin):
        relayval = relay.find_one({'_id': i})
        sensorval = mycol.find_one({'_id': i})
        if sensorval['true'] == 1 and relayval['command'] == 1:
           mybackup = {
                         "_id": int(number+1),
                         "pin": str(i),
                         "switch": str(relayval['status']),
                         "date": dt.now().strftime("%Y-%m-%d %H:%M:%S")
                      }
           x = backups.insert_one(mybackup)
           print(x.inserted_id)
           global number
           number += 1
           id = {"_id": i}
           values = {"$set": {"command": 0}}
           relay.update_one(id, values)
           parser.set('BACKUP_DATA', 'backup', str(number))
           with open('config.ini', 'wb') as configfile:
              parser.write(configfile)
           time.sleep(0.5)
#        if relayval['command'] == 0:
#           global number
#           number = 0
#           int(flag) = 0

while True:
      commanddb()
#      threading.Thread(target=commanddb).start()
