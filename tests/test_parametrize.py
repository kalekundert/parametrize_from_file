#!/usr/bin/env python3

import pytest
import parametrize_from_file as pff
import parametrize_from_file.parametrize as pffp
from unittest.mock import Mock
from voluptuous import Schema
from pathlib import Path

pytest_plugins = ['pytester']
TEST_DIR = Path(__file__).parent

@pytest.mark.parametrize(
        'paths, test_path, rel_path, expected', [(
            [],
            'test.py',
            'dummy.nt',
            lambda p: p / 'dummy.nt',
        ), (
            [],
            'test.py',
            ['dummy_1.nt', 'dummy_2.nt'],
            lambda p: [p / 'dummy_1.nt', p / 'dummy_2.nt'],
        ), (
            ['test.json'],
            'test.py',
            None,
            lambda p: p / 'test.json',
        ), (
            ['test.yaml'],
            'test.py',
            None,
            lambda p: p / 'test.yaml',
        ), (
            ['test.yml'],
            'test.py',
            None,
            lambda p: p / 'test.yml',
        ), (
            ['test.toml'],
            'test.py',
            None,
            lambda p: p / 'test.toml',
        ), (
            ['test.nt'],
            'test.py',
            None,
            lambda p: p / 'test.nt',
        )
])
def test_resolve_param_path(paths, test_path, rel_path, expected, tmp_path):
    for p in paths:
        (tmp_path / p).touch()

    param_path = pffp._resolve_param_path(tmp_path / test_path, rel_path)
    assert param_path == expected(tmp_path)

@pytest.mark.parametrize(
        'paths, test_path, rel_path, messages', [(
            [],
            'test.py',
            None,
            [
                "can't find parametrization file",
                "none of the following default paths exist",
                "test.json",
                "test.yml",
                "test.toml",
                "test.nt",
            ],
        ), (
            ['test.yml', 'test.toml'],
            'test.py',
            None,
            [
                "found multiple parametrization files",
                "don't know which file to use:",
                "test.yml",
                "test.toml",
            ],
        )
])
def test_resolve_param_path_err(paths, test_path, rel_path, messages, tmp_path):
    for p in paths:
        (tmp_path / p).touch()

    with pytest.raises(pff.ConfigError) as err:
        pffp._resolve_param_path(tmp_path / test_path, rel_path)

    for msg in messages:
        assert err.match(msg)

@pytest.mark.parametrize(
        'path, contents, expected', [
            ('ok.json', '{"a": "b"}', {'a': 'b'}),
            ('ok.yml', 'a: b', {'a': 'b'}),
            ('ok.yaml', 'a: b', {'a': 'b'}),
            ('ok.toml', 'a = "b"', {'a': 'b'}),
            ('ok.nt', 'a: b', {'a': 'b'}),
        ],
)
def test_load_suite_params(path, contents, expected, tmp_path):
    p = tmp_path / path
    p.write_text(contents)

    suite_params = pffp._load_and_cache_suite_params(p)
    assert suite_params == expected

@pytest.mark.parametrize(
        'files, path, messages', [(
            {},
            'does-not-exist.json',
            [
                "can't find parametrization file",
                "does-not-exist.json",
            ],
        ), (
            {'wrong-ext.xyz': ''},
            'wrong-ext.xyz',
            [
                "parametrization file must have a recognized extension",
                "the given extension is not recognized: .xyz",
            ],
        ), (
            {'err.json': '{"a":'},
            'err.json',
            [
                "failed to load parametrization file",
                "attempted to load file with: json.load()",
                "Expecting value",
            ],
        ), (
            {'err.yml': ':'},
            'err.yml',
            [
                "failed to load parametrization file",
                "attempted to load file with: yaml.safe_load()",
                "expected <block end>, but found ':'",
            ],
        ), (
            {'err.yaml': ':'},
            'err.yaml',
            [
                "failed to load parametrization file",
                "attempted to load file with: yaml.safe_load()",
                "expected <block end>, but found ':'",
            ],
        ), (
            {'err.toml': 'a ='},
            'err.toml',
            [
                "failed to load parametrization file",
                "attempted to load file with: toml.decoder.load()",
                "Empty value is invalid",
            ],
        ), (
            {'err.nt': 'a ='},
            'err.nt',
            [
                "failed to load parametrization file",
                "attempted to load file with: nestedtext.load()",
            ],
        ),
    ]
)
def test_load_suite_params_err(files, path, messages, tmp_path):
    for p, content in files.items():
        (tmp_path / p).write_text(content)
        
    with pytest.raises(pff.ConfigError) as err:
        pffp._load_and_cache_suite_params(tmp_path / path)

    for msg in messages:
        assert err.match(msg)

def test_cache_suite_params(tmp_path):
    m = Mock()
    p = tmp_path / 'dummy.xyz'
    p.touch()
    pff.add_loader('.xyz', m)

    try:
        assert m.call_count == 0

        pffp._load_and_cache_suite_params(p)
        assert m.call_count == 1

        pffp._load_and_cache_suite_params(p)
        assert m.call_count == 1

    finally:
        pff.drop_loader('.xyz')

@pytest.mark.parametrize(
        'suite_params, test_name, expected', [(
            {'a': 1}, 'a', 1,
        ),
])
def test_load_test_params(suite_params, test_name, expected, tmp_path):
    import json
    p = tmp_path / 'ok.yml'
    p.write_text(json.dumps(suite_params))

    test_params = pffp._load_test_params(p, test_name)
    assert test_params == expected

@pytest.mark.parametrize(
        'suite_params, test_name, message', [(
            {'b': 1}, 'a',
            "must specify parameters for 'a'",
        ),
])
def test_load_test_params_err(suite_params, test_name, message, tmp_path):
    import json
    p = tmp_path / 'err.yml'
    p.write_text(json.dumps(suite_params))

    with pytest.raises(pff.ConfigError, match=message):
        pffp._load_test_params(p, test_name)

@pytest.mark.parametrize(
        'test_params, preprocess, schema, expected', [(
            # preprocess:
            [{'a': 1}],
            lambda x: x + [{'a': 2}],
            None,
            [{'a': 1}, {'a': 2}],
        ), (
            # schema:
            [],
            None,
            Schema({'a': int}),
            [],
        ), (
            [{'a': 1}],
            None,
            Schema({'a': int}),
            [{'a': 1}],
        ), (
            [{'a': '1'}],
            None,
            Schema({'a': eval}),
            [{'a': 1}],
        ), (
            [{'a': 1}],
            None,
            Schema({str: int}),
            [{'a': 1}],
        ), (
            # schema + id
            [{'a': 1, 'id': 'x'}],
            None,
            Schema({str: int}),
            [{'a': 1, 'id': 'x'}],
        ), (
            [{'a': 1}],
            None,
            lambda x: {**x, 'id': 'x'},
            [{'a': 1, 'id': 'x'}],
        ), (
            [{'a': 1, 'id': 'x'}],
            None,
            lambda x: {**x, 'id': 'y'},
            [{'a': 1, 'id': 'x'}],
        ), (
            # schema + marks
            [{'a': 1, 'marks': 'skip'}],
            None,
            Schema({str: int}),
            [{'a': 1, 'marks': 'skip'}],
        ), (
            [{'a': 1}],
            None,
            lambda x: {**x, 'marks': 'skip'},
            [{'a': 1, 'marks': 'skip'}],
        ), (
            [{'a': 1, 'marks': 'skip'}],
            None,
            lambda x: {**x, 'marks': []},
            [{'a': 1, 'marks': 'skip'}],
        )
])
def test_process_test_params(test_params, preprocess, schema, expected):
    actual = pffp._process_test_params(test_params, preprocess, schema)
    assert actual == expected

@pytest.mark.parametrize(
        'test_params, preprocess, schema, message', [(
            # preprocess
            [{'a': 1}],
            lambda _: 'a',
            None,
            "expected preprocess to return list of dicts, got 'a'",
        ), (
            [{'a': 1}],
            lambda _: ['a'],
            None,
            "expected dict, got 'a'",
        ), (
            # schema
            'a',
            None,
            Schema({'a': int}),
            "expected list of dicts, got 'a'",
        ), (
            ['a'],
            None,
            Schema({'a': int}),
            "expected dict, got 'a'",
        ), (
            [{'a': 'b'}],
            None,
            Schema({'a': int}),
            "test case failed schema validation",
        ), (
            [{'a': 1}],
            None,
            Schema({'b': int}),
            "test case failed schema validation",
        ), (
            [{'a': 1, 'b': 'c'}],
            None,
            Schema({str: int}),
            "test case failed schema validation",
        ), (
            [{}],
            None,
            lambda _: 'a',
            "expected schema to return dict, got 'a'",
        )
])
def test_process_test_params_err(test_params, preprocess, schema, message):
    with pytest.raises(pff.ConfigError, match=message):
        pffp._process_test_params(test_params, preprocess, schema)

@pytest.mark.parametrize(
        'test_params, expected', [(
            [],
            set(),
        ), (
            [{'a': 1}],
            {'a'},
        ), (
            [{'a': 1}, {'a': 2}],
            {'a'},
        ), (
            [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}],
            {'a', 'b'},
        ), (
            [{'a': 1, 'id': 2}, {'a': 3}],
            {'a'},
        ), (
            [{'a': 1, 'marks': 2}, {'a': 3}],
            {'a'},
        ),
])
def test_check_test_param_keys(test_params, expected):
    assert pffp._check_test_params_keys(test_params) == expected

@pytest.mark.parametrize(
        'test_params', [
            [{'a': 1}, {'b': 2}],
            [{'a': 1, 'b': 2}, {'a': 3}],
            [{'a': 1, 'b': 2}, {'b': 4}],
])
def test_check_test_param_keys_err(test_params):
    message = "every test case must specify the same parameters"
    with pytest.raises(pff.ConfigError, match=message):
        pffp._check_test_params_keys(test_params)

@pytest.mark.parametrize(
        'case_params, expected', [(
            {'a': 'b'},
            "'a': 'b'",
        ), (
            {'a': 1, 'b': 2},
            "'a': 1\n'b': 2",
        ), (
            1,
            "1",
        )
])
def test_format_case_params(case_params, expected):
    assert pffp._format_case_params(case_params) == expected

@pytest.mark.parametrize(
        'test_params, keys, values', [(
            [{'a': 1}],
            ['a'],
            [pytest.param(1, id='1')],
        ), (
            [{'a': 1, 'b': 2}],
            ['a', 'b'],
            [pytest.param(1, 2, id='1')],
        ), (
            [{'a': 1, 'id': 'hello'}],
            ['a'],
            [pytest.param(1, id='hello')],
        ), (
            [{'a': 1, 'marks': 'skip'}],
            ['a'],
            [pytest.param(1, id='1', marks=[pytest.mark.skip])],
        ), (
            [{'a': 1, 'marks': 'skip,slow'}],
            ['a'],
            [pytest.param(1, id='1', marks=[pytest.mark.skip, pytest.mark.slow])],
        ), (
            [{'a': 1, 'marks': ['skip']}],
            ['a'],
            [pytest.param(1, id='1', marks=[pytest.mark.skip])],
        ), (
            [{'a': 1, 'marks': ['skip','slow']}],
            ['a'],
            [pytest.param(1, id='1', marks=[pytest.mark.skip, pytest.mark.slow])],
        ),
])
def test_init_parametrize_arguments(test_params, keys, values):
    assert pffp._init_parametrize_args(test_params) == (keys, values)

def test_parametrize_from_file(testdir):
    testdir.makefile('.nt', """\
            test_addition:
              -
                a: 1
                b: 2
                c: 3
              -
                a: 2
                b: 4
                c: 6
                    
            test_concat:
              -
                a: 1
                b: 2
                c: 12
              -
                a: 2
                b: 4
                c: 24
    """)
    testdir.makefile('.py', """\
            import parametrize_from_file
            from voluptuous import Schema

            @parametrize_from_file(schema=Schema({str: eval}))
            def test_addition(a, b, c):
                assert a + b == c

            @parametrize_from_file
            def test_concat(a, b, c):
                assert a + b == c
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=4)

@pytest.mark.parametrize(
        'files, get_path, key, expected_keys, expected_values', [(
            {
                'test.json': '{"aa": [{"x": 1}]}',
            },
            lambda p: p / 'test.json',
            'aa',
            ['x'],
            [pytest.param(1, id='1')],
        ), (
            {
                'test.json': '{"aa": [{"x": 1}], "bb": [{"x": 2}]}',
            },
            lambda p: p / 'test.json',
            ['aa', 'bb'],
            ['x'],
            [pytest.param(1, id='1'), pytest.param(2, id='2')],
        ), (
            {
                'test_1.json': '{"aa": [{"x": 1}]}',
                'test_2.json': '{"aa": [{"x": 2}]}',
            },
            lambda p: [p / 'test_1.json', p / 'test_2.json'],
            'aa',
            ['x'],
            [pytest.param(1, id='1'), pytest.param(2, id='2')],
        ), (
            {
                'test_1.json': '{"aa": [{"x": 1}]}',
                'test_2.json': '{"bb": [{"x": 2}]}',
            },
            lambda p: [p / 'test_1.json', p / 'test_2.json'],
            ['aa', 'bb'],
            ['x'],
            [pytest.param(1, id='1'), pytest.param(2, id='2')],
        )],
)
def test_load_parameters(files, get_path, key, expected_keys, expected_values, tmp_path):
    for p, content in files.items():
        (tmp_path / p).write_text(content)

    keys, values = pff.load_parameters(get_path(tmp_path), key)
    assert keys == expected_keys
    assert values == expected_values

@pytest.mark.parametrize(
        'files, get_path, key, messages', [(
            {
                'test.json': '{"a": ',
            },
            lambda p: p / 'test.json',
            'a',
            [r'parameter file: .*test\.json'],
        ), (
            {
                'test.json': '{"a": 1}',
            },
            lambda p: p / 'test.json',
            'a',
            [r'parameter file: .*test\.json', 'top-level key: a'],
        ), (
            {},
            lambda p: [p / 'test_1.json', p / 'test_2.json'],
            ['a', 'b', 'c'],
            [
                'must specify matching numbers of paths and keys',
                'paths: .*test_1.*test_2',
                r"keys: \['a', 'b', 'c'\]",
            ],
        )],
)
def test_load_parameters_err(files, get_path, key, messages, tmp_path):
    for p, content in files.items():
        (tmp_path / p).write_text(content)

    with pytest.raises(pff.ConfigError) as err:
        pff.load_parameters(get_path(tmp_path), key)

    for msg in messages:
        assert err.match(msg)
