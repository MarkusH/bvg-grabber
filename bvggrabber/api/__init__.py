# -*- coding: utf-8 -*-
import datetime
import json
import re

from functools import total_ordering
from math import floor

from dateutil.parser import parse

from bvggrabber.utils.format import fullformat, timeformat
from bvggrabber.utils.json import ObjectJSONEncoder


def compute_remaining(start, end):
    if not isinstance(start, datetime.datetime):
        raise ValueError("start needs to be a datetime.datetime")
    if not isinstance(end, datetime.datetime):
        raise ValueError("start needs to be a datetime.datetime")
    seconds = (end - start).total_seconds()
    return datetime.timedelta(minutes=floor(seconds / 60)).total_seconds()


class QueryApi(object):

    def __init__(self):
        pass

    def call(self):
        raise NotImplementedError("The inheriting class needs to implement "
                                  "the call() method!")


class Response(object):

    def __init__(self, state, station=None, departures=None, error=None):
        self._state = state
        self._departures = [(station, departures)]
        self._error = error

    def merge(self, other):
        if isinstance(other, Response):
            if not other.state:
                raise ValueError("The response contains errors: " + str(other.error))
            elif not self.state:
                raise ValueError("The response contains errors: " + str(self.error))
            else:
                self.departures.extend(other.departures)
        else:
            raise TypeError("The given object is not a response object")

    @property
    def to_json(self):
        return ObjectJSONEncoder(ensure_ascii=False).encode(self.departures)

    @property
    def state(self):
        return self._state

    @property
    def departures(self):
        return self._departures

    @property
    def error(self):
        return self._error


@total_ordering
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
            # We need to parse a string. But we need to remove trailing
            # whitespaces and *
            self.when = parse(re.sub('[\s*]$', '', when))
        elif isinstance(when, datetime.datetime):
            # Everything's fine, we can just take the parameter as is
            self.when = when
        else:
            raise TypeError("when must be a valid datetime, timestamp or "
                            "string!")
        diff = abs((self.when - self.now).total_seconds())
        if not no_add_day and self.when < self.now and diff > 43200:
            # 43200 are 12 hours in seconds So we accept a offset of 12 hours
            # that is still counted as "time gone" for the current day.
            self.when = self.when + datetime.timedelta(days=1)

    @property
    def remaining(self):
        return int(compute_remaining(self.now, self.when))

    def __eq__(self, other):
        """Two departures are assumed to be equal iff their remaining time
        and their destination are equal.

        Right now we do **not** considering the start or line, since that would
        require some kind of geo location in order to define a *total order*.
        """
        return ((self.remaining, self.end.lower()) ==
                (other.remaining, other.end.lower()))

    def __lt__(self, other):
        """A departure is assumed to be less than another iff its remaining
        time is less than the remaining time of the other departure.

        Right now we do **not** considering the start, end or line, since that
        would require some kind of geo location in order to define a *total
        order*.
        """
        return (self.remaining < other.remaining)

    def __str__(self):
        return "Start: %s, End: %s, when: %s, now: %s, line: %s" % (
            self.start, self.end, timeformat(self.when),
            timeformat(self.now), self.line)
