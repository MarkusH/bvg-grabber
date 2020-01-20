# -*- coding: utf-8 -*-
import requests

import datetime

from bs4 import BeautifulSoup

from bvggrabber.api import QueryApi, Departure, Response, timeformat

from bvggrabber.utils.format import dateformat, int2bin


SCHEDULED_API_ENDPOINT = 'https://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox'


class Vehicle():

    S = 64
    U = 32
    TRAM = 16
    BUS = 8
    FERRY = 4
    RB = 2
    IC = 1

    _ALL = 127


class ScheduledDepartureQueryApi(QueryApi):

    def __init__(self, station, vehicles=Vehicle._ALL, limit=5):
        """:param Vehicle vehicles: a bitmask described by :class:`Vehicle`"""
        super(ScheduledDepartureQueryApi, self).__init__()
        if isinstance(station, str):
            self.station_enc = station.encode('iso-8859-1')
        elif isinstance(station, bytes):
            self.station_enc = station
        else:
            raise ValueError("Invalid type for station")
        self.station = station
        self.vehicles = int2bin(vehicles, 7)
        self.limit = limit

    def call(self):
        params = {'input': self.station_enc,
                  'time': timeformat(datetime.datetime.now()),
                  'date': dateformat(datetime.datetime.now()),
                  'productsFilter': self.vehicles,
                  'maxJourneys': self.limit,
                  'start': 'yes'}
        response = requests.get(SCHEDULED_API_ENDPOINT, params=params)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find('span', 'error'):
                # The station we are looking for is ambiguous or does not exist
                stations = soup.find('span', 'select').find_all('a')
                if stations:
                    # The station is ambiguous
                    stationlist = [s.text.strip() for s in stations]
                    return Response(False, stationlist)
                else:
                    # The station does not exist
                    return Response(False, [])
            else:
                # The station seems to exist
                tbody = soup.find('tbody')
                if tbody is None:
                    return Response(True, self.station, [])
                rows = tbody.find_all('tr')
                departures = []
                for row in rows:
                    tds = row.find_all('td')
                    if len(tds) != 3:
                        continue
                    dep = Departure(start=self.station,
                                    end=tds[2].text.strip(),
                                    when=tds[0].text.strip(),
                                    line=tds[1].text.strip())
                    departures.append(dep)
                return Response(True, self.station, departures)
        else:
            try:
                response.raise_for_status()
            except requests.RequestException as e:
                return Response(False, error=e)
            else:
                return Response(False,
                                error=Exception("An unknown error occured"))
