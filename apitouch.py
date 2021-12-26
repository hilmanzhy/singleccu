import time
import os
import socket
import struct
import configparser
import subprocess
import threading
import RPi.GPIO as GPIO
import pymongo
import requests
import json

# import main Flask class and request object
from flask import Flask, request, jsonify, Response

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

IPAddr = get_ip_address('wlan0')
app = Flask(__name__)  # create the Flask app

@app.route('/touchsensor', methods=['POST'])
def rebootnow():
    dat = {
        "code": "00",
        "error": "false",
        "message": "Module Reboot"
    }
    jsonify(dat)
    time.sleep(5)
    restart()

@app.route('/', methods=['POST'])
def hello():
#  return"<html><head><title>ESP8266 Demo</title></head><body><h1>Hello from ESP8266!</h1></body></html>"
  data = request.data
  print(data)
  return"Hello ESP8266"
  response = app.response_class (
    response="hello ESP",
#    status=200,
#    mimetype='text/html'
  )
  return response
  time.sleep(1)

#app.run()

if __name__ == '__main__':
    # run app in debug mode on port 5000
#    app.run(debug=True, host=IPAddr, port='8025', ssl_context='adhoc')
    app.run(debug=True, host=IPAddr, port='8025', ssl_context=('cert.pem', 'key.pem'))
#    app.run(debug=True, host=IPAddr, port='443')
#    app.run(debug=True, ssl_context='adhoc')
