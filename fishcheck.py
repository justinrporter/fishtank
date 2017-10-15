import datetime
import smtplib
from email.mime.text import MIMEText

import pandas as pd

df = pd.read_csv(
    '/home/pi/fishdata.csv',
    names=['time', 'temp', 'sensor'])
df = df.dropna()
df['time'] = pd.to_datetime(df['time'], unit='s')
df['temp'] = (float(9)/5 * df['temp'])+32

day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
data = df[df['time'] > day_ago]
merge = data[data['sensor'] == 'fishtank'].merge(
    data[data['sensor'] == 'cpu'], on='time', suffixes=('_tank', "_cpu"))

del merge['sensor_tank']
del merge['sensor_cpu']

msg = MIMEText(
    "Statistics on the fishtank in the last 24 hours:\n%s"
    % merge['temp_tank'].describe())
msg['Subject'] = "Regarding Your Fishies"
msg['From'] = "Fish Butler"
msg['To'] = 'Fish Czar'

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login('justinrporter@gmail.com', 'fmdkamlidluqyuuu')
server.sendmail(
    'justinrporter@gmail.com',
    ['elizabeth.k.christiansen@gmail.com', 'justinrporter@gmail.com'],
    msg.as_string())

server.quit()
