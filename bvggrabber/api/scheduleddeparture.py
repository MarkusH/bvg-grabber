# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup

from bvggrabber.api import QueryApi, Departure

SCHEDULE_QUERY_API_ENDPOINT = 'http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox'


class ScheduleDepartureQueryApi(QueryApi):

    def __init__(self, station):
        super(ScheduleDepartureQueryApi, self).__init__()
        if isinstance(station, str):
            self.station_enc = station.encode('iso-8859-1')
        elif isinstance(station, bytes):
            self.station_enc = station
        else:
            raise ValueError("Invalid type for station")
        self.station = station

    def call(self):
        params = {'input': self.station_enc, 'time': '12:00', 'date': '25.01.2013','productsFilter': 11, 'maxJourneys': 7, 'start': 'yes'}
        response = requests.get(SCHEDULE_QUERY_API_ENDPOINT, params=params)
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
                #rows = soup.find('tbody').find_all('tr')
                rows = soup.find('tbody').find_all('tr')
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
