# -*- coding: utf-8 -*-
import unittest

from datetime import datetime

from bvggrabber.api import QueryApi, Departure


class TestQueryApi(unittest.TestCase):

    def test_call(self):
        q = QueryApi()
        self.assertRaises(NotImplementedError, q.call)


class TestDeparture(unittest.TestCase):

    def test_timestamp_futur(self):
        when = datetime.now()
        when = when.replace(minute=when.minute + 10)
        when = when.timestamp()
        dep = Departure("from", "to", when, "line")
        self.assertLessEqual(dep.remaining().total_seconds(), 600)
        self.assertGreaterEqual(dep.remaining().total_seconds(), 590)

    def test_string_futur(self):
        when = datetime.now()
        when = when.replace(minute=when.minute + 10)
        when = when.strftime('%Y-%m-%d %H:%M:%S')
        dep = Departure("from", "to", when, "line")
        self.assertLessEqual(dep.remaining().total_seconds(), 600)
        self.assertGreaterEqual(dep.remaining().total_seconds(), 590)

    def test_datetime_futur(self):
        when = datetime.now()
        when = when.replace(minute=when.minute + 10)
        dep = Departure("from", "to", when, "line")
        self.assertLessEqual(dep.remaining().total_seconds(), 600)
        self.assertGreaterEqual(dep.remaining().total_seconds(), 590)

    def test_error(self):
        self.assertRaises(ValueError, Departure, "from", "to", "foo", "line")
