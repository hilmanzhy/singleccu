import pymongo
import time
from configparser import ConfigParser

# Setup Config
parser = ConfigParser()
parser.read('config.ini')
# User Conf
total_pin = int(parser.get('USER_CONF', 'total_pin'))
# Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))

# Setup Database
myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]
colrelay = mydb["relaystatus"]
colsensor = mydb["sensorvalue"]
colbackup = mydb["sensorbackup"]
coldata = mydb["databackup"]

print("=== Relay Collection ===")
for x in colrelay.find():
    print(x)

print("=== Sensor Collection ===")
for x in colsensor.find():
    print(x)

print("=== Sensor backup ===")
for x in colbackup.find():
    print(x)

#print("=== Data Backup ===")
#for x in coldata.find():
#    print(x)
