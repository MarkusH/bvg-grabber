# -*- coding: utf-8 -*-
import requests

import datetime

from bs4 import BeautifulSoup

from bvggrabber.api import QueryApi, Departure


SCHEDULED_QUERY_API_ENDPOINT = 'http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox'


class Vehicle():

    S = 1
    U = 2
    TRAM = 4
    BUS = 8
    FERRY = 16
    RB = 32
    IC = 64

    _ALL = 127


class ScheduledDepartureQueryApi(QueryApi):

    def __init__(self, station, vehicles=Vehicle._ALL, limit=5):
        super(ScheduledDepartureQueryApi, self).__init__()
        if isinstance(station, str):
            self.station_enc = station.encode('iso-8859-1')
        elif isinstance(station, bytes):
            self.station_enc = station
        else:
            raise ValueError("Invalid type for station")
        self.station = station
        self.vehicles = bin(vehicles)[2:]
        self.limit = limit

    def call(self):

        params = {'input': self.station_enc, 'time': datetime.datetime.now().strftime('%H:%M'), 'date': datetime.datetime.now().strftime('%d.%m.%Y'),'productsFilter': self.vehicles, 'maxJourneys': self.limit, 'start': 'yes'}
        response = requests.get(SCHEDULED_QUERY_API_ENDPOINT, params=params)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.text)
            if soup.find('span', 'error'):
                # The station we are looking for is ambiguous or does not exist
                stations = soup.find('span', 'select').find_all('a')
                if stations:
                    # The station is ambiguous
                    stationlist = [s.text.strip() for s in stations]
                    return (False, stationlist)
                else:
                    # The station does not exist
                    return (False, [])
            else:
                # The station seems to exist
                tbody = soup.find('tbody')
                if tbody is None:
                    return (False, [])
                rows = tbody.find_all('tr')
                departures = []
                for row in rows:
                    tds = row.find_all('td')
                    dep = Departure(start=self.station,
                                    end=tds[2].text.strip(),
                                    when=tds[0].text.strip(),
                                    line=tds[1].text.strip())
                    departures.append(dep)
                return (True, departures)
        else:
            response.raise_for_status()
