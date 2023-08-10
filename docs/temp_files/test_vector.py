import vector
import parametrize_from_file as pff

with_vec = pff.Namespace('from vector import *')

@pff.parametrize(
        schema=[
            pff.cast(expected=with_vec.eval),
            pff.error_or('expected'),
        ],
        indirect=['tmp_files'],
)
def test_load(tmp_files, expected, error):
    with error:
        assert vector.load(tmp_files / 'vectors.txt') == expected
