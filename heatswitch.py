from __future__ import absolute_import

import sys
import argparse
import random
import datetime

import util
import settings


def process_command_line(argv):
    '''Parse the command line and do a first-pass on processing them into a
    format appropriate for the rest of the script.'''

    parser = argparse.ArgumentParser(formatter_class=argparse.
                                     ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "--max-temp", required=True, type=float,
        help="The temperature above which the fishtank shouldn't go.")
    parser.add_argument(
        "--min-temp", required=True, type=float,
        help="The temperature below which the fishtank shouldn't go.")

    args = parser.parse_args(argv[1:])

    return args


def modulate_heater(current_mean_temp, max_temp, min_temp):
    """
    """

    rand_value = random.random()

    # number for choosing if the heater should be turned off
    # could be made sigmoidal!
    p_heater_off = (current_mean_temp - min_temp) / max_temp

    if p_heater_off > rand_value:
        util.deactivate_heater()
        return False
    else:
        util.activate_heater()
        return True


def main(argv=None):
    '''Run the driver script for this module. This code only runs if we're
    being run as a script. Otherwise, it's silent and just exposes methods.'''
    args = process_command_line(argv)

    df = util.load_fish_dataframe(settings.DATA_PATH)

    oldest_datapoint = datetime.datetime.now() - datetime.timedelta(minutes=5)
    data = df[df['time'] > oldest_datapoint]

    mean_temp = data['temp'].mean()

    heater_on = modulate_heater(mean_temp, args.max_temp, args.min_temp)

    with open(settings.HEATER_STATUS_PATH, 'a') as f:
        s = '%s,%s' % (datetime.now(), int(heater_on))
        f.write(s+'\n')
        print(s)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
