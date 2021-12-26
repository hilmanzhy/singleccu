import pymongo
import socket
# import fcntl
import struct
import time
import subprocess
import threading
import logging
from datetime import datetime as dt
from configparser import ConfigParser
datenow = dt.now().strftime("%Y-%m-%d")

#Setup Config
parser = ConfigParser()
parser.read('config.ini')

# Mongo Conf
host = str(parser.get('MONGO_CONF', 'host'))
dbs = str(parser.get('MONGO_CONF', 'dbs'))

myclient = pymongo = pymongo.MongoClient(host)
mydb = myclient[dbs]

colbackup = mydb["sensorbackup"]

# Setup Logging
logging.basicConfig(filename='logs/main_' + datenow + '.log', filemode='w',
                    format='%(levelname)s | %(asctime)s | %(message)s', level=logging.DEBUG)

# Device Conf
dir = str(parser.get('DEVICE_CONF', 'dir'))
py = str(parser.get('DEVICE_CONF', 'py'))
values = str(parser.get('USER_CONF', 'device_id'))

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

def apiwifi():
    subprocess.Popen(["sudo", py, dir + "apiwifi.py"])

def socketclientpi():
    subprocess.Popen(["sudo", py, dir + "socketclientpi.py"])

def touch():
    subprocess.Popen(["sudo", py, dir + "touchtrigger.py"])

def sensor():
    subprocess.Popen(["sudo", py, dir + "sensordata.py"])

def setrelay():
    subprocess.Popen(["sudo", py, dir + "setrelay.py"])

def pingsocket():
    subprocess.Popen(["sudo", py, dir + "ping.py"])

def overide():
    subprocess.Popen(["sudo", py, dir + "overide.py"])

def settouch():
    subprocess.Popen(["sudo", py, dir + "settouch.py"])

def backup():
    subprocess.Popen(["sudo", py, dir + "commandbackup.py"])

def vpn():
    subprocess.check_output(["sudo", "openvpn", "/etc/openvpn/vpn.ovpn"])
    time.sleep(1)

def wifimode():
    IPAddrTun = get_ip_address('wlan0')
    print(IPAddrTun)
    setrelay()
#    socketclientpi()
    sensor()
    pingsocket()
#    overide()
#    settouch()
#    backup()
#    settouch()
#    vpn()

def delete():
    x = colbackup.delete_many({})

while True:
    try:
        IPAddrWlan = get_ip_address('wlan0')
        print(IPAddrWlan)
        if values == "NULL":
           subprocess.check_output(["sudo", "cp", "/etc/network/interfaces.ap", "/etc/network/interfaces"])
           time.sleep(0.5)
           subprocess.check_output(["sudo", "service", "hostapd", "restart"])
           threading.Thread(target=apiwifi).start()
           time.sleep(1)
           break
        else:
           time.sleep(0.5)
           subprocess.check_output(["sudo", "service", "hostapd", "stop"])
           time.sleep(1)
           wifimode()
           break
    except IOError:
        print("Wlan belum aktif")
        time.sleep(1)
