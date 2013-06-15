# -*- coding: utf-8 -*-
import datetime
import re

from functools import total_ordering
from math import floor

from dateutil.parser import parse

from bvggrabber.utils.format import timeformat
from bvggrabber.utils.json import ObjectJSONEncoder


def compute_remaining(start, end):
    """Compute the number of seconds between ``start`` and ``end`` and return
    the number of seconds rounded down to entire minutes. That means:

    * [0, 59] => 0
    * [60, 119] => 60
    * [120, 179] => 120
    * [-59, -1] => -60
    * [-119, -60] => -120

    :param datetime.datetime start: The start to compute the remaining number
        of minutes.
    :param datetime.datetime end: The end of the interval
    :raises: TypeError if either of ``start`` or ``end`` is not a
        ``datetime.datetime``.
    :return: The number of remaining seconds rounded to entire minutes
    :rtype: int
    """
    if not isinstance(start, datetime.datetime):
        raise TypeError("start needs to be a datetime.datetime")
    if not isinstance(end, datetime.datetime):
        raise TypeError("start needs to be a datetime.datetime")
    seconds = (end - start).total_seconds()
    return datetime.timedelta(minutes=floor(seconds / 60)).total_seconds()


class QueryApi(object):

    def __init__(self):
        pass

    def call(self):
        """Needs to be implemented by inheriting classes!"""
        raise NotImplementedError("The inheriting class needs to implement "
                                  "the call() method!")


class Response(object):

    def __init__(self, state, station=None, departures=None, error=None):
        """Creates a new response. Returned by :meth:`QueryApi.call`
        
        :param bool state: ``True`` iff the request and parsing was successful,
            ``False`` otherwise.
        :param station: If a ``list``, the station name is ambiguous. If a
            string the full qualified name of the station.
        :param departures: A list of :class:`Departure`` objects
        :param Exception error: In case an unexpected error occurred, this
            contains the original exception.

        If ``state`` is ``True``, ``station`` must be a ``str`` and
        ``departures`` must be a list of :class:`Departure`` objects. If
        ``state`` is ``False`` there must be several reasons for that:

            1. The provided station name during the :meth:`QueryApi.call`
               returned multiple possible departing stations. You have to
               specify the name in an unambiguous way.
            2. The station does not exist at all.
            3. An exception occurred during the :meth:`QueryApi.call`

        .. deprecated:: 0.1b3
           The ``state`` argument will be removed in the future and will be
           computed automatically based on ``station``, ``departures`` and
           ``error``.
        """
        self._state = state
        self._departures = [(station, departures)]
        self._error = error
        if self._error is None:
            if isinstance(station, list):
                self._state = False
                msg = ', '.join(station)
                self._error = Exception("Station is ambiguous: %s" % msg)
            elif station is None:
                self._state = False
                self._error = Exception("Station does not exist")
        elif isinstance(self._error, str):
            self._state = False
            self._error = Exception(self._error)

    def merge(self, other):
        """Checks that ``other`` is a :class:`Response` and extends
        :attr:`departures` by the departures given in ``other`` iff neither
        response object has a invalid state.
        """
        if isinstance(other, Response):
            if not other.state:
                raise ValueError("The response contains errors: " +
                                 str(other.error))
            elif not self.state:
                raise ValueError("The response contains errors: " +
                                 str(self.error))
            else:
                self.departures.extend(other.departures)
        else:
            raise TypeError("The given object is not a response object")

    @property
    def to_json(self):
        """.. deprecated:: 0.0.1
           Use :attr:`json` instead.
        """
        return ObjectJSONEncoder(ensure_ascii=False).encode(self.departures)

    @property
    def departures(self):
        """A list of 2-tuple in the form (:class:`str`, :class:`Departure`).
        The first element in the tuple defines the departing station where the
        second element holds a list of departure objects.
        """
        if self.state:
            return self._departures
        return str(self.error)

    @property
    def error(self):
        """The error that occurred during creation or ``None``"""
        return self._error

    @property
    def json(self):
        """Uses :class:`~bvggrabber.utils.json.ObjectJSONEncoder` to encode
        the :attr:`departures` to a JSON format.
        """
        if self.state:
            return ObjectJSONEncoder(ensure_ascii=False).encode(self.departures)
        return ObjectJSONEncoder(ensure_ascii=False).encode(str(self.error))

    @property
    def state(self):
        """``True`` iff the request and parsing was successful, ``False``
        otherwise.
        """
        return self._state


@total_ordering
class Departure(object):

    def __init__(self, start, end, when, line, since=None, no_add_day=False):
        """
        :param str start: The start station
        :param str end: The end station
        :param when: The leaving time of the public transport at the given
            ``start`` station. Might be an :class:`int` (timestamp), a
            :class:`datetime.datetime` instance or a :class:`str` accepted by
            ``dateutil.parse()``. If ``when`` is smaller than ``since`` and the
            difference between both times is larger than 12 hours (43200sec),
            the API will add another day unless ``no_add_day`` is ``True``.
        :param str line: The line of the public transport
        :param since: Either ``None`` or :class:`datetime.datetime`. Defines
            the temporal start for searching. ``None`` will internally be
            resolved as :meth:`datetime.datetime.now`.
        :param bool no_add_day: If true, there no additional day will be added
            if ``when`` is smaller than ``since``. Default ``False``.
        :raises: :exc:`TypeError` if ``when`` is invalid or cannot be parsed.
        """
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
        """.. seealso:: bvggrabber.api.compute_remaining"""
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

    def __repr__(self):
        return self.__str__()
