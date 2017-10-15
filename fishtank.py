import sys
import argparse
import os
import time

from fishtank import settings


def process_command_line(argv):
    '''Parse the command line and do a first-pass on processing them into a
    format appropriate for the rest of the script.'''

    parser = argparse.ArgumentParser(formatter_class=argparse.
                                     ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(argv[1:])

    return args


def main(argv=None):
    '''Run the driver script for this module. This code only runs if we're
    being run as a script. Otherwise, it's silent and just exposes methods.'''
    args = process_command_line(argv)

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    with open(settings.TANK_THERMOMETER_PATH, 'r') as f:
        reading = [s.rstrip() for s in f.readlines()]

        if 'YES' in reading[0]:
            fishtemp = float(reading[1][reading[1].find('t=')+2:])/1000
        else:
            return 1

    with open(settings.CPU_THERMOMETER_PATH, 'r') as f:
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

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
