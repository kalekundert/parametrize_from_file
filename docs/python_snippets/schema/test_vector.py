import vector
import parametrize_from_file as pff
from pytest import approx

with_math = pff.Namespace('from math import *')
with_vec = pff.Namespace(with_math, 'from vector import *')

@pff.parametrize(
        # *expected* is just a number, so let the schema handle it.
        schema=pff.cast(expected=with_math.eval),
)
def test_dot(a, b, expected):
    # *a* and *b* are vectors, so instantiate them inside the test function.
    a, b = with_vec.eval(a, b)
    assert vector.dot(a, b) == approx(expected)
