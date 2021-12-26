import ssl
import sys
import paho.mqtt.subscribe as sub

dict = {'ca_certs':"/etc/mosquitto/mosq_ca.crt",
        'certfile':"/etc/mosquitto/mosq_serv.key",
        'keyfile':"/etc/mosquitto/mosq_serv.crt",
        'tls_version':"tlsv1.2",
        'ciphers':"None"}

while 1:
   sensor = sub.simple("test",hostname="192.168.137.155")
   print(sensorgas.topic,"=",sensorgas.payload)

#   dict = {'ca_certs':"</etc/mosquitto/mosq_ca.crt>",
#           'certfile':"</etc/mosquitto/mosq_serv.key>",
#           'keyfile':"</etc/mosquitto/mosq_ser.crt>",
#           'tls_version':"<tlsv1.2>",
#           'ciphers':"<None>"}
