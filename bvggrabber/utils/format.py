#-*- coding: utf-8 -*-


def fullformat(dt):
    """Formats a datetime object as YYYY-MM-DD HH:MM:SS

    :param datetime dt: The datetime.datetime object to format
    :return: A formattet string
    :rtype: str

    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def hourformat(dt):
    """Formats a datetime object as HH:MM

    :param datetime dt: The datetime.datetime object to format
    :return: A formattet string
    :rtype: str

    """
    return dt.strftime('%H:%M')


def int2bin(i, length=8):
    """Returns the bit representation of the given integer with a minimum
    length of ``length``. E.g. ``int2bin(109, 7) == '1101101'`` and
    ``int2bin(109, 8) == '01101101'.

    :param int i: The integer to format
    :param int length: The minimum length of the output string. The string is
        zero-padded on the left.
    :return: The bit representation of the given int
    :rtype: string

    """
    if not isinstance(length, int):
        raise ValueError("expected int for length")
    return ('{:0>' + str(length) + 'b}').format(i)
