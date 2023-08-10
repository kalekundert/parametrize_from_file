import vector
import parametrize_from_file as pff

with_vec = pff.Namespace("from vector import *")

@pff.parametrize
def test_to_vector(given, expected):
    given = with_vec.exec(given)['obj']
    converted = vector.to_vector(given)
    expected = with_vec.eval(expected)

    assert converted.x == expected.x
    assert converted.y == expected.y
