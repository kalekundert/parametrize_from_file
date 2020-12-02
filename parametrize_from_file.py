#!/usr/bin/env python3

"""
Parameterize unit tests with values from YAML, TOML, and NT files.
"""

__version__ = '0.0.1'

import sys, pytest, inspect
import json, toml, yaml, nestedtext as nt
from pathlib import Path
from functools import lru_cache
from more_itertools import first
from schema import Schema
from tidyexc import Error

def _load_json(path):
    with open(path) as f:
        return json.load(f)

def _load_yml(path):
    with open(path) as f:
        return yaml.safe_load(f)

LOADERS = {
        '.json': _load_json,
        '.yaml': _load_yml,
        '.yml': _load_yml,
        '.toml': toml.load,
        '.nt': nt.load,
}

def parametrize_from_file(rel_path=None, test_key=None, schema=None):

    def decorator(f):
        try:
            # The path is relative to the file the caller is defined in.
            module = inspect.getmodule(f)
            test_path = Path(module.__file__)

            ConfigError.push_info(
                    "test function: {test_module.__name__}.{test_func.__qualname__}()",
                    test_func=f,
                    test_module=module,
            )
            ConfigError.push_info(
                    "test file: {test_path}",
                    test_path=test_path,
            )

            param_path = _find_param_path(test_path, rel_path)

            ConfigError.push_info(
                    "parameter file: {param_path}",
                    param_path=param_path,
            )

            # suite_params:
            #     All parameters associated with the test file in question.  
            #     This is a dictionary where the keys are test names and the 
            #     values are lists of test parameters (see below).
            #
            # test_params:
            #     All parameters associated with a specific test function.  
            #     This is a list of case parameters (see below).
            #
            # case_params:
            #     A specific set of parameters to test.  This is a dictionary 
            #     of keys and values that will be provided to the actual test 
            #     function.

            suite_params = _load_and_cache_suite_params(param_path)
            test_params = _get_test_params(suite_params, test_key or f.__name__)
            test_params = _validate_test_params(test_params, schema)
            keys, values = _init_parametrize_args(test_params)

            return pytest.mark.parametrize(keys, values)(f)

        finally:
            ConfigError.clear_info()

    if callable(rel_path):
        f, rel_path = rel_path, None
        return decorator(f)
    else:
        return decorator

def _find_param_path(test_path, rel_path):
    if rel_path:
        param_path = test_path.parent / rel_path

        if not param_path.exists():
            err = ConfigError(
                    rel_path=rel_path,
                    param_path=param_path,
            )
            err.brief = "can't find parametrization file"
            err.blame += "'{param_path}' does not exist."
            raise err

        if param_path.suffix not in LOADERS:
            err = ConfigError(
                    rel_path=rel_path,
                    param_path=param_path,
                    known_extensions=LOADERS.keys(),
            )
            err.brief = "parametrization file must have a recognized extension"
            err.info += lambda e: '\n'.join(
                    "the following extensions are recognized:",
                    *e.known_extensions,
            )
            err.blame += "the given extension is not recognized: {param_path.suffix}"
            raise err


    else:
        param_path_candidates = [
                test_path.with_suffix(x)
                for x in LOADERS
        ]
        try:
            param_path = first(
                    x for x in param_path_candidates if x.exists()
            )
        except ValueError:
            err = ConfigError(
                paths=param_path_candidates,
            )
            err.brief = "can't find parametrization file"
            err.info += "no relative path specified"
            err.blame += lambda e: '\n    '.join([
                "none of the following paths exist:",
                *map(str, e.paths),
            ])
            raise err from None

    return param_path

@lru_cache()
def _load_and_cache_suite_params(path):
    # This should be guaranteed by _find_param_path().
    assert path.suffix in LOADERS
    loader = LOADERS[path.suffix]

    try:
        return loader(path)

    except Exception as e:
        err = ConfigError(
                load_func=loader,
        )
        err.brief = "failed to load parametrization file"
        err.info += "attempted to load file with: {load_func}"
        err.blame += str(e)
        raise err

def _get_test_params(suite_params, test_name):
    try:
        return suite_params[test_name]

    except KeyError:
        err = ConfigError(
                test_name=test_name,
        )
        err.brief += "must specify parameters for '{test_name}'"
        err.hints += "make sure the top-level data structure in the parameter file is a dictionary where the keys are the names of test functions, and the values are dictionaries of test parameters."
        raise err from None

def _validate_test_params(test_params, schema):
    if schema is None:
        return test_params
    else:
        return Schema([schema]).validate(test_params)

def _init_parametrize_args(test_params):
    # Convert the keys into a list to better define their order.  It's 
    # important that the values are arranged in the same order as the keys, 
    # otherwise they might not be matched correctly.  The sorting is just to 
    # make testing easier.
    keys = sorted(_check_test_params_keys(test_params))

    def get_id(case_params, i):
        return case_params.get('id', str(i))

    def get_marks(case_params):
        try:
            marks = case_params['marks']
        except KeyError:
            return ()

        if isinstance(marks, str):
            marks = marks.split(',')

        return [getattr(pytest.mark, x) for x in marks]

    values = [
            pytest.param(
                *(x[k] for k in keys),
                id=get_id(x, i),
                marks=get_marks(x),
            )
            for i, x in enumerate(test_params, 1)
    ]
    return keys, values

def _check_test_params_keys(test_params):
    # We don't need to check if the keys match the arguments to the test 
    # function, because pytest will do that for us.  We just need to check that 
    # the keys are consistent with each other, and to raise a good error if 
    # they aren't.
    special_keys = {'id', 'marks'}
    test_param_keys = set.union(set(), *(set(x) for x in test_params)) - special_keys

    for case_params in test_params:
        missing = test_param_keys - set(case_params)
        if missing:
            err = ConfigError(
                    params=case_params,
                    missing=missing,
            )
            err.brief = "every test case must specify the same parameters"
            err.info += lambda e: "\n    ".join([
                "test case:",
                *(f'{k}: {v}' for k, v in e.params.items())
            ])
            err.blame += lambda e: "\n    ".join([
                "the following parameters are missing:",
                *e.missing,
            ])
            raise err

    return test_param_keys

class Params:

    @classmethod
    def parametrize(cls, f):
        args = cls.args

        params = []
        for k, v in cls.__dict__.items():
            if k.startswith('params'):
                params.extend(v)

        # Could also check to make sure parameters make sense.

        return pytest.mark.parametrize(args, params)(f)

class ConfigError(Error):
    pass

# Hack to make the module directly usable as a decorator.  Only works for 
# python 3.5 or higher.  See this Stack Overflow post:
# https://stackoverflow.com/questions/1060796/callable-modules

class CallableModule(sys.modules[__name__].__class__):

    def __call__(self, *args, **kwargs):
        return parametrize_from_file(*args, **kwargs)

sys.modules[__name__].__class__ = CallableModule
