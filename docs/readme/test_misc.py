#!/usr/bin/env python3

import parametrize_from_file

@parametrize_from_file
def test_addition(a, b, c):
    assert a + b == c
