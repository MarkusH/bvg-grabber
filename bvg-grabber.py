#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from bvggrabber.api.actualdeparture import ActualDepartureQueryApi

from bvggrabber.api.scheduleddeparture import ScheduledDepartureQueryApi, Vehicle


if __name__ == '__main__':

    vehicle_choices = ('S', 'U', 'TRAM', 'BUS', 'FERRY', 'RB', 'IC')

    parser = argparse.ArgumentParser(
        description='Query the BVG-website for departures')
    parser.add_argument('station', type=str, help='The station to query')
    parser.add_argument('file', type=str, help='Path to file. Use - for stdout')
    parser.add_argument('--vehicle', type=str, nargs='*',
                        choices=vehicle_choices,
                        help='Vehicles which shall be queried, if non given '
                             'actualdepartue (bus) will be used')
    parser.add_argument('--limit', type=int, default=9,
                        help='Max departures to query. Default: 9')
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

        query = ScheduledDepartureQueryApi(args.station, vehicles, limit=args.limit)
        res = query.call()
        if bus:
            aquery = ActualDepartureQueryApi(args.station, limit=args.limit)
            res2 = aquery.call()
            res.merge(res2)
    else:
        query = ActualDepartureQueryApi(args.station, limit=args.limit)
        res = query.call()

    if args.file in ('stdout', '-'):
        print(res.to_json)
    else:
        with open(args.file, 'w') as f:
            print(res.to_json, file=f)