import parametrize_from_file
from pytest import approx
from voluptuous import Schema
from parametrize_from_file.voluptuous import Namespace

with_vec = Namespace('from vector import *')

@parametrize_from_file(
        schema=Schema({
            'given': with_vec.eval,
            **with_vec.error_or({
                'expected': with_vec.eval,
            }),
        }),
)
def test_normalize(given, expected, error):
    with error:
        given.normalize()

        assert given.x == approx(expected.x)
        assert given.y == approx(expected.y)
