# -*- coding: utf-8 -*-
import time
import unittest

from datetime import datetime, timedelta

from bvggrabber.api import QueryApi, Departure


class TestQueryApi(unittest.TestCase):

    def test_call(self):
        q = QueryApi()
        self.assertRaises(NotImplementedError, q.call)


class TestDeparture(unittest.TestCase):

    def setUp(self):
        self.td = timedelta(minutes=10)

    def test_timestamp_futur(self):
        when = time.time() + 10 * 60
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, 600)
        self.assertGreaterEqual(diff, 590)

    def test_timestamp_now(self):
        when = time.time()
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, 5)
        self.assertGreaterEqual(diff, -5)

    def test_timestamp_past(self):
        when = time.time() - 10 * 60
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, -600)
        self.assertGreaterEqual(diff, -610)

    def test_string_futur(self):
        when = datetime.now() + self.td
        when = when.strftime('%Y-%m-%d %H:%M:%S')
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, 600)
        self.assertGreaterEqual(diff, 590)

    def test_string_now(self):
        when = datetime.now()
        when = when.strftime('%Y-%m-%d %H:%M:%S')
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, 5)
        self.assertGreaterEqual(diff, -5)

    def test_string_past(self):
        when = datetime.now() - self.td
        when = when.strftime('%Y-%m-%d %H:%M:%S')
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, -600)
        self.assertGreaterEqual(diff, -610)

    def test_datetime_futur(self):
        when = datetime.now() + self.td
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, 600)
        self.assertGreaterEqual(diff, 590)

    def test_datetime_now(self):
        when = datetime.now()
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, 5)
        self.assertGreaterEqual(diff, -5)

    def test_datetime_past(self):
        when = datetime.now() - self.td
        dep = Departure("from", "to", when, "line")
        diff = dep.remaining.total_seconds()
        self.assertLessEqual(diff, -600)
        self.assertGreaterEqual(diff, -610)

    def test_error(self):
        self.assertRaises(ValueError, Departure, "from", "to", "foo", "line")
