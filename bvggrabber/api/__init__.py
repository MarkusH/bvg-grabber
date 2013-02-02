# -*- coding: utf-8 -*-
import datetime
import json
import re

from functools import total_ordering
from math import floor

from dateutil.parser import parse

from bvggrabber.utils.format import fullformat, timeformat


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

    def __init__(self, state, departures, error=None):
        self._state = state
        self._departures = departures
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
            self.when = parse(re.sub('[\s*]$', '', when))
            #if (self.when - self.now).total_seconds() < -60:
            #    self.when = self.when + timedelta(days=1)
        elif isinstance(when, datetime.datetime):
            self.when = when
        else:
            raise TypeError("when must be a valid datetime, timestamp or "
                            "string!")

    @property
    def remaining(self):
        return compute_remaining(self.now, self.when)

    @property
    def to_json(self):
        return json.dumps({'start': self.start,
                           'end': self.end,
                           'line': self.line,
                           'now_full': fullformat(self.now),
                           'now_hour': timeformat(self.now),
                           'when_full': fullformat(self.when),
                           'when_hour': timeformat(self.when),
                           'remaining': round(self.remaining)})

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
