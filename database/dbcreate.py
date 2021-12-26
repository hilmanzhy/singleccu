import pymongo
import time
from random import randint
from configparser import ConfigParser

# Setup Config
parser = ConfigParser()
parser.read('config.ini')
# User Conf
total_pin = int(parser.get('USER_CONF', 'total_pin'))
#total_pin = 10
# Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))

# Setup Database
myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]

colrelay = mydb["relaystatus"]
colsensor = mydb["sensorvalue"]
colbackup = mydb["sensorbackup"]

x = colrelay.find_one()
y = colsensor.find_one()
z = colbackup.find_one()

if x == None:
    mylist = [
        {"_id": 1, "gpio": 27, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 2, "gpio": 22, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 3, "gpio": 5, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 4, "gpio": 6, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 5, "gpio": 13, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 6, "gpio": 19, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 7, "gpio": 26, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 8, "gpio": 16, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 9, "gpio": 20, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"},
        {"_id": 10, "gpio": 21, "status": "1",
            "touched": "0", "channelname": "Default", "command": "0"}
    ]
    x = colrelay.insert_many(mylist)

    if x != None:
        print("Collection Relay created")
    else:
        print("Collection Relay failed to create")

else:
    print("Collection Relay exist")

if y == None:
   if total_pin != 0:
      sensorlist = []
      for i in range(total_pin):
         column = {"_id": i+1, "value": "0", "backup": "0", "true": "0"}
         sensorlist.append(column)

      y = colsensor.insert_many(sensorlist)

      if y != None:
         print("Collection Sensor created")
      else:
         print("Collection Sensor failed to create")

   else:
      print("Collection Sensor failed to create")

else:
   print("Collection Sensor exist")

#if z == None:
#   if total_pin!= 0:
#      sensorbackup = []
#      for i in range(total_pin):
#      column = {"_id": 1, "name": 0, "value": 0}
#      sensorbackup.append(column)

#      z = colbackup.insert_many(sensorbackup)
#
#      if z != None:
#         print("Collection Sensor backup created")
#      else:
#         print("Collection sensor backup failed to create")
#   else:
#      print("Collection sensor backup exist")
