#!/usr/bin/env python3

import pytest
from parametrize_from_file import Namespace

class MockError1(Exception):
    pass

class MockError1a(MockError1):
    pass

class MockError2(Exception):
    pass

class SharedParams:
    use_init = pytest.mark.parametrize(
            'args, kwargs, expected', [

                # One name:
                ([{'a': 1}], {}, {'a': 1}),
                (['a = 1'], {}, {'a': 1}),
                ([], {'a': 1}, {'a': 1}),

                # Two names:
                ([{'a': 1, 'b': 2}], {}, {'a': 1, 'b': 2}),
                ([{'a': 1}, {'b': 2}], {}, {'a': 1, 'b': 2}),
                ([{'a': 1}, 'b = 2'], {}, {'a': 1, 'b': 2}),
                ([{'a': 1}], {'b': 2}, {'a': 1, 'b': 2}),

                (['a, b = 1, 2'], {}, {'a': 1, 'b': 2}),
                (['a = 1', {'b': 2}], {}, {'a': 1, 'b': 2}),
                (['a = 1', 'b = 2'], {}, {'a': 1, 'b': 2}),
                (['a = 1'], {'b': 2}, {'a': 1, 'b': 2}),

                ([{'b': 2}], {'a': 1}, {'a': 1, 'b': 2}),
                (['b = 2'], {'a': 1}, {'a': 1, 'b': 2}),
                ([], {'a': 1, 'b': 2}, {'a': 1, 'b': 2}),

                # Order matters:
                ([{'a': 1}, {'a': 2}], {}, {'a': 2}),
                ([{'a': 1}, 'a = 2'], {}, {'a': 2}),
                ([{'a': 1}], {'a': 2}, {'a': 2}),

                (['a = 1', {'a': 2}], {}, {'a': 2}),
                (['a = 1', 'a = 2'], {}, {'a': 2}),
                (['a = 1'], {'a': 2}, {'a': 2}),
            ],
    )
    eval_err = pytest.mark.parametrize(
            'globals, args, kwargs, error', [
                # Name errors:
                ({'a': 1}, ['b + 1'], {}, NameError),
                ({'a': 1}, ['a + 1', 'b + 2'], {}, NameError),
                ({'a': 1}, [['b + 1']], {}, NameError),
                ({'a': 1}, [{'a': 'b + 1'}], {}, NameError),
                ({'a': 1}, [{'b': '1'}], {'eval_keys': True}, NameError),

                # Unhashable keys:
                ({'a': 1}, [{'[a]': '1'}], {'eval_keys': True}, TypeError),
                ({'a': 1}, [{'{a: 1}': '1'}], {'eval_keys': True}, TypeError),

                # Regular errors:
                ({}, ['1/0'], {}, ZeroDivisionError),
                ({}, ['[][1]'], {}, IndexError),
                ({}, ['{}["x"]'], {}, KeyError),

                # Not list/dict/str:
                ({'a': 1}, [1], {}, TypeError),
                ({'a': 1}, [('a + 1', 'a + 2')], {}, TypeError),
            ],
    )
    exec_err = pytest.mark.parametrize(
            'globals, src, error', [
                ({'a': 1}, 'b', NameError),
                ({'a': 1}, '1/0', ZeroDivisionError),
                ({'a': 1}, 1, TypeError),
            ],
    )
    exec_and_lookup_err = pytest.mark.parametrize(
            'globals, src, key, error', [
                ({'a': 1}, 'b', '', NameError),
                ({'a': 1}, '1/0', '', ZeroDivisionError),
                ({'a': 1}, 1, '', TypeError),
                ({'a': 1}, 'b = a + 1', 'c', KeyError),
                ({'a': 1}, 'b = a + 1', lambda d: d['c'], KeyError),
            ],
    )
    error_err = pytest.mark.parametrize(
            'globals, params, error', [
                ({'E': MockError1}, 'F', NameError),
                ({'E': MockError1}, '1/0', ZeroDivisionError),
                ({'E': MockError1}, 1, TypeError),
            ],
    )

@SharedParams.use_init
def test_init(args, kwargs, expected):
    ns = Namespace(*args, **kwargs)
    for k, v in expected.items():
        assert ns[k] == v

def test_repr():
    ns = Namespace(a=1)
    assert repr(ns) == "Namespace({'a': 1})"

@SharedParams.use_init
def test_use(args, kwargs, expected):
    ns = Namespace().use(*args, **kwargs)
    for k, v in expected.items():
        assert ns[k] == v

def test_use_method_chaining():
    ns = Namespace().use(a=1).use(b=2)
    assert ns == {'a': 1, 'b': 2}

def test_use_method_chaining_overwrite():
    ns = Namespace().use(a=1).use(a=2)
    assert ns == {'a': 2}

def test_all_1():
    import mock_module
    ns = Namespace().all(mock_module)
    assert ns == {'a': 1}

def test_all_2():
    import mock_module_all
    ns = Namespace().all(mock_module_all)
    assert ns == {'b': 2}

def test_all_method_chaining():
    import mock_module
    import mock_module_all
    ns = Namespace().all(mock_module).all(mock_module_all)
    assert ns == {'a': 1, 'b': 2}

def test_all_method_chaining_overwrite():
    import mock_module
    import mock_module_overwrite
    ns = Namespace().all(mock_module).all(mock_module_overwrite)
    assert ns == {'a': 2}

def test_copy():
    ns1 = Namespace(a=1)
    ns2 = ns1.copy().use(b=2)

    assert ns1 == {'a': 1}
    assert ns2 == {'a': 1, 'b': 2}

@pytest.mark.parametrize(
        'globals, args, kwargs, expected', [
            # Basic data types:
            ({'a': 1}, ['a + 1'], {}, 2),
            ({'a': 1}, ['a + 1', 'a + 2'], {}, [2, 3]),
            ({'a': 1}, [['a + 1']], {}, [2]),
            ({'a': 1}, [['a + 1', 'a + 2']], {}, [2, 3]),
            ({'a': 1}, [{'a': 'a + 1'}], {}, {'a': 2}),
            ({'a': 1}, [{'a': 'a + 1'}], {'eval_keys': True}, {1: 2}),
            ({'a': 1}, [{'a': 'a + 1', 'b': 'a + 2'}], {}, {'a': 2, 'b': 3}),

            # Recursion:
            ({'a': 1}, [[['a + 1']]], {}, [[2]]),
            ({'a': 1}, [[{'a': 'a + 1'}]], {}, [{'a': 2}]),
            ({'a': 1}, [{'a': ['a + 1']}], {}, {'a': [2]}),
            ({'a': 1}, [{'a': ['a + 1']}], {'eval_keys': True}, {1: [2]}),
            ({'a': 1}, [{'a': {'b': 'a + 1'}}], {}, {'a': {'b': 2}}),
            ({'a': 1}, [{'a': {'a+1': 'a+2'}}], {'eval_keys': True}, {1: {2: 3}}),
        ],
)
def test_eval(globals, args, kwargs, expected):
    ns = Namespace(globals)
    assert ns.eval(*args, **kwargs) == expected

@SharedParams.eval_err
def test_eval_err(globals, args, kwargs, error):
    ns = Namespace(globals)
    with pytest.raises(error):
        ns.eval(*args, **kwargs)

def test_exec():
    ns1 = Namespace(a=1)
    ns2 = ns1.exec('b = a + 1')
    ns3 = ns2.exec('c = b + 1')

    assert ns1 == {'a': 1}

    # Can't simply compare to a dictionary anymore, because `exec()` adds a 
    # bunch of builtin names to the namespace.
    assert ns2['a'] == 1
    assert ns2['b'] == 2
    assert 'c' not in ns2

    assert ns3['a'] == 1
    assert ns3['b'] == 2
    assert ns3['c'] == 3

@SharedParams.exec_err
def test_exec_err(globals, src, error):
    ns = Namespace(globals)
    with pytest.raises(error):
        ns.exec(src)

@pytest.mark.parametrize(
        'globals, src, key, expected', [
            ({'a': 1}, 'b = a + 1', 'b', 2),
            ({'a': 1}, 'b = a + 1', lambda d: d['b'], 2),
        ],
)
def test_exec_and_lookup(globals, src, key, expected):
    ns = Namespace(globals)
    assert ns.exec_and_lookup(key)(src) == expected

@SharedParams.exec_and_lookup_err
def test_exec_and_lookup_err(globals, src, key, error):
    ns = Namespace(globals)
    with pytest.raises(error):
        ns.exec_and_lookup(key)(src)

@pytest.mark.parametrize(
        'globals, params, expected_error, unexpected_error', [
            (
                {'E': MockError1},
                'none',
                None,
                MockError2(),
            ), (
                {'E': MockError1},
                'E',
                MockError1,
                MockError2(),
            ), (
                {'E': MockError1},
                {'type': 'E'},
                MockError1,
                MockError2(),
            ), (
                {'E': MockError1},
                {'type': 'E'},
                MockError1a,
                MockError2(),
            ), (
                {'E': MockError1a},
                {'type': 'E'},
                MockError1a,
                MockError1(),
            ), (
                {'E': MockError1},
                {'type': 'E', 'message': 'a'},
                MockError1('a'),
                MockError1('b'),
            ), (
                {'E': MockError1},
                {'type': 'E', 'message': r'\d{3}'},
                MockError1('404'),
                MockError1(r'\d{3}'),
            ),
        ],
)
def test_error(globals, params, expected_error, unexpected_error):
    ns = Namespace(globals)
    cm = ns.error(params)

    with cm:
        if expected_error is not None:
            raise expected_error

    with pytest.raises((unexpected_error.__class__, AssertionError)):
        with cm:
            raise unexpected_error
    
@SharedParams.error_err
def test_error_err(globals, params, error):
    ns = Namespace(globals)
    with pytest.raises(error):
        ns.error(params)

def test_error_repr():
    ns = Namespace(E=MockError1)
    cm = ns.error('E')
    assert repr(cm) == "<ExpectError type=<class 'test_namespace.MockError1'> messages=[]>"

