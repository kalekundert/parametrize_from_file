import vector
import parametrize_from_file as pff
from pytest import approx

# Define this object globally, because it is immutable and will be useful for 
# many tests.
with_vec = pff.Namespace('from vector import *')

@pff.parametrize
def test_dot(a, b, expected):
    a, b, expected = with_vec.eval(a, b, expected)
    assert vector.dot(a, b) == approx(expected)
