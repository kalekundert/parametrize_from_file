#!/usr/bin/env python3

import pytest
import parametrize_from_file as pff
from unittest.mock import Mock
from schema import Use
from pathlib import Path

pytest_plugins = ['pytester']
TEST_DIR = Path(__file__).parent

@pytest.mark.parametrize(
        'test_path, rel_path, expected', [(
            'test.py', 'dummy.nt',
            'dummy.nt',
        ), (
            'json_dir/test.py', None,
            'json_dir/test.json',
        ), (
            'toml_dir/test.py', None,
            'toml_dir/test.toml',
        ), (
            'yaml_dir/test.py', None,
            'yaml_dir/test.yml',
        ), (
            'nt_dir/test.py', None,
            'nt_dir/test.nt',
        )
])
def test_find_param_path(test_path, rel_path, expected):
    root = TEST_DIR / 'test_find_param_path'
    param_path = pff._find_param_path(root/test_path, rel_path)
    assert param_path == root/expected

@pytest.mark.parametrize(
        'test_path, rel_path, message', [(
            'test.py', 'xyz',
            "can't find parametrization file",
        ), (
            'test.py', 'dummy.xyz',
            "parametrization file must have a recognized extension",
        ), (
            'dummy_dir/test.py', None,
            "can't find parametrization file",
        )
])
def test_find_param_path_err(test_path, rel_path, message):
    root = TEST_DIR / 'test_find_param_path'
    with pytest.raises(pff.ConfigError, match=message):
        pff._find_param_path(root/test_path, rel_path)

@pytest.mark.parametrize('suffix', pff.LOADERS.keys())
def test_load_suite_params(suffix):
    root = TEST_DIR / 'test_load_and_cache_suite_params'
    suite_params = pff._load_and_cache_suite_params(root / f'ok{suffix}')
    assert suite_params == {'a': 'b'}

@pytest.mark.parametrize('suffix', pff.LOADERS.keys())
def test_load_suite_params_err(suffix):
    root = TEST_DIR / 'test_load_and_cache_suite_params'
    message = "failed to load parametrization file"

    with pytest.raises(pff.ConfigError, match=message):
        pff._load_and_cache_suite_params(root / f'err{suffix}')

def test_cache_suite_params(monkeypatch):
    m = Mock()
    monkeypatch.setattr(pff, 'LOADERS', {'.xyz': m})
    assert m.call_count == 0

    for i in range(2):
        pff._load_and_cache_suite_params(Path('dummy.xyz'))
        assert m.call_count == 1

@pytest.mark.parametrize(
        'suite_params, test_name, expected', [(
            {'a': 1}, 'a', 1,
        ),
])
def test_get_test_params(suite_params, test_name, expected):
    test_params = pff._get_test_params(suite_params, test_name)
    assert test_params == expected

@pytest.mark.parametrize(
        'suite_params, test_name, message', [(
            {'b': 1}, 'a',
            "must specify parameters for 'a'",
        ),
])
def test_get_test_params_err(suite_params, test_name, message):
    with pytest.raises(pff.ConfigError, match=message):
        pff._get_test_params(suite_params, test_name)

@pytest.mark.parametrize(
        'test_params, schema, expected', [(
            [],
            None,
            [],
        ), (
            [{'a': 1}],
            None,
            [{'a': 1}],
        ), (
            [],
            {'a': str},
            [],
        ), (
            [{'a': '1'}],
            {'a': str},
            [{'a': '1'}],
        ), (
            [{'a': '1'}],
            {'a': Use(int)},
            [{'a': 1}],
        )
])
def test_validate_test_params(test_params, schema, expected):
    assert pff._validate_test_params(test_params, schema) == expected

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
    assert pff._check_test_params_keys(test_params) == expected

@pytest.mark.parametrize(
        'test_params', [
            [{'a': 1}, {'b': 2}],
            [{'a': 1, 'b': 2}, {'a': 3}],
            [{'a': 1, 'b': 2}, {'b': 4}],
])
def test_check_test_param_keys_err(test_params):
    message = "every test case must specify the same parameters"
    with pytest.raises(pff.ConfigError, match=message):
        pff._check_test_params_keys(test_params)

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
    assert pff._init_parametrize_args(test_params) == (keys, values)

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
            from schema import Use

            @parametrize_from_file(schema={str: Use(eval)})
            def test_addition(a, b, c):
                assert a + b == c

            @parametrize_from_file
            def test_concat(a, b, c):
                assert a + b == c
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=4)

