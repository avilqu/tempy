#!/usr/bin/python3

''' CLI tool for DS18B20 sensor driver.
    @author: Adrien Vilquin Barrajon <avilqu@gmail.com>
'''

import os
import glob
from datetime import datetime
import time
import sqlite3
from sqlite3 import Error

import config as cfg
from db import *
from DS18B20 import *

sensors_dirs = glob.glob(cfg.BASE_DIR + '28*')
sensors = []
for item in sensors_dirs:
    sensors.append(DS18B20(item))
if not sensors:
    print('No sensor found on host system.')
else:
    print(sensors)


def start_recording():
    db = DB()
    while True:
        data_points = [{
            'measurement': 'indoorTemp',
            'fields': {
                'temperature': round(sensors[0].read_temp(), 2)
            }
        }, {
            'measurement': 'outdoorTemp',
            'fields': {
                'temperature': round(sensors[1].read_temp(), 2)
            }
        }]
        db.write_data_points(data_points)

        time.sleep(cfg.RECORD_INTERVAL)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='Reads output from DS18B20 temperature sensors. Check config.py for settings.')
    parser.add_argument(
        '-l', '--loop', help='print temp loop (1s interval)', action='store_true')
    parser.add_argument(
        '-r', '--record', help='record data to database', action='store_true')

    args = parser.parse_args()

    if args.loop and args.record:
        print('Loop and record functions are exclusive to each other.')
        exit()

    elif args.loop:
        while True:
            for sensor in sensors:
                print(sensor.sensor_id, ':', sensor.read_temp())
            time.sleep(1)

    elif args.record:
        start_recording()

    else:
        for sensor in sensors:
            print(sensor.sensor_id, ':', sensor.read_temp())
