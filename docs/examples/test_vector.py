#!/usr/bin/env python3

import parametrize_from_file
from pytest import approx
from vector import Vector, dot
from schema import Use

local_eval = lambda x: eval(x)

@parametrize_from_file(schema={str: Use(local_eval)})
def test_dot(a, b, expected):
    assert dot(a, b) == approx(expected)

