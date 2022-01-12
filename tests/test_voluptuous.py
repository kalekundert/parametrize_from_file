#!/usr/bin/env python3

import pytest
from voluptuous import Schema, Invalid, Optional
from parametrize_from_file.voluptuous import Namespace, empty_ok
from test_namespace import SharedParams, MockError1
from unittest.mock import MagicMock

@SharedParams.eval_err
def test_eval_err(globals, args, kwargs, error):
    ns = Namespace(globals)
    with pytest.raises(Invalid):
        ns.eval(*args, **kwargs)

@SharedParams.exec_err
def test_exec_err(globals, src, kwargs, error):
    ns = Namespace(globals)
    with pytest.raises(Invalid):
        ns.exec(src, **kwargs)

@SharedParams.error_err
def test_error_err(globals, params, trigger_error, expected_error):
    ns = Namespace(globals)
    with pytest.raises(Invalid):
        with ns.error(params):
            raise trigger_error

def test_error_or():
    ns = Namespace(E=MockError1)
    schema = Schema({
        **ns.error_or({'x': int}),
    })

    # Given: expected
    x1 = schema({'x': 1})

    assert x1['x'] == 1

    with pytest.raises(MockError1):
        with x1['error']:
            raise MockError1

    # Given: error
    x2 = schema({'error': 'E'})

    assert 'x' in x2

    with x2['error']:
        raise MockError1

def test_error_or_optional():
    ns = Namespace(E=MockError1)
    schema = Schema({
        **ns.error_or({Optional('x', default=0): int}),
    })

    x0 = schema({})
    assert x0['x'] == 0
    assert isinstance(x0['x'], int)

def test_error_or_reserved():
    ns = Namespace(E=MockError1)
    with pytest.raises(ValueError):
        schema = Schema({
            **ns.error_or({'error': int}),
        })

def test_error_or_type_err():
    ns = Namespace(E=MockError1)
    with pytest.raises(TypeError):
        schema = Schema({
            **ns.error_or({str: int}),
        })

@pytest.mark.parametrize(
        'schema, value, expected', [
            ([int], [1], [1]),
            ([int], [], []),
            ([int], '', []),
        ],
)
def test_empty_ok(schema, value, expected):
    assert empty_ok(schema)(value) == expected
