#!/usr/bin/env python3

import pytest, sys, os
from unittest.mock import Mock, MagicMock
from parametrize_from_file import Namespace, star, error
from operator import itemgetter

class IgnoreMissing:

    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return f'IgnoreMissing({self.items!r})'

    def __eq__(self, other):
        subset = {k: other[k] for k in self.items if k in other}
        return subset == self.items

parametrize_init_fork = pytest.mark.parametrize(
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

@parametrize_init_fork
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

@parametrize_init_fork
def test_copy(args, kwargs, expected):
    ns1 = Namespace(*args, **kwargs)
    ns2 = ns1.copy()
    for k, v in expected.items():
        assert ns2[k] == v

@parametrize_init_fork
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

def test_eval_immutable():
    ns = Namespace(a=1)
    assert ns == {'a': 1}

    ns.eval('a + 1')
    assert ns == {'a': 1}

@pytest.mark.parametrize(
        'obj', [
            Mock(),
            MagicMock(),
            error({'type': 'ZeroDivisionError'}),
            error('none'),
        ],
)
def test_eval_mock(obj):
    ns = Namespace()
    assert ns.eval(obj) is obj

@pytest.mark.parametrize(
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
        'obj', [
            Mock(),
            MagicMock(),
            error({'type': 'ZeroDivisionError'}),
            error('none'),
        ],
)
def test_exec_mock(obj):
    ns = Namespace()
    assert ns.exec(obj) is obj

@pytest.mark.parametrize(
        'globals, src, kwargs, error', [
            ({'a': 1}, 'b', {}, NameError),
            ({'a': 1}, '1/0', {}, ZeroDivisionError),
            ({'a': 1}, 1, {}, TypeError),
            ({'a': 1}, 'b = a + 1', {'get': 'c'}, KeyError),
            ({'a': 1}, 'b = a + 1', {'get': itemgetter('c')}, KeyError),
        ],
)
def test_exec_err(globals, src, kwargs, error):
    ns = Namespace(globals)
    with pytest.raises(error):
        ns.exec(src, **kwargs)

