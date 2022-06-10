import vector
import parametrize_from_file
from parametrize_from_file import Namespace, cast, error_or

with_py = Namespace()
with_vec = Namespace('from vector import *')

@parametrize_from_file(
        schema=[
            cast(expected=with_vec.eval),
            error_or('expected'),
        ],
        indirect=['tmp_files'],
)
def test_load(tmp_files, expected, error):
    with error:
        assert vector.load(tmp_files / 'vectors.txt') == expected
