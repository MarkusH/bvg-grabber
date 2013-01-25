# -*- coding: utf-8 -*-
import datetime
import json
import re

from math import ceil, floor
from dateutil.parser import parse


fullformat = lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
hourformat = lambda dt: dt.strftime('%H:%M')


class QueryApi(object):

    def __init__(self):
        pass

    def call(self):
        raise NotImplementedError("The inheriting class needs to implement "
                                  "the call() method!")


class Departure(object):

    def __init__(self, start, end, when, line, since=None):
        if since is None:
            self.now = datetime.datetime.now()
        else:
            self.now = since
        self.start = start
        self.end = end
        self.line = line
        if isinstance(when, (int, float)):
            # We assume to get a UNIX / POSIX timestamp
            self.when = datetime.datetime.fromtimestamp(when)
        elif isinstance(when, str):
            self.when = parse(re.sub('[\s*]$', '', when))
            #if (self.when - self.now).total_seconds() < -60:
            #    self.when = self.when + timedelta(days=1)
        elif isinstance(when, datetime.datetime):
            self.when = when
        else:
            ValueError("when must be a valid datetime, timestamp or string!")

    def __str__(self):
        return "Start: %s, End: %s, when: %s, now: %s, line: %s" % (
            self.start, self.end, hourformat(self.when), hourformat(self.now),
            self.line)

    @property
    def remaining(self):
        td = self.when - self.now
        seconds = (td / 60).total_seconds()
        if td < datetime.timedelta(seconds=0):
            return datetime.timedelta(minutes=floor(seconds))
        elif td > datetime.timedelta(seconds=0):
            return datetime.timedelta(minutes=ceil(seconds))
        else:
            return datetime.timedelta(seconds=0)

    def to_json(self):
        return json.dumps({'start': self.start.decode('iso-8859-1'),
                           'end': self.end,
                           'line': self.line,
                           'now_full': fullformat(self.now),
                           'now_hour': hourformat(self.now),
                           'when_full': fullformat(self.when),
                           'when_hour': hourformat(self.when),
                           'remaining': round(self.remaining.total_seconds())})
