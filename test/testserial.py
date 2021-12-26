import serial
import os
import time


ser = serial.Serial('/dev/ttyUSB0', 9600)

sensordata = []
listdata = []

while True:
    try:
        if (ser.inWaiting() > 0):
            data = ser.readline()
            data = os.linesep.join([s for s in data.splitlines() if s])
            if data != '':
                sensordata = data.split()
                print(data)

    except KeyboardInterrupt:
        ser.close()
        break

    except serial.serialutil.SerialException:
        continue

    except IOError:
        ser.close()
        time.sleep(0.5)
        ser.open()
        continue

    except OSError:
        time.sleep(0.5)
        continue
