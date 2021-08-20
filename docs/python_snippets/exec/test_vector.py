import vector
import parametrize_from_file

with_vec = Namespace("from vector import *")

@parametrize_from_file
def test_to_vector(given, expected):
    given = with_vec.exec(given)['obj']
    converted = vector.to_vector(given)
    expected = with_vec.eval(expected)

    assert converted.x == expected.x
    assert converted.y == expected.y
