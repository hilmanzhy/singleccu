import pymongo
from configparser import ConfigParser

# Setup Config
parser = ConfigParser()
parser.read('config.ini')
# Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))

myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]

colrelay = mydb["relaystatus"]
colsensor = mydb["sensorvalue"]
colbackup = mydb["sensorbackup"]
coldata = mydb["databackup"]

x = colrelay.delete_many({})
print(x.deleted_count, " relay documents deleted.")

#y = colsensor.delete_many({})
#print(y.deleted_count, " sensor documents deleted.")

#z = colbackup.delete_many({})
#print(z.deleted_count, " backup documents deleted.")

#a = coldata.delete_many({})
