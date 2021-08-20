import parametrize_from_file
from vector import Vector, dot
from pytest import approx

@parametrize_from_file
def test_dot(a, b, expected):
    a, b = Vector(*a), Vector(*b)
    assert dot(a, b) == approx(expected)

