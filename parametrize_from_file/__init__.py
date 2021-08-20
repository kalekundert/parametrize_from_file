#!/usr/bin/env python3

"""
Parametrize test functions with values read from config files.
"""

from .parametrize import parametrize_from_file
from .namespace import Namespace
from .loaders import add_loader, drop_loader
from .errors import ConfigError

__version__ = '0.4.0'

for obj in [Namespace, ConfigError, add_loader, drop_loader]:
    obj.__module__ = 'parametrize_from_file'

# Hack to make the module directly usable as a decorator.  Only works for 
# python 3.5 or higher.  See this Stack Overflow post:
# https://stackoverflow.com/questions/1060796/callable-modules

import sys
import functools

class CallableModule(sys.modules[__name__].__class__):

    @functools.wraps(parametrize_from_file)
    def __call__(self, *args, **kwargs):
        return parametrize_from_file(*args, **kwargs)

sys.modules[__name__].__class__ = CallableModule
del sys, functools, CallableModule
