# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.parser import parse


fullformat = lambda dt: dt.strftime('%Y-%m-%d %H:%M')


class QueryApi():

    def __init__(self):
        pass

    def call(self):
        raise NotImplementedError("The inheriting class needs to implement "
                                  "the call() method!")


class Departure():

    def __init__(self, start, end, when, line):
        self.start = start
        self.end = end
        if isinstance(when, (int, float)):
            # We assume to get a UNIX timestamp
            self.when = datetime.fromtimestamp(when)
        elif isinstance(when, str):
            self.when = parse(when)
            now = datetime.now()
            if (self.when - now).total_seconds() < 0:
                self.when = self.when.replace(day=self.when.day + 1)
        elif isinstance(when, datetime):
            self.when = when
        else:
            ValueError("when must be a valid datetime, timestamp or string!")
        self.line = line

    def __str__(self):
        return "Start: %s, End: %s, when: %s, line: %s" % (
            self.start, self.end, fullformat(self.when), self.line)

    def remaining(self):
        return self.when - datetime.now()

    def to_json(self):
        pass
