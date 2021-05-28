# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup

from bvggrabber.api import QueryApi, Departure, Response


ACTUAL_API_ENDPOINT = 'https://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?ld=0.1&boardType=depRT&'


class ActualDepartureQueryApi(QueryApi):

    def __init__(self, station, limit=5):
        super(ActualDepartureQueryApi, self).__init__()
        if isinstance(station, str):
            self.station_enc = station.encode('iso-8859-1')
        elif isinstance(station, bytes):
            self.station_enc = station
        else:
            raise ValueError("Invalid type for station")
        self.station = station
        self.limit = limit

    def call(self):
        params = {
            'input': self.station_enc,
            'maxJourneys': self.limit,
            'start': 'suchen',
        }
        response = requests.get(ACTUAL_API_ENDPOINT, params=params)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find_all('form'):
                # The station we are looking for is ambiguous or does not exist
                stations = soup.find_all('option')
                if stations:
                    # The station is ambiguous
                    stationlist = [s.get('value') for s in stations]
                    return Response(False, stationlist)
                else:
                    # The station does not exist
                    return Response(False)
            else:
                # The station seems to exist
                result = soup.find('table', {'id': '',
                                           'class': 'ivu_table'})
                if result is None:
                    return Response(True, self.station, [])
                rows = result.find_all('tr')
                departures = []
                for row in rows:
                    if row.parent.name == 'tbody':
                        td = row.find_all('td')
                        if len(td) != 3:
                            continue
                        if td:
                            dep = Departure(start=self.station,
                                            end=td[2].text.strip(),
                                            when=td[0].text.strip(),
                                            line=td[1].text.strip())
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
