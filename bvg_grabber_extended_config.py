# This file is part of BVG Grabber (3-clause BSD), see LICENSE

# Extended BVG Grabber configuration
# See `bvg_grabber_extended.py` for more info.

from bvggrabber.api.scheduleddeparture import Vehicle

# commonly used stations
# these have to be BVG compatible (you may test by using bvg.de manually,
# when adding new entries)
# NOTE you may only use station names here, not addresses
# (unlike with the bvg.de webinterface)
station_TE = 'Tempelhof'
station_ERP = 'U Ernst-Reuter-Platz (Berlin)'
station_Zoo = 'S+U Zoologischer Garten'
station_MAR = 'Marchbrücke (Berlin)'

# sets of close-by stations, and how long it takes to get there in seconds.
# each line represents a location
stations_EB104 = [[station_ERP, 5 * 60]]
stations_FREITAGSRUNDE_WALK = [[station_MAR, 1 * 60], [station_ERP, 10 * 60]]
stations_FREITAGSRUNDE = [[station_MAR, 1 * 60]]

# choose one set to be actually used
stations = stations_FREITAGSRUNDE

# how long one would be willing to wait at most for a connection,
# after reaching the station [seconds]
# default: 60 * 60 # = 1h
maxWaitSecs = 60 * 60

# all the types of vehicles to consider while grabbing data
vehicles = 0
vehicles |= Vehicle.S
vehicles |= Vehicle.U
vehicles |= Vehicle.TRAM
bus = True
vehicles |= Vehicle.FERRY
vehicles |= Vehicle.RB
vehicles |= Vehicle.IC

# maximum number of entries to request when grabbing.
# as we might do up to two grabs per station (scheduled and actual),
# this might be exceeded, while post filtering may decrease it again.
# thus you should consider this only as a rough indication
# it also seems to stall the fetching process, when it exceeds a certain value.
# for example, 20 seems to be too much.
grab_departures_limit = 10

# choose automatically
json_parser = None
# set fixed.
# NOTE This is usually necessary to prevent a nasty warning message,
#   which gets printed to the terminal, messing with the curses GUI.
#   If the library given here is unavailable on your system,
#   comment this line temporarily, and the mentioned error message will
#   tell you which value to use here.
json_parser = 'html5lib'
