import vector
import parametrize_from_file
from pytest import approx
from voluptuous import Schema
from parametrize_from_file.voluptuous import Namespace

# Define these objects globally, because they will be useful for many tests.
with_math = Namespace('from math import *')
with_vec = with_math.copy().use('from vector import *')

@parametrize_from_file(
        schema=Schema({
            'expected': with_math.eval,
            str: str,
        }),
)
def test_dot(a, b, expected):
    a, b = with_vec.eval(a, b)
    assert vector.dot(a, b) == approx(expected)
