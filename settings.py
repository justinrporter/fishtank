HUB_CTRL_PATH = '/home/pi/hub-ctrl.c/hub-ctrl'
DATA_PATH = '/home/pi/fishdata.csv'
HEATER_STATUS_PATH = '/home/pi/heaterstatus.txt'
TANK_THERMOMETER_PATH = '/sys/bus/w1/devices/28-000007c5d1fd/w1_slave'

ADMIN = 'justinrporter@gmail.com'
STEAKHOLDERS = [ADMIN, 'elizabeth.k.christiansen@gmail.com']

with open('email-secret-key.txt', 'r') as f:
    EMAIL_SECRET_KEY = f.read().strip()
