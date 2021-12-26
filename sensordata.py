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
backups = mydb["sensorbackup"]

x = backups.find_one()

parser = ConfigParser()
parser.read('config.ini')

user_id = str(parser.get('USER_CONF', 'user_id'))
device_id = str(parser.get('USER_CONF', 'device_id'))
total_pin = int(parser.get('USER_CONF', 'total_pin'))
flag = str(parser.get('BACKUP_DATA', 'backup'))

total_pin += 1

ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

#ser = serial.Serial('/dev/ttyUSB0', 9600)

sensordata = []
listdata = []
sensorbackup = []
backup = []

number = int(flag)

def savetodb(sensordata):
    lens = len(sensordata)
    if lens != 0:
       for i in range (1, total_pin):
          myquery = {"_id": i}
          newvalues = {"$set": {"value": int(sensordata[i-1])}}
          mycol.update(myquery, newvalues)
    print('Value Created...')
    print(sensordata)

def savedb(backup):
       lens = len(backup)
       if lens != 0:
          query = {"_id": i}
          values = {"$inc": {"backup": int(backup[i-1])}}
          mycol.update(query, values)
       print('Backup Saved...')
       print(backup)

while True:
    time.sleep(0.1)
    try:
        if (ser.inWaiting() > 0):
            data = ser.readline()
            data = os.linesep.join([s for s in data.splitlines() if s])
            if data != '':
               sensordata = data.split()
               backup = data.split()
            savetodb(sensordata)
            for i in range(1, total_pin):
                sensorval = mycol.find_one({'_id': i})
                if sensorval['true'] == 1:
                   savedb(backup)
    except KeyboardInterrupt:
        ser.close()
        break

#    except serial.serialutil.SerialException as e:
#        print(e)
#        time.sleep(2.5)
#        continue

    except IOError:
        print('Reconnecting...')
        ser.close()
        time.sleep(1)
        ser.open()
#        time.sleep(2.5)
#        ser.open()
        continue

    except OSError:
        time.sleep(0.5)
        continue

