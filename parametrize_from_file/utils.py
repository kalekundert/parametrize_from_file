#!/usr/bin/env python3

from collections.abc import Iterable

def is_iterable(obj, not_iterable=(str, bytes)):
    if not isinstance(obj, Iterable):
        return False
    if not_iterable and isinstance(obj, not_iterable):
        return False
    return True


