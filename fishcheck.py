import datetime
import smtplib
from email.mime.text import MIMEText

from fishtank import settings
from fishtank.util import load_fish_dataframe


df = load_fish_dataframe(settings.DATA_PATH)

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
server.login(settings.ADMIN, settings.EMAIL_SECRET_KEY)
server.sendmail(
    settings.ADMIN,
    settings.STEAKHOLDERS,
    msg.as_string())

server.quit()
