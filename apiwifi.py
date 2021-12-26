import time
import os
import socket
# import fcntl
import struct
import configparser
import subprocess
import threading
from configparser import ConfigParser
# import main Flask class and request object
from flask import Flask, request, jsonify, Response

# Setup Config
parser = ConfigParser()
parser.read('config.ini')
# User Conf
user_id = str(parser.get('USER_CONF', 'user_id'))
device_id = str(parser.get('USER_CONF', 'device_id'))
device_name = str(parser.get('USER_CONF', 'device_name'))
#total_pin = int(parser.get('USER_CONF', 'total_pin'))

def restart():
    command = "/usr/bin/sudo /sbin/reboot"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def wpareconf():
    subprocess.check_output(["sudo", "cp", "/etc/network/interfaces.wifi", "/etc/network/interfaces"])
    subprocess.check_output(["sudo", "service", "hostapd", "stop"])
    subprocess.check_output(["sudo", "service", "dhcpcd", "restart"])
    subprocess.check_output(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])
    print('Rebotting........')
    subprocess.check_output(["/usr/bin/sudo", "/sbin/reboot"])
    os.system('reboot')
#    print('Subproccess')

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

@app.route('/adddevice', methods=['POST'])

def connectwifi():
    data = "Success"
    ssid = request.json['ssid']
    password = request.json['pass']
    device_name = request.json['device_name']
    user_id = request.json['user_id']
    device_id = request.json['device_id']
    if os.path.exists("/etc/wpa_supplicant/wpa_supplicant.conf"):
        os.remove("/etc/wpa_supplicant/wpa_supplicant.conf")
    else:
        print("The file does not exist")
    parser.set('USER_CONF', 'user_id', user_id)
    parser.set('USER_CONF', 'device_id', device_id)
    parser.set('USER_CONF', 'device_name', device_name)
#    parser.set('USER_CONF', 'total_pin', total_pin)
    with open('config.ini', 'wb') as configfile:
       parser.write(configfile)
    time.sleep(1)
    f = open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+")
    f.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
    f.write("update_config=1\n")
    f.write("country=GB\n")
    f.write('\n' + 'network={' + '\n' + '\t' + 'ssid="' + ssid + '"' + '\n' + '\t' +
            'psk="' + password + '"' + '\n' + '\t' + 'key_mgmt=WPA-PSK' + '\n' + '}')
    f.close()
    threading.Thread(target=wpareconf).start()
    response = app.response_class (
       response=data,
       status=200,
       mimetype='application/json'
    )
    return response
    time.sleep(2)
    subprocess.check_output(["sudo", "reboot"])

@app.route('/rebootnow', methods=['POST'])
def rebootnow():
    dat = {
        "code": "00",
        "error": "false",
        "message": "Module Reboot"
    }
    jsonify(dat)
    time.sleep(5)
    restart()


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host='192.168.100.1', port='443', ssl_context='adhoc')
#    app.run(debug=True, ssl_context='adhoc')
