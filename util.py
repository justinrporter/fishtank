import os
import pandas as pd

from settings import HUB_CTRL_PATH


def load_fish_dataframe(filename):
    """Returns a dataframe of the fishtank temperature with units
    Fahrenheit and seconds.
    """

    df = pd.read_csv(
        filename,
        names=['time', 'temp', 'sensor'])
    df = df.dropna()
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['temp'] = (float(9)/5 * df['temp'])+32

    df = df.dropna()
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['temp'] = (float(9)/5 * df['temp'])+32

    return df


def deactivate_heater():
    """Turn off the fishtank heater
    """

    # current implementation is by turning off the relevant USB port
    os.system('sudo %s -h 0 -P 2 -p 0' % HUB_CTRL_PATH)


def activate_heater():
    """Turn on the fishtank heater
    """

    # current implementation is by turning on the relevant USB port
    os.system('sudo %s -h 0 -P 2 -p 1' % HUB_CTRL_PATH)
