#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from bvggrabber.api.actualdeparture import ActualDepartureQueryApi

from bvggrabber.api.scheduleddeparture import ScheduledDepartureQueryApi, Vehicle


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Query the BVG-website for departures')
    parser.add_argument('station', type=str, help='The station to query')
    parser.add_argument('file', type=str, help='Path to file')
    parser.add_argument('--vehicle', type=str, nargs='*',
                        help='''Vehicles which shall be queried,
                              if non given actualdepartue (bus)
                              will be used''')
    parser.add_argument('--limit', type=int, help='Max departures to query')
    args = parser.parse_args()

    query = None
    res = None
    if args.vehicle:
        vehicles = 0
        bus = False
        for vehicle in args.vehicle:
            if vehicle == 'S':
                vehicles |= Vehicle.S
            elif vehicle == 'U':
                vehicles |= Vehicle.U
            elif vehicle == 'TRAM':
                vehicles |= Vehicle.TRAM
            elif vehicle == 'BUS':
                bus = True
            elif vehicle == 'FERRY':
                vehicles |= Vehicle.FERRY
            elif vehicle == 'RB':
                vehicles |= Vehicle.RB
            elif vehicle == 'IC':
                vehicles |= Vehicle.IC
        limit = 9
        if args.limit:
            limit = args.limit

        if bus:
            aquery = ActualDepartureQueryApi(args.station)
        query = ScheduledDepartureQueryApi(args.station, vehicles, limit=limit)
        res = query.call()
        res2 = aquery.call()
        res.merge(res2)
    else:
        query = ActualDepartureQueryApi(args.station)
        res = query.call()

    if args.file in ('stdout', '-'):
        print(res.to_json, file=sys.stdout)
    else:
        file = open(args.file, 'w')
        print(res.to_json, file=file)
        file.close()
