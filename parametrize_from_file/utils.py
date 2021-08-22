#!/usr/bin/env python3

from collections.abc import Iterable

def zip_with_scalars(*objs, strict=False, not_iterable=(str, bytes)):
    from builtins import zip
    from operator import itemgetter
    from more_itertools import zip_equal

    iterables = []
    formatters = []

    for obj in objs:
        if is_iterable(obj, not_iterable):
            formatters.append(itemgetter(len(iterables)))
            iterables.append(obj)
        else:
            # The double-lambdas are necessary to create a closure.
            formatters.append((lambda x: lambda _: x)(obj))

    if not iterables:
        if not objs:
            return
        else:
            yield tuple(objs)
            return

    if strict:
        zip = zip_equal

    for values in zip(*iterables):
        yield tuple(f(values) for f in formatters)

def is_iterable(obj, not_iterable=(str, bytes)):
    if not isinstance(obj, Iterable):
        return False
    if not_iterable and isinstance(obj, not_iterable):
        return False
    return True


