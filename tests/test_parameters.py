#!/usr/bin/env python3

import pytest
import parametrize_from_file as pff
import parametrize_from_file.parameters as pffp
from unittest.mock import Mock
from pathlib import Path

pytest_plugins = ['pytester']
TEST_DIR = Path(__file__).parent
SENTINEL = object()

def assertion_error(x):
    raise AssertionError

def value_error_with_braces(x):
    raise ValueError('{hello world}')


@pytest.mark.parametrize(
        'loaders, expected', [
            # The order of the loaders/suffixes is significant to this test, 
            # since it affects how error messages are formatted.
            (
                None,
                pffp.get_loaders(),
            ), (
                {'.nt': SENTINEL},
                {
                    '.json': pffp.get_loaders()['.json'],
                    '.yaml': pffp.get_loaders()['.yaml'],
                    '.yml': pffp.get_loaders()['.yml'],
                    '.toml': pffp.get_loaders()['.toml'],
                    '.nt': SENTINEL,
                },
            ), (
                {'.xyz': SENTINEL},
                {
                    '.json': pffp.get_loaders()['.json'],
                    '.yaml': pffp.get_loaders()['.yaml'],
                    '.yml': pffp.get_loaders()['.yml'],
                    '.toml': pffp.get_loaders()['.toml'],
                    '.nt': pffp.get_loaders()['.nt'],
                    '.xyz': SENTINEL,
                },
            ),
        ],
)
def test_override_global_loaders(loaders, expected):
    assert pffp._override_global_loaders(loaders) == expected

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

    param_path = pffp._resolve_param_path(
            tmp_path / test_path, rel_path, pffp.get_loaders())

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
        pffp._resolve_param_path(
                tmp_path / test_path, rel_path, pffp.get_loaders())

    for msg in messages:
        assert err.match(msg)

@pytest.mark.parametrize(
        'suite_params, test_name, expected', [(
            {'a': 1}, 'a', 1,
        ),
])
def test_load_test_params(suite_params, test_name, expected, tmp_path):
    import json
    p = tmp_path / 'ok.json'
    p.write_text(json.dumps(suite_params))

    test_params = pffp._load_test_params(pffp.get_loaders(), p, test_name)
    assert test_params == expected

@pytest.mark.parametrize(
        'suite_params, test_name, message', [(
            {'b': 1}, 'a',
            "must specify parameters for 'a'",
        ),
])
def test_load_test_params_err(suite_params, test_name, message, tmp_path):
    import json
    p = tmp_path / 'err.json'
    p.write_text(json.dumps(suite_params))

    with pytest.raises(pff.ConfigError, match=message):
        pffp._load_test_params(pffp.get_loaders(), p, test_name)

def test_pick_loader_by_suffix():
    f = Mock()
    assert pffp._pick_loader_by_suffix({'.xyz': f}, Path('test.xyz')) is f

def test_pick_loader_by_suffix_err():
    with pytest.raises(pff.ConfigError) as err:
        pffp._pick_loader_by_suffix({'.abc': None}, Path('wrong-ext.xyz'))

    assert err.match("parametrization file must have a recognized extension")
    assert err.match("the following extensions are recognized")
    assert err.match(r"\.abc")
    assert err.match(r"the given extension is not recognized: \.xyz")

@pytest.mark.parametrize(
        'loader, path, contents, expected', [
            # Make sure all the builtin loaders work.  This doesn't really test 
            # any logic from `_load_and_cache_suite_params()`, but whatever.
            (pffp.get_loaders()['.json'], 'ok.json', '{"a": "b"}', {'a': 'b'}),
            (pffp.get_loaders()['.yml'], 'ok.yml', 'a: b', {'a': 'b'}),
            (pffp.get_loaders()['.yaml'], 'ok.yaml', 'a: b', {'a': 'b'}),
            (pffp.get_loaders()['.toml'], 'ok.toml', 'a = "b"', {'a': 'b'}),
            (pffp.get_loaders()['.nt'], 'ok.nt', 'a: b', {'a': 'b'}),
        ],
)
def test_load_suite_params(loader, path, contents, expected, tmp_path):
    p = tmp_path / path
    p.write_text(contents)

    suite_params = pffp._load_and_cache_suite_params(loader, p)
    assert suite_params == expected

@pytest.mark.parametrize(
        'loader, path, files, messages', [(
            lambda p: None,
            'does-not-exist.json',
            {},
            [
                "can't find parametrization file",
                "does-not-exist.json",
            ],
        ), (
            # Check examples of real files that the built-in loaders will fail 
            # to parse, to make sure that the error messages are still good.
            pffp.get_loaders()['.json'],
            'err.json',
            {'err.json': '{"a":'},
            [
                "failed to load parametrization file",
                r"attempted to load file with: json.load\(\)",
                "Expecting value",
            ],
        ), (
            pffp.get_loaders()['.yml'],
            'err.yml',
            {'err.yml': ':'},
            [
                "failed to load parametrization file",
                r"attempted to load file with: yaml.safe_load\(\)",
                "expected <block end>, but found ':'",
            ],
        ), (
            pffp.get_loaders()['.yaml'],
            'err.yaml',
            {'err.yaml': ':'},
            [
                "failed to load parametrization file",
                r"attempted to load file with: yaml.safe_load\(\)",
                "expected <block end>, but found ':'",
            ],
        ), (
            pffp.get_loaders()['.toml'],
            'err.toml',
            {'err.toml': 'a ='},
            [
                "failed to load parametrization file",
                r"attempted to load file with: toml.decoder.load\(\)",
                "Empty value is invalid",
            ],
        ), (
            pffp.get_loaders()['.nt'],
            'err.nt',
            {'err.nt': 'a ='},
            [
                "failed to load parametrization file",
                r"attempted to load file with: nestedtext.load\(\)",
            ],
        ), (
            # Any braces in error messages must not be evaluated by tidyexc.
            value_error_with_braces,
            'braces.xyz',
            {'braces.xyz': ''},
            [
                "failed to load parametrization file",
                "attempted to load file with: .*value_error_with_braces",
                r"\{hello world\}",
            ],
        ),
    ]
)
def test_load_suite_params_err(loader, path, files, messages, tmp_path):
    for p, contents in files.items():
        (tmp_path / p).write_text(contents)
        
    with pytest.raises(pff.ConfigError) as err:
        pffp._load_and_cache_suite_params(loader, tmp_path / path)

    for msg in messages:
        assert err.match(msg)

def test_cache_suite_params(tmp_path):
    m1 = Mock()
    m2 = Mock()

    p1 = tmp_path / 'p1.xyz'
    p2 = tmp_path / 'p2.xyz'

    p1.touch()
    p2.touch()

    pffp._load_and_cache_suite_params.cache_clear()

    assert m1.call_count == 0
    assert m2.call_count == 0


    pffp._load_and_cache_suite_params(m1, p1)
    assert m1.call_count == 1
    assert m2.call_count == 0

    pffp._load_and_cache_suite_params(m1, p1)
    assert m1.call_count == 1
    assert m2.call_count == 0


    pffp._load_and_cache_suite_params(m1, p2)
    assert m1.call_count == 2
    assert m2.call_count == 0

    pffp._load_and_cache_suite_params(m1, p2)
    assert m1.call_count == 2
    assert m2.call_count == 0


    pffp._load_and_cache_suite_params(m2, p1)
    assert m1.call_count == 2
    assert m2.call_count == 1

    pffp._load_and_cache_suite_params(m2, p1)
    assert m1.call_count == 2
    assert m2.call_count == 1


    pffp._load_and_cache_suite_params(m2, p2)
    assert m1.call_count == 2
    assert m2.call_count == 2

    pffp._load_and_cache_suite_params(m2, p2)
    assert m1.call_count == 2
    assert m2.call_count == 2

@pytest.mark.parametrize(
        'test_params, preprocess, context, schema, expected', [(
            # preprocess:
            [{'a': 1}],
            lambda xs: xs + [{'a': 2}],
            None,
            None,
            [{'a': 1}, {'a': 2}],
        ), (
            [{'a': 1}],
            lambda xs, ctx: [
                {'path': ctx.path, 'key': ctx.key, **x}
                for x in xs
            ],
            pffp.Context('x', 'y'),
            None,
            [{'path': 'x', 'key': 'y', 'a': 1}],
        ), (
            # schema:
            [],
            None,
            None,
            pff.cast(a=lambda x: x+1),
            [],
        ), (
            [{'a': 1}],
            None,
            None,
            pff.cast(a=lambda x: x+1),
            [{'a': 2}],
        ), (
            [{}],
            None,
            None,
            [pff.defaults(a=1), pff.cast(a=lambda x: x+1)],
            [{'a': 2}],
        ), (
            # schema + id
            [{'a': 1, 'id': 'x'}],
            None,
            None,
            pff.cast(id=assertion_error),
            [{'a': 1, 'id': 'x'}],
        ), (
            [{'a': 1}],
            None,
            None,
            lambda x: {**x, 'id': 'x'},
            [{'a': 1, 'id': 'x'}],
        ), (
            [{'a': 1, 'id': 'x'}],
            None,
            None,
            lambda x: {**x, 'id': 'y'},
            [{'a': 1, 'id': 'x'}],
        ), (
            # schema + marks
            [{'a': 1, 'marks': 'skip'}],
            None,
            None,
            pff.cast(marks=assertion_error),
            [{'a': 1, 'marks': 'skip'}],
        ), (
            [{'a': 1}],
            None,
            None,
            lambda x: {**x, 'marks': 'skip'},
            [{'a': 1, 'marks': 'skip'}],
        ), (
            [{'a': 1, 'marks': 'skip'}],
            None,
            None,
            lambda x: {**x, 'marks': []},
            [{'a': 1, 'marks': 'skip'}],
        )
])
def test_process_test_params(test_params, preprocess, context, schema, expected):
    actual = pffp._process_test_params(test_params, preprocess, context, schema)
    assert actual == expected

@pytest.mark.parametrize(
        'test_params, preprocess, context, schema, messages', [(
            # preprocess
            [{'a': 1}],
            lambda _: 'a',
            None,
            None,
            ["expected preprocess to return list of dicts, got 'a'"],
        ), (
            [{'a': 1}],
            lambda _: ['a'],
            None,
            None,
            ["expected dict, got 'a'"],
        ), (
            # schema
            'a',
            None,
            None,
            assertion_error,
            ["expected list of dicts, got 'a'"],
        ), (
            ['a'],
            None,
            None,
            assertion_error,
            ["expected dict, got 'a'"],
        ), (
            [{'a': 1}],
            None,
            None,
            assertion_error,
            ["test case failed schema validation"],
        ), (
            # This error message will have braces, which must not be evaluated 
            # by tidyexc.
            [{'a': 1}],
            None,
            None,
            value_error_with_braces,
            ["test case failed schema validation", r"\{hello world\}"],
        ), (
            [{}],
            None,
            None,
            lambda _: 'a',
            ["expected schema to return dict, got 'a'"],
        )
])
def test_process_test_params_err(test_params, preprocess, context, schema, messages):
    with pytest.raises(pff.ConfigError) as err:
        pffp._process_test_params(test_params, preprocess, context, schema)

    for msg in messages:
        assert err.match(msg)

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

def test_parametrize(testdir):
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
            from parametrize_from_file import cast

            @parametrize_from_file(schema=cast(a=int, b=int, c=int))
            def test_addition(a, b, c):
                assert a + b == c

            @parametrize_from_file
            def test_concat(a, b, c):
                assert a + b == c
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=4)

def test_parametrize_no_args(testdir):
    testdir.makefile('.nt', test_file="""\
            test_eq:
              -
                a: x
                b: x
    """)
    testdir.makefile('.py', test_file="""\
            import parametrize_from_file

            @parametrize_from_file
            def test_eq(a, b):
                assert a == b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_parametrize_path(testdir):
    testdir.makefile('.nt', test_file_alt="""\
            test_eq:
              -
                a: x
                b: x
    """)
    testdir.makefile('.py', test_file="""\
            import parametrize_from_file

            @parametrize_from_file('test_file_alt.nt')
            def test_eq(a, b):
                assert a == b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_parametrize_key(testdir):
    testdir.makefile('.nt', test_file="""\
            test_eq_alt:
              -
                a: x
                b: x
    """)
    testdir.makefile('.py', test_file="""\
            import parametrize_from_file

            @parametrize_from_file(key='test_eq_alt')
            def test_eq(a, b):
                assert a == b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_parametrize_loaders(testdir):
    testdir.makefile('.xyz', test_file="""\
            test_eq:
              -
                a: x
                b: x
    """)
    testdir.makefile('.py', test_file="""\
            import parametrize_from_file
            import nestedtext as nt

            @parametrize_from_file(
                loaders={'.xyz': nt.load},
            )
            def test_eq(a, b):
                assert a == b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_parametrize_preprocess(testdir):
    testdir.makefile('.nt', test_file="""\
            test_eq:
              -
                a: x
                b: x
    """)
    testdir.makefile('.py', test_file="""\
            import parametrize_from_file

            @parametrize_from_file(
                preprocess=lambda x: [*x, dict(a='y', b='y')],
            )
            def test_eq(a, b):
                assert a == b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)

def test_parametrize_schema(testdir):
    testdir.makefile('.nt', test_file="""\
            test_double:
              -
                a: 1
                b: 2
    """)
    testdir.makefile('.py', test_file="""\
            import parametrize_from_file

            @parametrize_from_file(
                schema=lambda x: {k: int(v) for k, v in x.items()},
            )
            def test_double(a, b):
                assert a * 2 == b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_parametrize_indirect(testdir):
    testdir.makefile('.nt', """\
            test_eq:
              -
                a: x
                b: x-fixture
    """)
    testdir.makefile('.py', """\
            import pytest
            import parametrize_from_file

            @pytest.fixture
            def a(request):
                return f"{request.param}-fixture"

            @parametrize_from_file(indirect=['a'])
            def test_eq(a, b):
                assert a == b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_parametrize_err(testdir):
    testdir.makefile('.py', test_path="""\
            import parametrize_from_file

            @parametrize_from_file
            def test_noop():
                pass
    """)
    result = testdir.runpytest()
    stdout = '\n'.join(result.outlines)
    assert 'test function: test_noop()' in stdout
    assert f'test file: {testdir.tmpdir}/test_path.py' in stdout

def test_fixture(testdir):
    testdir.makefile('.nt', """\
            ab:
              -
                a: x
                b: x
              -
                a: y
                b: y
    """)
    testdir.makefile('.py', """\
            import parametrize_from_file as pff

            @pff.fixture
            def ab(request):
                return request.param

            def test_eq(ab):
                assert ab.a == ab.b
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)

def test_fixture_id_marks(testdir):
    testdir.makefile('.nt', """\
            ab:
              -
                id: x
                a: x
                b: x
              -
                id: y
                marks: skip
                a: y
                b: y
    """)
    testdir.makefile('.py', """\
            import parametrize_from_file as pff

            @pff.fixture
            def ab(request):
                return request.param

            def test_eq(ab):
                assert ab.a == ab.b
    """)
    result = testdir.runpytest('-v')
    result.assert_outcomes(passed=1, skipped=1)
    stdout = '\n'.join(result.outlines)
    assert 'test_eq[x] PASSED' in stdout
    assert 'test_eq[y] SKIPPED' in stdout

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
            {
                'test_1.json': '{"a": [{"x": 1}]}',
                'test_2.json': '{"b": [{"x": 2}]}',
            },
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
        

