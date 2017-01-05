#-*- coding: utf-8 -*-

from datetime import timedelta
from math import floor

def dateformat(dt):
    """Formats a :class:`datetime.datetime` object as dd.mm.yyyy

    :param datetime.datetime dt: The :class:`datetime.datetime` object to
        format
    :return: A formatted string
    :rtype: str

    """
    return dt.strftime('%d.%m.%Y')


def fullformat(dt):
    """Formats a :class:`datetime.datetime` object as YYYY-MM-DD HH:MM:SS

    :param datetime.datetime dt: The :class:`datetime.datetime` object to
        format
    :return: A formatted string
    :rtype: str

    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def int2bin(i, length=8):
    """Returns the bit representation of the given integer with a minimum
    length of ``length``. E.g. ``int2bin(109, 7) == '1101101'`` and
    ``int2bin(109, 8) == '01101101'``.

    :param int i: The integer to format
    :param int length: The minimum length of the output string. The string is
        zero-padded on the left.
    :return: The bit representation of the given int
    :rtype: string

    """
    if not isinstance(length, int):
        raise ValueError("expected int for length")
    return ('{:0>' + str(length) + 'b}').format(i)


def timeformat(dt):
    """Formats a :class:`datetime.datetime` object as HH:MM

    :param datetime.datetime dt: The :class:`datetime.datetime` object to
        format
    :return: A formatted string
    :rtype: str

    """
    return dt.strftime('%H:%M')


def durationformat(seconds):
    """Formats a value in seconds (positive or negative) into a human readable duration,
    for example: 125 -> "2m 5s".

    @param int seconds
    @return: A formatted duration time
    @rtype: str
    """
    if seconds < 0:
        seconds = seconds * -1;
        prefix = '-('
        suffix = ')'
    else:
        prefix = '  '
        suffix = ' '
    # here we may switch between variant1 and variant2
    return prefix + durationformat_positive_variant2(seconds = seconds) + suffix


def durationformat_positive_variant1(seconds):
    """
    Takes an amount of seconds,
    and turns it into a human-readable amount of time.
    This creates slightly longer strings then variant2.
    for example: 125 -> "2min 5s".

    @param int seconds
    @return: A formatted duration time
    @rtype: str
    """
    return timedelta(seconds = seconds).__str__()


def durationformat_positive_variant2(seconds, suffixes=['y','w','d','h','m','s'], add_s=False, separator=' '):
    """
    Takes an amount of seconds,
    and turns it into a human-readable amount of time.
    This creates slightly shorter strings then variant1.
    for example: 125 -> "2m 5s".

    @param int seconds (must be positive!)
    @return: A formatted duration time
    @rtype: str
    """
    # the formatted time string to be returned
    time = []

    # the pieces of time to iterate over (days, hours, minutes, etc)
    # - the first piece in each tuple is the suffix (d, h, w)
    # - the second piece is the length in seconds (a day is 60s * 60m * 24h)
    parts = [(suffixes[0], 60 * 60 * 24 * 7 * 52),
          (suffixes[1], 60 * 60 * 24 * 7),
          (suffixes[2], 60 * 60 * 24),
          (suffixes[3], 60 * 60),
          (suffixes[4], 60),
          (suffixes[5], 1)]

    # for each time piece, grab the value and remaining seconds, and add it to
    # the time string
    for suffix, length in parts:
        value = floor(seconds / length)
        if value > 0:
            seconds = seconds % length
            time.append('%s%s' % (str(value),
                           (suffix, (suffix, suffix + 's')[value > 1])[add_s]))
        if seconds < 1:
            break

    return separator.join(time)
