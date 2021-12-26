import pymongo
import RPi.GPIO as GPIO
import time
from configparser import ConfigParser

GPIO.setmode(GPIO.BCM)

# Setup Config
parser = ConfigParser()
parser.read('/home/pi/sitamoto/config.ini')
# Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))

myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]

relay = mydb["relaystatus"]
leng = relay.count()
leng += 1
print(leng)
while True:
    time.sleep(0.1)
    for i in range(1, leng):
        valuenya = relay.find_one({'_id': i})
        GPIO.setup(valuenya['gpio'], GPIO.OUT)
        if valuenya['status'] == 1:
            GPIO.output(valuenya['gpio'], GPIO.HIGH)
            # print(valuenya['gpio'])
        else:
            GPIO.output(valuenya['gpio'], GPIO.LOW)
            # print(valuenya['gpio'])
