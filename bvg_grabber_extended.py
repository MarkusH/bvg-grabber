# This file is part of BVG Grabber (3-clause BSD), see LICENSE

# Extended BVG Grabber
# Comibines grabbing of BVG schedules of multiple stations.

from bvggrabber.api.actualdeparture import ActualDepartureQueryApi
from bvggrabber.api.scheduleddeparture import ScheduledDepartureQueryApi
from bvggrabber.api import Response
from bvggrabber.utils.format import durationformat


# load the settings
exec(open('bvg_grabber_extended_config.py').read())


stationToMinReachSeconds = {}
for stat in stations:
    stationToMinReachSeconds[stat[0]] = stat[1]

stationToIndex = {}
stationIndex = 0
for stat in stations:
    stationToIndex[stat[0]] = stationIndex
    stationIndex += 1


def station_name_to_minReachSeconds(station_name):
    return(stationToMinReachSeconds[station_name])


def station_name_to_index(station_name):
    return(stationToIndex[station_name])


def get_data():

    stationIndex = 0
    # fetch from the first station
    responses = get_station_data(stations[stationIndex][0])
    stationIndex += 1

    # fetch from the remaining stations, if there are any
    while stationIndex < len(stations):
        responsesNew = get_station_data(stations[stationIndex][0])
        responses.merge(responsesNew)
        stationIndex += 1

    return responses


def get_station_data(station):

    query = ScheduledDepartureQueryApi(station, vehicles, grab_departures_limit, json_parser = json_parser)
    res = query.call()
    if bus:
        aquery = ActualDepartureQueryApi(station, grab_departures_limit, json_parser = json_parser)
        res2 = aquery.call()
        res.merge(res2)

    return res


def line_simplifier(line):
    return line.replace('Bus  ', '')


def location_simplifier(location):
    return location.replace(' (Berlin)', '').replace('S+U ', '').replace('S ', '').replace('U ', '')


def duration_humanizer(seconds):
    if seconds == 0:
        durationStr = 'now '
    else:
        durationStr = durationformat(seconds)
    return durationStr


def leaves_too_soon(departure):

    minReachSecs = station_name_to_minReachSeconds(departure.start)
    return(departure.remaining < minReachSecs)


def leaves_too_late(departure):

    minReachSecs = station_name_to_minReachSeconds(departure.start)
    return(departure.remaining > (minReachSecs + maxWaitSecs))
