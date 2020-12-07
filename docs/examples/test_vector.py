#!/usr/bin/env python3

import parametrize_from_file
from vector import Vector, dot
from pytest import approx
from voluptuous import Schema

local_eval = lambda x: eval(x)

@parametrize_from_file(schema=Schema({str: local_eval}))
def test_dot(a, b, expected):
    assert dot(a, b) == approx(expected)

