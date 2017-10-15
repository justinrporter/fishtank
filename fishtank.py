import requests
import os
import time
import json

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

with open('/sys/bus/w1/devices/28-000007c5d1fd/w1_slave', 'r') as f:
    reading = [s.rstrip() for s in f.readlines()]

    if 'YES' in reading[0]:
        fishtemp = float(reading[1][reading[1].find('t=')+2:])/1000
    else:
        exit()

with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
    cputemp = float(f.read())/1000
        

epoch = time.time()
payload = [
    {
        "key": "fishtank",
        "value": fishtemp,
        "epoch": epoch
    },
    {
        "key": "cpu",
        "value": cputemp,
        "epoch": epoch
    }
]

with open('/home/pi/fishdata.csv', 'a') as f:
    for measurement in payload:
        f.write(",".join(map(str, measurement.values())) + "\n")
