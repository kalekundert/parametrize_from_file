import vector
import parametrize_from_file as pff
from pytest import approx

with_math = pff.Namespace('from math import *')
with_vec = pff.Namespace(with_math, 'from vector import *')

@pff.parametrize(
        schema=[
            pff.cast(
                angle=with_math.eval,
                magnitude=with_math.eval,
                expected=with_vec.eval,
            ),
            pff.defaults(
                unit='deg',
                magnitude=1,
            ),
        ],
)
def test_from_angle(angle, unit, magnitude, expected):
    actual = vector.from_angle(angle, unit=unit, magnitude=magnitude)

    assert actual.x == approx(expected.x)
    assert actual.y == approx(expected.y)
