#! /usr/bin/python3
#-.- coding: UTF-8 -.-

import json
import time

from datetime import datetime
from subprocess import call
from urllib.parse import quote
from urllib.request import urlopen


def printOutput(json_return, haltestelle):
    print('Station: %s' % haltestelle)
    if 'error' in json_return:
        print(json_return.get('error'))
    else:
        actual = int(datetime.today().hour) * 3600 + int(datetime.today().minute) * 60
        for station in json_return.get('stations', []):
            for departure in station.get('departures', []):
                arrival = int(departure['time'].replace("*", "").split(":")[0]) * 3600 + int(departure['time'].replace("*", "").split(":")[1]) * 60
                if (arrival - actual) / 60 < 0:
                    arrival += 60 * 60 * 24
                arrival_text = "in %2d min" % (int((arrival - actual)) / 60)
                print('%-9s%-31s%12s' % (departure['line'], departure['direction'], arrival_text))
            print()

def queryAPI(haltestelle):
    error = ''
    try:
        ret = urlopen('http://bvg-api.herokuapp.com/stations?input=' + quote(haltestelle))
        return json.loads(ret.read().decode('UTF-8'))
    except (IOError, UnicodeDecodeError) as e:
        error = 'Error grabbing %s!\n' % haltestelle
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
