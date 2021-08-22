#!/usr/bin/env python3

import pytest
from parametrize_from_file.utils import zip_with_scalars
from more_itertools import UnequalIterablesError

@pytest.mark.parametrize(
        "objs, kwargs, expected", [(
            # 0 items
            [],
            {},
            [],
        ), (
            [[]],
            {},
            [],
        ), (
            # 1 item
            [1],
            {},
            [(1,)],
        ), (
            [[1]],
            {},
            [(1,)],
        ), (
            [[1], 2],
            {},
            [(1, 2)],
        ), (
            [1, [2]],
            {},
            [(1, 2)],
        ), (
            [[1], [2]],
            {},
            [(1, 2)],
        ), (
            # 2 items
            [[1, 2]],
            {},
            [(1,), (2,)],
        ), (
            [[1, 2], 3],
            {},
            [(1, 3), (2, 3)],
        ), (
            [1, [2, 3]],
            {},
            [(1, 2), (1, 3)],
        ), (
            [[1, 2], [3, 4]],
            {},
            [(1, 3), (2, 4)],
        ), (
            # not iterable
            ['ab'],
            {},
            [('ab',)],
        ), (
            ['ab'],
            dict(not_iterable=None),
            [('a',), ('b',)],
        ), (
            [[1, 2]],
            dict(not_iterable=list),
            [([1, 2],)],
        ), (
            # unequal length
            [[], [1]],
            {},
            [],
        ), (
            [[1], [2, 3]],
            {},
            [(1, 2)],
        )],
)
def test_zip_with_scalars(objs, kwargs, expected):
    assert list(zip_with_scalars(*objs, **kwargs)) == expected

@pytest.mark.parametrize(
        "objs, kwargs, error", [(
            # 0 items
            [[], [1]],
            dict(strict=True),
            UnequalIterablesError,
        ), (
            [[1], [2, 3]],
            dict(strict=True),
            UnequalIterablesError,
        )],
)
def test_zip_with_scalars_err(objs, kwargs, error):
    with pytest.raises(error):
        list(zip_with_scalars(*objs, **kwargs))
