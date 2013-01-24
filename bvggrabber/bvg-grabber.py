#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from datetime import datetime
from subprocess import call
from urllib.parse import quote
from urllib.request import urlopen


def printOutput(stations, stationName):
    print('Station: %s' % stationName)
    if 'error' in stations:
        print(stations.get('error'))
    else:
        currentTime = int(datetime.today().hour) * 3600 + int(datetime.today().minute) * 60
        for station in stations.get('stations', []):
            for departure in station.get('departures', []):
                departureTime = int(departure['time'].replace("*", "").split(":")[0]) * 3600 + int(departure['time'].replace("*", "").split(":")[1]) * 60
                if (departureTime - currentTime) / 60 < -1:
                    departureTime += 60 * 60 * 24
                if (departureTime - currentTime) / 60 < 2:
                    departureText = "now"
                else:
                    departureText = "in %2d min" % ((departureTime - currentTime) / 60)
                print('%-9s%-31s%12s' % (departure['line'], departure['direction'], departureText))
            print()


def queryAPI(stationName):
    error = ''
    try:
        stations = urlopen('http://bvg-api.herokuapp.com/stations?input=' + quote(stationName))
        return json.loads(stations.read().decode('UTF-8'))
    except (IOError, UnicodeDecodeError) as e:
        error = 'Error grabbing %s!\n' % stationName
        if hasattr(e, 'reason'):
            error += 'failed to connect\n'
            error += 'Reason: ' + str(e.reason)
        elif hasattr(e, 'code'):
            error += 'serverside problem\n'
            error += 'Code: ' + str(e.code) + '\n' + str(e.headers)
        else:
            error += 'Unexpected Error'
    return {'error': error}


if __name__ == '__main__':
    while(True):
        march = queryAPI('Marchbrücke')
        # ernst = queryAPI('U Ernst-Reuter-Platz')
        call("clear", shell=True)
        print('%-9s%-31s%12s' % ("Line", "Destination", "Departure"))
        printOutput(march, 'Marchbrücke')
        # printOutput(ernst, 'U Ernst-Reuter-Platz')
        time.sleep(20)
