# -*- coding: utf-8 -*-
"""
Used for beehive as compatibility layer between different Python versions
and implementations.
"""

try:
    unicode = unicode
except NameError:
    unicode = str
    basestring = (str, bytes)
    long = int
else:
    bytes = str
    basestring = basestring
    long = long
