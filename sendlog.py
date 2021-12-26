import json
import requests
import ast
import time

api_url_sensordata = "https://sitasock.vasdev.co.id:8027/device/sensordata"
header = {
    "Content-Type": "application/json",
    "Session-Key": "device"
}

f = open("log.txt", "r+")
logdata = f.readlines()
leng = len(logdata)
f.close()

while leng != 0:
    try:
        f = open("log.txt", "r+")
        payload = f.readline()
        logdata = f.readlines()
        leng = len(logdata)
        sendpayload = ast.literal_eval(payload.strip('\n'))

        print(sendpayload)
        print(json.dumps(sendpayload))
        r = requests.post(url=api_url_sensordata, data=json.dumps(
            sendpayload), headers=header, timeout=3)
        # Close opened file
        f.close()

        f = open("log.txt", "w+")
        j = len(logdata)
        for i in range(0, leng):
            f.write(logdata[i])
        f.close()
        time.sleep(1)
    except requests.exceptions.ConnectionError as e:
        time.sleep(10)
        pass
