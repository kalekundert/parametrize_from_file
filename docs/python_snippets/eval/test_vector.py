import vector
import parametrize_from_file

from pytest import approx
from parametrize_from_file import Namespace

# Define this object globally, because it will be useful for many tests.
with_vec = Namespace('from vector import *')

@parametrize_from_file
def test_dot(a, b, expected):
    a, b, expected = with_vec.eval(a, b, expected)
    assert dot(a, b) == approx(expected)
