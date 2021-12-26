import RPi.GPIO as GPIO
import os
import json
import requests
import time
import socket
import math
import threading
import subprocess
import pymongo
import socketio
import ast
import ssl
# import fcntl
import struct
import logging
import configparser
from configparser import ConfigParser
from datetime import datetime as dt
from getmac import get_mac_address

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, False)

# Setup Config
parser = ConfigParser()
parser.read('config.ini')
# Device Conf
dir = str(parser.get('DEVICE_CONF', 'dir'))
# User Conf
user_id = str(parser.get('USER_CONF', 'user_id'))
device_id = str(parser.get('USER_CONF', 'device_id'))
device_name = str(parser.get('USER_CONF', 'device_name'))
total_pin = int(parser.get('USER_CONF', 'total_pin'))
# Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))
# Backup Data
databackup = int(parser.get('BACKUP_DATA', 'backup'))
# Setup Database
myclient = pymongo.MongoClient(host)
mydb = myclient[dbs]
relay = mydb["relaystatus"]
sensor = mydb["sensorvalue"]
backups = mydb["sensorbackup"]
# upgrade firmware
firmware = str(parser.get('UPGRADE_FIRMWARE', 'firmware'))
datenow = dt.now().strftime("%Y-%m-%d")

hostname = "8.8.8.8"

#sensor_status = 0
flag = 0
active = 0

# Setup Logging
logging.basicConfig(filename='logs/socket_' + datenow + '.log', filemode='w',
                    format='%(levelname)s | %(asctime)s | %(message)s', level=logging.DEBUG)

sio = socketio.Client(
    reconnection=True, reconnection_attempts=0, reconnection_delay=1, logger=True, engineio_logger=True)

def indicator():
   GPIO.output(17, True)
   time.sleep(0.1)
   GPIO.output(17, False)
   time.sleep(0.1)


def database():
    for i in range(1, total_pin):
        query = {"_id": i}
        values = {"$set": {"true": 0}}
        sensor.update(query, values)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # NOT SUPPORT IN PYTHON3 & WINDOWS
    """ return socket.inet_ntoa(fcntl.ioctl(
  	s.fileno(),
    0x8915,  # SIOCGIFADDR
    struct.pack('256s', ifname[:15])
    )[20:24]) """

    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()

    return ip

MacAddr = get_mac_address()

IPAddr = get_ip_address('wlan0')


def cbhandshake(err, res):
    if err != None:
        print("[Connect Device : ]", err)
    else:
        print(res)
        time.sleep(0.2)
        for i in range(len(res)):
            myquery = {"_id": res[i]["pin"]}
            newvalues = {"$set": {"channelname": res[i]["device_name"]}}
            relay.update_one(myquery, newvalues)


def cbcommandpanel(err, res):
    if err != None:
        print("[Panel : ]", err)
    else:
        print("[Panel : ]", res)


def cbsensordata(err, res):
    if err != None:
        print("[Sensor Data : ]", err)
    else:
        print("[Sensor Data : ]", res)


def send_data(pin, sensorvalue, relayvalue):
    sensor_status = 0
    wattage = float(sensorvalue)
    amper = float(sensorvalue) / 220
    relay = float(relayvalue)
    ampere = round(amper, 2)
    if wattage > 3.5 and relay == 1:
       sensor_status = 1
    if wattage < 3.5 and relay == 1:
       sensor_status = 0
    if (wattage > 3.5 or wattage < 3.5) and relay == 0:
       sensor_status = 0

    payload = {
        "device_id": device_id,
        "user_id": user_id,
        "device_ip": IPAddr,
        "device_type": "1",
        "pin": str(pin),
        "ampere": str(ampere),
        "wattage": str(wattage),
        "switch": str(relayvalue),
        "sensor_status": str(sensor_status),
        "date": dt.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(payload)
    sio.emit('sensordata', payload, callback=cbsensordata)
    sio.sleep(0.2)


@sio.on('connect')
def on_connect():
    payload = {
        "device_id": device_id,
        "user_id": user_id,
        "device_ip": IPAddr,
        "device_name": device_name,
        "device_type": "1",
        "pin": str(total_pin),
        "mac_address":str(MacAddr)
    }
    print(payload)
    sio.emit('handshake', payload, callback=cbhandshake)
    time.sleep(1)
    print('connection established')
    time.sleep(1)

@sio.on('reset')
def reset(params):
    device_id = str(params["device_id"])
    reset = str(params["reset"])
    print(params)
    print('Resetting Device.....')

@sio.on('command')
def command(params):
    mode = int(params["mode"])
    pin = int(params["pin"])
    switch = int(params["switch"])

    mode = int(params["mode"])
    pin = int(params["pin"])
    switch = int(params["switch"])

    if mode == 1:
        myquery = {"_id": pin}
        newvalues = {"$set": {"status": switch}}
        relay.update_one(myquery, newvalues)
    elif mode == 2:
        newvalues = {"$set": {"status": switch}}
        relay.update({}, newvalues, multi=True)
    print(device_id, pin, params["mode"], params["switch"])

@sio.event
def reset(params):
    print('COMMAND RESET')
    print(params)
    reset = int(params["reset"])
    print('Resetting Device....')

    if reset == 1:
        subprocess.check_output(["sudo", "cp", "/etc" "/network" "/interfaces.ap", "/etc" "/network" "/interfaces"])
        subprocess.check_output(["sudo", "cp", "/home/pi/sitamoto/config.ini.example", "/home/pi/sitamoto/config.ini"])
        subprocess.check_output(["sudo", "cp", "/etc/wpa_supplicant/wpa_supplicant.conf.ori",
        "/etc/wpa_supplicant/supplicant.conf"])
        subprocess.check_output(["sudo", "reboot"])

@sio.on('upgrade_firmware')
def firmware(params):
    print('upgrade_firmware')
#    print(params)
    firmware = str(params["firmware_url"])
    print(firmware)
    parser.set('UPGRADE_FIRMWARE', 'firmware', firmware)
    with open('config.ini', 'wb') as configfile:
       parser.write(configfile)
    time.sleep(3)
    subprocess.Popen(["sudo", "python", "/home/pi/sitamoto/upgrade.py"])
    time.sleep(0.5)

@sio.on('disconnect')
def on_disconnect():
    threading.Thread(target=indicator).start()
    logging.warning('disconnected from server')
    print('Disconnected')
#    subprocess.Popen(["sudo", "python", "/home/pi/sitamoto/commandbackup.py"])
    time.sleep(1)
    backup()
    flag = 1

def backup():
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
#       active = 1

while True:
    time.sleep(1)
    try:
        sio.connect("https://sitasock.vasdev.co.id:8027")
        subprocess.check_output(["sudo", "pkill", "-f", "commandbackup.py"])
#        sio.connect("http://21.0.0.107:5005")
        print('Connected Devices')
        break
    except socketio.exceptions.ConnectionError as e:
        print(e, ': attempt reconnecting')
        continue
    except:
        print('Connection failed, attempt reconnecting')
        continue

minute = 0
error_flag = 0
total_pin += 1
databackup += 1
statusPin = [0] * total_pin
last_sensor_status = [0] * int(total_pin)

while True:
#   global active
   time.sleep(0.2)
   global socket
   if flag == 1:
      sio.connect("https://sitasock.vasdev.co.id:8027")
      flag = 0

   if minute != dt.now().minute:
      for i in range(1, total_pin):
          sensorval = sensor.find_one({'_id': i})
          relayval = relay.find_one({'_id': i})
          print(i, relayval['gpio'], relayval['status'], sensorval['value'])
          print('sensordata')
          send_data(i, sensorval['value'], relayval['status'])
          time.sleep(0.2)
          print('Sending Data')
      minute = dt.now().minute

   for i in range(1, total_pin):
       sensorval = sensor.find_one({'_id': i})
       relayval = relay.find_one({'_id': i})

       if statusPin[i] != relayval['status']:
          statusPin[i] = relayval['status']
          send_data(i, sensorval['value'], relayval['status'])


   for i in range(1, total_pin):
       sensorval = sensor.find_one({'_id': i})
       relayval = relay.find_one({'_id': i})

       query = {"_id": i}
       values = {"$set": {"true": 0, "backup": 0}}
       sensor.update_one(query, values)

       if sensorval['true'] == 1:
          send_data(i, sensorval['backup'] / 2, relayval['status'])
          time.sleep(0.2)
          print('Sending data Backup Sensor Data')


   for i in range(1, databackup):
#       time.sleep(0.1)
#       backupval = backups.find_one({'_id': i})
       if databackup > 0:
          print(databackup)
          backupval = backups.find_one({'_id': i})
          payload = {
             "device_id": device_id,
             "user_id": user_id,
             "pin": str(backupval['pin']),
             "switch": str(backupval['switch']),
             "mode": "2",
             "date": str(backupval['date'])
          }
          print(payload)
          sio.emit('commandpanel', payload, callback=cbcommandpanel)
          x = backups.delete_one({'_id': i})
          print(x.deleted_count, " backup data deleted.")
          databackup -= 1
       parser.set('BACKUP_DATA', 'backup', str(0))
       with open('config.ini', 'wb') as configfile:
          parser.write(configfile)
#       databackup = 0
       sio.sleep(0.2)
       time.sleep(0.2)


   for i in range(1, total_pin):
       sensorval = sensor.find_one({'_id': i})
       relayval = relay.find_one({'_id': i})

       myquery = {"_id": i}
       newvalues = {"$set": {"touched": 0}}
       relay.update_one(myquery, newvalues)

       if relayval['touched'] == 1:
          payload = {
              "device_id": device_id,
              "user_id": user_id,
              "pin": str(i),
              "switch": str(relayval['status']),
              "mode": "2",
              "date": dt.now().strftime("%Y-%m-%d %H:%M:%S")
          }
          sio.emit('commandpanel', payload, callback=cbcommandpanel)
          sio.sleep(0.2)
          time.sleep(0.2)
