# -*- coding: utf-8 -*-
import datetime
import json
import unittest

from bvggrabber.api import QueryApi, Departure, fullformat, \
    compute_remaining


class TestFunctions(unittest.TestCase):

    def test_compute_remaining(self):
        dates = [datetime.datetime(2013, 1, 2, 3, 4, 0),
                 datetime.datetime(2013, 1, 2, 3, 4, 1),
                 datetime.datetime(2013, 1, 2, 3, 4, 59),
                 datetime.datetime(2013, 1, 2, 3, 5, 0),
                 datetime.datetime(2013, 1, 2, 3, 5, 1),
                 datetime.datetime(2013, 1, 2, 3, 5, 59)]

        target = [[0, 0, 0, 60, 60, 60],
                  [-60, 0, 0, 0, 60, 60],
                  [-60, -60, 0, 0, 0, 60],
                  [-60, -60, -60, 0, 0, 0],
                  [-120, -60, -60, -60, 0, 0],
                  [-120, -120, -60, -60, -60, 0]]
        for start in range(len(dates)):
            for end in range(len(dates)):
                s = dates[start]
                e = dates[end]
                t = target[start][end]
                self.assertEqual(compute_remaining(s, e),
                                 target[start][end],
                                 "Start: %s; End: %s; target: %d" % (
                                     fullformat(s), fullformat(e), t))

    def test_compute_remaining_error(self):
        self.assertRaises(ValueError, compute_remaining,
                          1357092240, datetime.datetime(2013, 1, 2, 3, 4, 1))
        self.assertRaises(ValueError, compute_remaining,
                          datetime.datetime(2013, 1, 2, 3, 4, 0), 1357092241)
        self.assertRaises(ValueError, compute_remaining,
                          1357092240, 1357092241)


class TestQueryApi(unittest.TestCase):

    def test_call(self):
        q = QueryApi()
        self.assertRaises(NotImplementedError, q.call)


class BaseTestDeparture(unittest.TestCase):

    def setUp(self):
        self.since = datetime.datetime(2013, 1, 2, 3, 4, 0)
        self.delta1 = datetime.timedelta(seconds=45)
        self.delta2 = datetime.timedelta(seconds=80)
        self.delta3 = datetime.timedelta(seconds=150)


class TestDepartureTimestamp(BaseTestDeparture):

    def setUp(self):
        super(TestDepartureTimestamp, self).setUp()
        self.sincets = 1357092240
        self.since = datetime.datetime.fromtimestamp(self.sincets)
        self.delta1 = self.delta1.total_seconds()
        self.delta2 = self.delta2.total_seconds()
        self.delta3 = self.delta3.total_seconds()

    def test_timestamp_futur(self):
        when = self.sincets + self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 0)

        when = self.sincets + self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 60)

        when = self.sincets + self.delta3
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 120)

    def test_timestamp_now(self):
        when = self.sincets
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 0)

    def test_timestamp_past(self):
        when = self.sincets - self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -60)

        when = self.sincets - self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -120)

        when = self.sincets - self.delta3
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -180)


class TestDepartureString(BaseTestDeparture):

    def test_string_futur(self):
        when = fullformat(self.since + self.delta1)
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 0)

        when = fullformat(self.since + self.delta2)
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 60)

        when = fullformat(self.since + self.delta3)
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 120)

    def test_string_now(self):
        when = fullformat(self.since)
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 0)

    def test_string_past(self):
        when = fullformat(self.since - self.delta1)
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -60)

        when = fullformat(self.since - self.delta2)
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -120)

        when = fullformat(self.since - self.delta3)
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -180)


class TestDepartureDatetime(BaseTestDeparture):

    def test_datetime_futur(self):
        when = self.since + self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 0)

        when = self.since + self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 60)

        when = self.since + self.delta3
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 120)

    def test_datetime_now(self):
        when = self.since
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, 0)

    def test_datetime_past(self):
        when = self.since - self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -60)

        when = self.since - self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -120)

        when = self.since - self.delta3
        dep = Departure("from", "to", when, "line", since=self.since)
        self.assertEqual(dep.remaining, -180)


class TestDeparture(BaseTestDeparture):

    def test_error(self):
        self.assertRaises(ValueError, Departure, "from", "to", "when", "line")
        self.assertRaises(TypeError, Departure, "from", "to", ["when"], "line")
        self.assertIsInstance(Departure("from", "to", "16:15\n \t*", "line"),
                              Departure)

    def test_json(self):
        json1 = {'start': "From My Station",
                 'end': "To Your Station",
                 'line': "A Line",
                 'now_full': "2013-01-02 03:04:00",
                 'now_hour': "03:04",
                 'when_full': "2013-01-02 03:04:45",
                 'when_hour': "03:04",
                 'remaining': 0}
        dep1 = Departure("From My Station", "To Your Station",
                         self.since + self.delta1, "A Line", since=self.since)
        self.assertEqual(json1, json.loads(dep1.to_json))
        str1 = "Start: From My Station, End: To Your Station, when: 03:04, " \
               "now: 03:04, line: A Line"
        self.assertEqual(str1, str(dep1))

        json2 = {'start': "From My Station",
                 'end': "To Your Station",
                 'line': "A Line",
                 'now_full': "2013-01-02 03:04:00",
                 'now_hour': "03:04",
                 'when_full': "2013-01-02 03:05:20",
                 'when_hour': "03:05",
                 'remaining': 60}
        dep2 = Departure("From My Station", "To Your Station",
                         self.since + self.delta2, "A Line", since=self.since)
        self.assertEqual(json2, json.loads(dep2.to_json))
        str2 = "Start: From My Station, End: To Your Station, when: 03:05, " \
               "now: 03:04, line: A Line"
        self.assertEqual(str2, str(dep2))
