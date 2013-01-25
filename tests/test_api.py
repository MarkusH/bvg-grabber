# -*- coding: utf-8 -*-
import unittest

import datetime

from bvggrabber.api import QueryApi, Departure, fullformat


class TestQueryApi(unittest.TestCase):

    def test_call(self):
        q = QueryApi()
        self.assertRaises(NotImplementedError, q.call)


class TestDeparture(unittest.TestCase):

    def setUp(self):
        self.since = datetime.datetime(2013, 1, 2, 3, 4, 0)
        self.delta1 = datetime.timedelta(seconds=60)
        self.delta2 = datetime.timedelta(seconds=80)

    def test_timestamp_futur(self):
        when = self.since + self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 60)

        when = self.since + self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 120)

    def test_timestamp_now(self):
        when = self.since
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 0)

    def test_timestamp_past(self):
        when = self.since - self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, -60)

        when = self.since - self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, -120)

    def test_string_futur(self):
        when = fullformat(self.since + self.delta1)
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 60)

        when = fullformat(self.since + self.delta2)
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 120)

    def test_string_now(self):
        when = fullformat(self.since)
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 0)

    def test_string_past(self):
        when = fullformat(self.since - self.delta1)
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, -60)

        when = fullformat(self.since - self.delta2)
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, -120)

    def test_datetime_futur(self):
        when = self.since + self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 60)

        when = self.since + self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 120)

    def test_datetime_now(self):
        when = self.since
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, 0)

    def test_datetime_past(self):
        when = self.since - self.delta1
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, -60)

        when = self.since - self.delta2
        dep = Departure("from", "to", when, "line", since=self.since)
        diff = dep.remaining.total_seconds()
        self.assertEqual(diff, -120)

    def test_error(self):
        self.assertRaises(ValueError, Departure, "from", "to", "foo", "line")
