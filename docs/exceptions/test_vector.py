import parametrize_from_file as pff
from pytest import approx

with_vec = pff.Namespace('from vector import *')

@pff.parametrize(
        schema=[
            pff.cast(
                given=with_vec.eval,
                expected=with_vec.eval,
            ),
            pff.error_or('expected', globals=with_vec),
        ],
)
def test_normalize(given, expected, error):
    with error:
        given.normalize()

        assert given.x == approx(expected.x)
        assert given.y == approx(expected.y)
