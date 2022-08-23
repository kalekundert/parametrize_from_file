#!/usr/bin/env python3

import pytest
import parametrize_from_file as pff
from parametrize_from_file.schema import ExpectSuccess
from unittest.mock import MagicMock
from inspect import isclass

class MockError1(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.__dict__.update(kwargs)

class MockError1a(MockError1):
    pass

class MockError2(Exception):
    pass

parametrize_get_cm = pytest.mark.parametrize(
        'get_cm', [
            lambda exc_spec, globals: pff.error(exc_spec, globals=globals),
            lambda exc_spec, globals: pff.Namespace(globals).error(exc_spec),
        ],
)
def wrap_error(exc_1, exc_2, cause=True):
    try:
        raise exc_1
    except Exception as err:
        if cause:
            raise exc_2 from err
        else:
            raise exc_2


def test_defaults():
    schema = pff.defaults(a=1, b=0)
    assert schema({'b': 2, 'c': 3}) == {'a': 1, 'b': 2, 'c': 3}

def test_cast():
    schema = pff.cast(a=int)
    assert schema({'a': '1', 'b': 2}) == {'a': 1, 'b': 2}

def test_cast_list():
    from operator import neg
    schema = pff.cast(a=[int, neg])
    assert schema({'a': '1', 'b': 2}) == {'a': -1, 'b': 2}

def test_cast_missing():
    schema = pff.cast(a=int)
    assert schema({}) == {}

@pytest.mark.parametrize(
        'globals, exc_spec, expected_errors, unexpected_errors', [
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
                {'type': 'E1', 'cause': 1},
                [lambda: wrap_error(MockError1, MockError2)],
                [
                    MockError1(), 
                    (MockError2, lambda: wrap_error(MockError1, MockError2, cause=False)),
                    (MockError1, lambda: wrap_error(MockError2, MockError1)),
                ],
            ), (
                {'E1': MockError1, 'E2': MockError2},
                {'type': 'E1', 'cause': '1', 'message': 'a'},
                [lambda: wrap_error(MockError1('a'), MockError1)],
                [
                    (MockError1, lambda: wrap_error(MockError1, MockError1('a'))),
                ],
            ), (
                {'E1': MockError1, 'E2': MockError2},
                {'type': 'E1', 'cause': '1', 'pattern': r'\d{3}'},
                [lambda: wrap_error(MockError1('404'), MockError1('HTTP'))],
                [
                    (MockError1, lambda: wrap_error(MockError1('HTTP'), MockError1('404'))),
                ],
            ), (
                {'E1': MockError1, 'E2': MockError2},
                {'type': 'E1', 'cause': '1', 'attrs': {'a': '1'}},
                [lambda: wrap_error(MockError1(a=1), MockError1(a=2))],
                [
                    (MockError1, lambda: wrap_error(MockError1(a=2), MockError1(a=1))),
                ],
            ),
        ],
)
@parametrize_get_cm
def test_error(globals, exc_spec, get_cm, expected_errors, unexpected_errors):
    cm = get_cm(exc_spec, globals)

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
    
@pytest.mark.parametrize(
        'globals, exc_spec, trigger_error, expected_error', [
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
@parametrize_get_cm
def test_error_err(globals, exc_spec, get_cm, trigger_error, expected_error):
    with pytest.raises(expected_error):
        with get_cm(exc_spec, globals):
            raise trigger_error

@pytest.mark.parametrize(
        'globals, exc_spec, expected', [
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
def test_error_repr(globals, exc_spec, expected):
    cm = pff.error(exc_spec, globals=globals)
    assert repr(cm) == expected

def test_error_or_expected():
    schema = pff.error_or('a')
    params = schema({'a': 1})

    assert set(params) == {'a', 'error'}
    assert params['a'] == 1
    assert isinstance(params['error'], ExpectSuccess)
    assert not params['error']

def test_error_or_error():
    schema = pff.error_or('a')
    params = schema({'error': 'ZeroDivisionError'})

    assert set(params) == {'a', 'error'}
    assert isinstance(params['a'], MagicMock)
    assert params['error']
    with params['error']:
        raise ZeroDivisionError

@pytest.mark.parametrize(
        'wrap_globals', [
            lambda x: x,
            lambda x: pff.Namespace(x),
        ],
)
def test_error_or_globals(wrap_globals):
    globals = wrap_globals({'E1': MockError1})
    schema = pff.error_or('a', globals=globals)
    params = schema({'error': 'E1'})

    with params['error']:
        raise MockError1

def test_error_or_param():
    schema = pff.error_or('a', param='err')
    params = schema({'err': 'ZeroDivisionError'})

    with params['err']:
        raise ZeroDivisionError

def test_error_or_mock_factory():
    sentinel = object()
    schema = pff.error_or('a', mock_factory=lambda: sentinel)
    params = schema({'error': 'ZeroDivisionError'})

    assert params['a'] is sentinel

def test_error_or_ambiguous():
    schema = pff.error_or('a')

    with pytest.raises(pff.ConfigError) as err:
        schema({'a': 1, 'error': 'ZeroDivisionError'})

    assert err.match(r"must specify either an expected value or an error, not both")
    assert err.match(r"expected value parameter\(s\): a")
    assert err.match(r"error parameter: error")

