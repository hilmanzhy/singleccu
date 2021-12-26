import wget
import time
import os
import configparser
import subprocess
from configparser import ConfigParser

# upgrade firmware
parser = ConfigParser()
parser.read('config.ini')
firmware = str(parser.get('UPGRADE_FIRMWARE', 'firmware'))
directory = '/home/pi/sitamoto'

subprocess.check_output(["sudo", "wget", firmware, "-O", "sitamoto.zip"])
print(firmware)
time.sleep(3)
subprocess.check_output(["sudo", "unzip", "-o", "sitamoto", "-x", "upgrade.py"])
print("Upgrades Done....")
