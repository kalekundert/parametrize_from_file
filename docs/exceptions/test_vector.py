import parametrize_from_file
from pytest import approx
from parametrize_from_file import Namespace, cast

with_vec = Namespace('from vector import *')

@parametrize_from_file(
        schema=[
            cast(
                given=with_vec.eval,
                expected=with_vec.eval,
            ),
            with_vec.error_or('expected'),
        ],
)
def test_normalize(given, expected, error):
    with error:
        given.normalize()

        assert given.x == approx(expected.x)
        assert given.y == approx(expected.y)
