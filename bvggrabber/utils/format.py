#-*- coding: utf-8 -*-

def int2bin(i, length):

    if not isinstance(length, int):
        raise ValueError("expected int for length")
    return ('{:0>' + str(length) + 'b}').format(i)
