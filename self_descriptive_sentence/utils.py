# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import sys


def unicodefy_std_io():
    sys.stdin = codecs.getreader(sys.stdin.encoding or sys.getfilesystemencoding())(sys.stdin)
    sys.stdout = codecs.getwriter(sys.stdout.encoding or sys.getfilesystemencoding())(sys.stdout)
    sys.stderr = codecs.getwriter(sys.stdout.encoding or sys.getfilesystemencoding())(sys.stderr)


def enumerate_digits(number):
    """
    :type number: int | long
    :rtype: collections.Iterable[int, int]
    """
    position = 0
    while number > 0:
        digit = number % 10
        number //= 10
        yield position, digit
        position += 1
