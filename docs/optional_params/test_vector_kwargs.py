import vector
import parametrize_from_file as pff
from pytest import approx

with_math = pff.Namespace('from math import *')
with_vec = pff.Namespace(with_math, 'from vector import *')

@pff.parametrize(
        schema=[
            pff.cast(
                angle=with_math.eval,
                kwargs=with_math.eval,
                expected=with_vec.eval,
            ),
            pff.defaults(
                kwargs={},
            ),
        ],
)
def test_from_angle(angle, kwargs, expected):
    actual = vector.from_angle(angle, **kwargs)

    assert actual.x == approx(expected.x)
    assert actual.y == approx(expected.y)
