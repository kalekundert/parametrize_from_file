import vector
import parametrize_from_file
from pytest import approx
from parametrize_from_file import Namespace, cast

# Define these objects globally, because they will be useful for many tests.
with_math = Namespace('from math import *')
with_vec = Namespace(with_math, 'from vector import *')

@parametrize_from_file(
        schema=cast(expected=with_math.eval),
)
def test_dot(a, b, expected):
    a, b = with_vec.eval(a, b)
    assert vector.dot(a, b) == approx(expected)
