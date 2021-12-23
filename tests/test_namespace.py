#!/usr/bin/env python3

import pytest, sys, os
from unittest.mock import Mock, MagicMock
from parametrize_from_file import Namespace, star

class MockError1(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.__dict__.update(kwargs)

class MockError1a(MockError1):
    pass

class MockError2(Exception):
    pass

class SharedParams:
    init_fork = pytest.mark.parametrize(
            'args, kwargs, expected', [

                # One name:
                ([{'a': 1}], {}, {'a': 1}),
                (['a = 1'], {}, {'a': 1}),
                ([sys], {}, {'sys': sys}),
                ([], {'a': 1}, {'a': 1}),

                # Two names:
                ([{'a': 1, 'b': 2}], {}, {'a': 1, 'b': 2}),
                ([{'a': 1}, {'b': 2}], {}, {'a': 1, 'b': 2}),
                ([{'a': 1}, 'b = 2'], {}, {'a': 1, 'b': 2}),
                ([{'a': 1}, sys], {}, {'a': 1, 'sys': sys}),
                ([{'a': 1}], {'b': 2}, {'a': 1, 'b': 2}),

                (['a, b = 1, 2'], {}, {'a': 1, 'b': 2}),
                (['a = 1', {'b': 2}], {}, {'a': 1, 'b': 2}),
                (['a = 1', 'b = 2'], {}, {'a': 1, 'b': 2}),
                (['a = 1', sys], {}, {'a': 1, 'sys': sys}),
                (['a = 1'], {'b': 2}, {'a': 1, 'b': 2}),

                ([sys, {'b': 2}], {}, {'sys': sys, 'b': 2}),
                ([sys, 'b = 2'], {}, {'sys': sys, 'b': 2}),
                ([sys, os], {}, {'sys': sys, 'os': os}),
                ([sys], {'b': 2}, {'sys': sys, 'b': 2}),

                ([{'b': 2}], {'a': 1}, {'a': 1, 'b': 2}),
                (['b = 2'], {'a': 1}, {'a': 1, 'b': 2}),
                ([sys], {'a': 1}, {'a': 1, 'sys': sys}),
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
            'globals, params, trigger_error, expected_error', [
                (
                    {'E': MockError1},
                    'F',
                    MockError1,
                    NameError,
                ), (
                    {'E': MockError1},
                    '1/0',
                    MockError1,
                    ZeroDivisionError,
                ), (
                    {'E': MockError1}, 
                    {'type': 'E', 'attrs': {'a': 'b'}},
                    MockError1(a=1),
                    NameError,
                ), (
                    {'E': MockError1},
                    {'type': 'E', 'assertions': 'a'},
                    MockError1,
                    NameError,
                ),
            ],
    )

@SharedParams.init_fork
def test_init(args, kwargs, expected):
    ns = Namespace(*args, **kwargs)
    for k, v in expected.items():
        assert ns[k] == v

def test_repr():
    ns = Namespace(a=1)
    assert repr(ns) == "Namespace({'a': 1})"

def test_operators():
    ns = Namespace(a=1)
    assert ns['a'] == 1
    assert len(ns) == 1
    assert list(ns.items()) == [('a', 1)]
    assert list(ns.keys()) == ['a']
    assert list(ns.values()) == [1]

@SharedParams.init_fork
def test_fork(args, kwargs, expected):
    ns = Namespace().fork(*args, **kwargs)
    for k, v in expected.items():
        assert ns[k] == v

def test_fork_overwrite():
    ns1 = Namespace(a=1, b=2)
    ns2 = ns1.fork(b=3, c=4)

    assert ns1 == {'a': 1, 'b': 2}
    assert ns2 == {'a': 1, 'b': 3, 'c': 4}

def test_fork_unpickleable():
    # Only globally-defined functions can be pickled.
    def unpickleable():
        pass

    ns1 = Namespace(a=unpickleable)
    ns2 = ns1.fork(b=2)

    assert ns1 == {'a': unpickleable}
    assert ns2 == {'a': unpickleable, 'b': 2}

def test_star_1():
    import mock_module
    assert star(mock_module) == {'a': 1}

def test_star_2():
    import mock_module_all
    assert star(mock_module_all) == {'b': 2}

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

@pytest.mark.parametrize(
        'mock', [Mock(), MagicMock()],
)
def test_eval_mock(mock):
    ns = Namespace()
    assert ns.eval(mock) is mock

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

@pytest.mark.parametrize(
        'mock', [Mock(), MagicMock()],
)
def test_exec_mock(mock):
    ns = Namespace()
    assert ns.exec(mock) is mock

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
        'globals, params, expected_errors, unexpected_errors', [
            (
                {'E': MockError1},
                'none',
                [],
                [MockError2()],
            ), (
                {'E': MockError1},
                'E',
                [MockError1],
                [MockError2()],
            ), (
                {'E': MockError1},
                {'type': 'E'},
                [MockError1],
                [MockError2()],
            ), (
                {'E': MockError1},
                {'type': 'E'},
                [MockError1a],
                [MockError2()],
            ), (
                {'E': MockError1a},
                {'type': 'E'},
                [MockError1a],
                [MockError1()],
            ), (
                {'E1a': MockError1a, 'E2': MockError2},
                {'type': ['E1a', 'E2']},
                [MockError1a, MockError2],
                [MockError1()],
            ), (
                {'E': MockError1},
                {'type': 'E', 'message': 'a'},
                [MockError1('a')],
                [MockError1('b')],
            ), (
                {'E': MockError1},
                {'type': 'E', 'message': ['a', 'b']},
                [MockError1('ab'), MockError1('ba')],
                [MockError1('a'), MockError1('b')],
            ), (
                {'E': MockError1},
                {'type': 'E', 'pattern': r'\d{3}'},
                [MockError1('404')],
                [MockError1(r'\d{3}')],
            ), (
                {'E': MockError1},
                {'type': 'E', 'pattern': [r'\d{3}', r'\w{4}']},
                [MockError1('HTTP 404'), MockError1('404 HTTP')],
                [MockError1(r'\d{3}\w{4}'), MockError1('HTTP'), MockError1('404')],
            ), (
                {'E': MockError1},
                {'type': 'E', 'attrs': {'a': '1'}},
                [MockError1(a=1)],
                [MockError1(), MockError1(a=2)],
            ), (
                {'E': MockError1},
                {'type': 'E', 'attrs': {'a': '1', 'b': '2'}},
                [MockError1(a=1, b=2)],
                [MockError1(a=1), MockError1(b=2), MockError1(a=1, b=1), MockError1(a=2, b=2)],
            ), (
                {'E': MockError1},
                {'type': 'E', 'assertions': 'assert err.f() == 1'},
                [MockError1(f=lambda: 1)],
                [MockError1(f=lambda: 2)],
            ),
        ],
)
def test_error(globals, params, expected_errors, unexpected_errors):
    ns = Namespace(globals)
    cm = ns.error(params)

    assert bool(cm) == bool(expected_errors)

    for err in expected_errors:
        with cm:
            raise err

    if not expected_errors:
        with cm:
            pass

    for err in unexpected_errors:
        with pytest.raises((err.__class__, AssertionError)):
            with cm:
                raise err
    
@SharedParams.error_err
def test_error_err(globals, params, trigger_error, expected_error):
    ns = Namespace(globals)
    with pytest.raises(expected_error):
        with ns.error(params):
            raise trigger_error

def test_error_repr():
    ns = Namespace(E=MockError1)
    cm = ns.error('E')
    assert repr(cm) == "<ExpectError type='E'>"

