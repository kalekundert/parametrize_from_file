#!/usr/bin/env python3

"""
Parametrize test functions with values read from config files.

Note that this module itself can be used as an alias for `parametrize`, e.g.:

.. code-block::

    import parametrize_from_file

    @parametrize_from_file
    def test_my_func(given, expected):
        assert my_func(given) == expected

This is the recommended usage if you do not need to import any other names from 
the module.  If you do need to import other names, the recommendation is 
instead to import the module as ``pff``, e.g.:

.. code-block::

    import parametrize_from_file as pff

    @pff.fixture
    def env(request):
        return request.param

    @pff.parametrize
    def test_my_func(given, expected, env):
        assert my_func(given) == expected
"""

from .parameters import parametrize, fixture, load_parameters
from .namespace import Namespace, star
from .schema import defaults, cast, error, error_or
from .loaders import add_loader, drop_loader
from .errors import ConfigError

__version__ = '0.17.0'

for obj in [parametrize, fixture, Namespace, star, defaults, cast, error, error_or, add_loader, drop_loader, load_parameters, ConfigError]:
    obj.__module__ = 'parametrize_from_file'

del obj

# Hack to make the module directly usable as a decorator.  Only works for 
# python 3.5 or higher.  See this Stack Overflow post:
# https://stackoverflow.com/questions/1060796/callable-modules

import sys
import functools

class CallableModule(sys.modules[__name__].__class__):

    def __call__(self, *args, **kwargs):
        return parametrize(*args, **kwargs)

sys.modules[__name__].__class__ = CallableModule
del sys, functools, CallableModule
