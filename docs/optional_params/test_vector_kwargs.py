import math
import vector
import parametrize_from_file
from pytest import approx
from parametrize_from_file import Namespace, cast, defaults

with_math = Namespace('from math import *')
with_vec = with_math.fork('from vector import *')

@parametrize_from_file(
        schema=[
            cast(
                angle=with_math.eval,
                kwargs=with_math.eval,
                expected=with_vec.eval,
            ),
            defaults(
                kwargs={},
            ),
        ],
)
def test_from_angle(angle, kwargs, expected):
    actual = vector.from_angle(angle, **kwargs)

    assert actual.x == approx(expected.x)
    assert actual.y == approx(expected.y)
