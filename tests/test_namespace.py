#!/usr/bin/env python3

import pytest, sys, os
from unittest.mock import Mock, MagicMock
from parametrize_from_file import Namespace, star
from operator import itemgetter
from inspect import isclass

class MockError1(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.__dict__.update(kwargs)

class MockError1a(MockError1):
    pass

class MockError2(Exception):
    pass

class IgnoreMissing:

    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return f'IgnoreMissing({self.items!r})'

    def __eq__(self, other):
        subset = {k: other[k] for k in self.items if k in other}
        return subset == self.items

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
                ({'a': 1}, [{'b': '1'}], {'keys': True}, NameError),

                # Unhashable keys:
                ({'a': 1}, [{'[a]': '1'}], {'keys': True}, TypeError),
                ({'a': 1}, [{'{a: 1}': '1'}], {'keys': True}, TypeError),

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
            'globals, src, kwargs, error', [
                ({'a': 1}, 'b', {}, NameError),
                ({'a': 1}, '1/0', {}, ZeroDivisionError),
                ({'a': 1}, 1, {}, TypeError),
                ({'a': 1}, 'b = a + 1', {'get': 'c'}, KeyError),
                ({'a': 1}, 'b = a + 1', {'get': itemgetter('c')}, KeyError),
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
        'globals, args, kwargs, invoke, expected', [
            # Basic data types:
            (
                {'a': 1},
                ['a + 1'],
                {},
                lambda f: f,
                2,
            ), (
                {'a': 1},
                ['a + 1', 'a + 2'],
                {},
                lambda f: f,
                [2, 3],
            ), (
                {'a': 1},
                [['a + 1']],
                {},
                lambda f: f,
                [2],
            ), (
                {'a': 1},
                [['a + 1', 'a + 2']],
                {},
                lambda f: f,
                [2, 3],
            ), (
                {'a': 1},
                [{'a': 'a + 1'}],
                {},
                lambda f: f,
                {'a': 2},
            ), (
                {'a': 1},
                [{'a': 'a + 1'}],
                {'keys': True},
                lambda f: f,
                {1: 2},
            ), (
                {'a': 1},
                [{'a': 'a + 1', 'b': 'a + 2'}],
                {},
                lambda f: f,
                {'a': 2, 'b': 3},
            ),

            # Recursion:
            (
                {'a': 1},
                [[['a + 1']]],
                {},
                lambda f: f,
                [[2]],
            ), (
                {'a': 1},
                [[{'a': 'a + 1'}]],
                {},
                lambda f: f,
                [{'a': 2}],
            ), (
                {'a': 1},
                [{'a': ['a + 1']}],
                {},
                lambda f: f,
                {'a': [2]},
            ), (
                {'a': 1},
                [{'a': ['a + 1']}],
                {'keys': True},
                lambda f: f,
                {1: [2]},
            ), (
                {'a': 1},
                [{'a': {'b': 'a + 1'}}],
                {},
                lambda f: f,
                {'a': {'b': 2}},
            ), (
                {'a': 1},
                [{'a': {'a+1': 'a+2'}}],
                {'keys': True},
                lambda f: f,
                {1: {2: 3}},
            ),

            # Deferral
            (
                {'a': 1},
                [],
                {},
                lambda f: f('a + 1'),
                2,
            ), (
                {'a': 1},
                ['a + 1'],
                {'defer': True},
                lambda f: f(),
                2,
            ), (
                {'a': 1},
                ['a + 1'],
                {'defer': True},
                lambda f: f.eval(),
                2,
            ), (
                {},
                ['1/0'],
                {'defer': True},
                lambda f: 'no error',
                'no error',
            ), (
                {'a': 1},
                [{'a': 'a + 1'}],
                {'defer': True, 'keys': True},
                lambda f: f(),
                {1: 2},
            ), (
                {'a': 1},
                [],
                {'defer': True},
                lambda f: f('a + 1')(),
                2,
            ), (
                {},
                [],
                {'defer': True},
                lambda f: f('1/0') and 'no error',
                'no error',
            ), (
                {'a': 1},
                [],
                {'defer': True, 'keys': True},
                lambda f: f({'a': 'a + 1'})(),
                {1: 2},
            ),
        ],
)
def test_eval(globals, args, kwargs, invoke, expected):
    ns = Namespace(globals)
    f = ns.eval(*args, **kwargs)
    assert invoke(f) == expected

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

@pytest.mark.parametrize(
        'globals, args, kwargs, invoke, expected', [
            (
                {'a': 1},
                ['b = a + 1'],
                {},
                lambda f: f,
                IgnoreMissing({'a': 1, 'b': 2}),
            ),

            # Deferral
            (
                {'a': 1},
                [],
                {},
                lambda f: f('b = a + 1'),
                IgnoreMissing({'a': 1, 'b': 2}),
            ), (
                {'a': 1},
                ['b = a + 1'],
                {'defer': True},
                lambda f: f(),
                IgnoreMissing({'a': 1, 'b': 2}),
            ), (
                {'a': 1},
                ['b = a + 1'],
                {'defer': True},
                lambda f: f.exec(),
                IgnoreMissing({'a': 1, 'b': 2}),
            ), (
                {},
                ['1/0'],
                {'defer': True},
                lambda f: 'no error',
                'no error',
            ), (
                {'a': 1},
                [],
                {'defer': True},
                lambda f: f('b = a + 1')(),
                IgnoreMissing({'a': 1, 'b': 2}),
            ), (
                {},
                [],
                {'defer': True},
                lambda f: f('1/0') and 'no error',
                'no error',
            ),

            # Name lookup
            (
                {'a': 1},
                ['b = a + 1'],
                {'get': 'b'},
                lambda f: f,
                2,
            ), (
                {'a': 1},
                [],
                {'get': 'b'},
                lambda f: f('b = a + 1'),
                2,
            ), (
                {'a': 1},
                [],
                {'get': ('a', 'b')},
                lambda f: f('b = a + 1'),
                (1, 2),
            ), (
                {'a': 1},
                [],
                {'get': ['a', 'b']},
                lambda f: f('b = a + 1'),
                (1, 2),
            ), (
                {'a': 1},
                [],
                {'get': itemgetter('b')},
                lambda f: f('b = a + 1'),
                2,
            ), (
                {'a': 1},
                [],
                {'get': 'b', 'defer': True},
                lambda f: f('b = a + 1')(),
                2,
            ), (
                {},
                [],
                {'get': 'b', 'defer': True},
                lambda f: f('1/0') and 'no error',
                'no error',
            ),
        ],
)
def test_exec(globals, args, kwargs, invoke, expected):
    ns1 = Namespace(globals)
    f = ns1.exec(*args, **kwargs)

    assert ns1 == globals
    assert invoke(f) == expected

def test_exec_immutable():
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
def test_exec_err(globals, src, kwargs, error):
    ns = Namespace(globals)
    with pytest.raises(error):
        ns.exec(src, **kwargs)

@pytest.mark.parametrize(
        'globals, params, expected_errors, unexpected_errors', [
            # Type
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
            ),

            # Message
            (
                {'E': MockError1},
                {'type': 'E', 'message': 'a'},
                [MockError1('a')],
                [MockError1('b')],
            ), (
                {'E': MockError1},
                {'type': 'E', 'message': ['a', 'b']},
                [MockError1('ab'), MockError1('ba')],
                [MockError1('a'), MockError1('b')],
            ),

            # Pattern
            (
                {'E': MockError1},
                {'type': 'E', 'pattern': r'\d{3}'},
                [MockError1('404')],
                [MockError1(r'\d{3}')],
            ), (
                {'E': MockError1},
                {'type': 'E', 'pattern': [r'\d{3}', r'\w{4}']},
                [MockError1('HTTP 404'), MockError1('404 HTTP')],
                [MockError1(r'\d{3}\w{4}'), MockError1('HTTP'), MockError1('404')],
            ),

            # Attrs
            (
                {'E': MockError1},
                {'type': 'E', 'attrs': {'a': '1'}},
                [MockError1(a=1)],
                [MockError1(), MockError1(a=2)],
            ), (
                {'E': MockError1},
                {'type': 'E', 'attrs': {'a': '1', 'b': '2'}},
                [MockError1(a=1, b=2)],
                [MockError1(a=1), MockError1(b=2), MockError1(a=1, b=1), MockError1(a=2, b=2)],
            ),

            # Assertions
            (
                {'E': MockError1},
                {'type': 'E', 'assertions': 'assert exc.f() == 1'},
                [MockError1(f=lambda: 1)],
                [MockError1(f=lambda: 2)],
            ),

            # Cause
            (
                {'E1': MockError1, 'E2': MockError2},
                {'type': 'E1', 'cause': 'True'},
                [lambda: wrap_error(MockError1, MockError2)],
                [
                    MockError1(), 
                    (MockError2, lambda: wrap_error(MockError1, MockError2, cause=False)),
                    (MockError1, lambda: wrap_error(MockError2, MockError1)),
                ],
            ), (
                {'E1': MockError1, 'E2': MockError2},
                {'type': 'E1', 'cause': 'True', 'message': 'a'},
                [lambda: wrap_error(MockError1('a'), MockError1)],
                [
                    (MockError1, lambda: wrap_error(MockError1, MockError1('a'))),
                ],
            ), (
                {'E1': MockError1, 'E2': MockError2},
                {'type': 'E1', 'cause': 'True', 'pattern': r'\d{3}'},
                [lambda: wrap_error(MockError1('404'), MockError1('HTTP'))],
                [
                    (MockError1, lambda: wrap_error(MockError1('HTTP'), MockError1('404'))),
                ],
            ), (
                {'E1': MockError1, 'E2': MockError2},
                {'type': 'E1', 'cause': 'True', 'attrs': {'a': '1'}},
                [lambda: wrap_error(MockError1(a=1), MockError1(a=2))],
                [
                    (MockError1, lambda: wrap_error(MockError1(a=2), MockError1(a=1))),
                ],
            ),
        ],
)
def test_error(globals, params, expected_errors, unexpected_errors):
    ns = Namespace(globals)
    cm = ns.error(params)

    assert bool(cm) == bool(expected_errors)

    def unpack(err):
        if isinstance(err, tuple):
            return err
        else:
            return err.__class__, err

    def raise_or_call(err):
        if isinstance(err, Exception):
            raise err
        if isclass(err) and issubclass(err, Exception):
            raise err
        err()

    def noop():
        pass

    for err in expected_errors or [noop]:
        print("expected:", err)
        with cm:
            raise_or_call(err)

    for err_type, err in map(unpack, unexpected_errors):
        print("unexpected:", err_type, err)
        with pytest.raises((err_type, AssertionError)):
            with cm:
                raise_or_call(err)
    
@SharedParams.error_err
def test_error_err(globals, params, trigger_error, expected_error):
    ns = Namespace(globals)
    with pytest.raises(expected_error):
        with ns.error(params):
            raise trigger_error

@pytest.mark.parametrize(
        'globals, params, expected', [
            (
                {'E': MockError1},
                'none',
                "<ExpectSuccess>",
            ), (
                {'E': MockError1},
                'E',
                "<ExpectError type='E'>",
            ), (
                {'E': MockError1},
                {'type': 'E', 'message': 'a'},
                "<ExpectError type='E' messages=['a']>",
            ), (
                {'E': MockError1},
                {'type': 'E', 'pattern': 'a'},
                "<ExpectError type='E' patterns=['a']>",
            ), (
                {'E': MockError1},
                {'type': 'E', 'attrs': {'a': '1'}},
                "<ExpectError type='E' attrs={'a': '1'}>",
            ), (
                {'E': MockError1},
                {'type': 'E', 'assertions': 'assert True'},
                "<ExpectError type='E' assertions='assert True'>",
            ),
        ],
)
def test_error_repr(globals, params, expected):
    ns = Namespace(globals)
    cm = ns.error(params)
    assert repr(cm) == expected


def wrap_error(exc_1, exc_2, cause=True):
    try:
        raise exc_1
    except Exception as err:
        if cause:
            raise exc_2 from err
        else:
            raise exc_2

