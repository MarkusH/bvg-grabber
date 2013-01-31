# -*- coding: utf-8 -*-
import datetime
import unittest

from bvggrabber.utils.format import int2bin, fullformat, dateformat, timeformat


class TestFormats(unittest.TestCase):

    def test_int2bin(self):
        nums = [(0b1101110, 7, '1101110'),
                (0b0010001, 7, '0010001'),
                (0b111111, 6, '111111'),
                (0b00000001, 8, '00000001'),
                (0b00111, 5, '00111'),
                (0b00111, 8, '00000111'),
                (0b1100011, 7, '1100011')]
        for b, l, s in nums:
            self.assertEqual(int2bin(b, l), s)

    def test_datetime_formats(self):
        f = [(datetime.datetime(2013, 1, 2, 3, 4, 0),
              "2013-01-02 03:04:00", "03:04", "02.01.2013"),
             (datetime.datetime(2013, 5, 2),
              "2013-05-02 00:00:00", "00:00", "02.05.2013"),
             (datetime.datetime(2013, 2, 2, 3, 4, 30),
              "2013-02-02 03:04:30", "03:04", "02.02.2013")]
        for dt, sf, st, sd in f:
            self.assertEqual(fullformat(dt), sf)
            self.assertEqual(dateformat(dt), sd)
            self.assertEqual(timeformat(dt), st)
