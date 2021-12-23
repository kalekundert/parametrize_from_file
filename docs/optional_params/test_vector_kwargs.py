import math
import vector
import parametrize_from_file
from pytest import approx
from voluptuous import Schema, Optional
from parametrize_from_file.voluptuous import Namespace

with_math = Namespace('from math import *')
with_vec = with_math.fork('from vector import *')

@parametrize_from_file(
        schema=Schema({
            'angle': with_math.eval,
            Optional('kwargs', default={}): with_math.eval,
            'expected': with_vec.eval,
        }),
)
def test_from_angle(angle, kwargs, expected):
    actual = vector.from_angle(angle, **kwargs)

    assert actual.x == approx(expected.x)
    assert actual.y == approx(expected.y)
