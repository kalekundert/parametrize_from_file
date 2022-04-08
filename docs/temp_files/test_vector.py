import vector
import parametrize_from_file

from voluptuous import Schema
from parametrize_from_file.voluptuous import Namespace

with_py = Namespace()
with_vec = Namespace('from vector import *')

@parametrize_from_file(
        schema=Schema({
            'tmp_files': {str: str},
            **with_py.error_or({
                'expected': with_vec.eval,
            }),
        }),
        indirect=['tmp_files'],
)
def test_load(tmp_files, expected, error):
    with error:
        assert vector.load(tmp_files / 'vectors.txt') == expected
