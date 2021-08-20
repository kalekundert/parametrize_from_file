#!/usr/bin/env python3

import pytest
import inspect

from .loaders import get_loaders
from .errors import ConfigError
from pathlib import Path
from functools import lru_cache
from textwrap import indent
from more_itertools import first
from copy import copy

def parametrize_from_file(path=None, key=None, schema=lambda x: x):
    """
    Parametrize a test function with values read from a config file.

    Arguments:
        path (str,pathlib.Path):
            The path to the parameter file, relative to the directory containing 
            the test file.  By default, the parameter file will be assumed to 
            have the same base name as the test file and one of the extensions 
            listed in the file format table below.

        key (str):
            The key that will be used to identify the parameters affiliated 
            with the decorated test function.  The default is to use the name 
            of the test function.  See below for more detail about the 
            structure of the parameters file.

        schema (collections.abc.Callable):
            A function that will be used to validate and/or transform each set 
            of parameters.  The function should have the following signature::

                def schema(params: Dict[str: Any]) -> Dict[str, Any]:

            The argument will be a single set of parameters, exactly as they 
            were read from the file.  The return value will be used to actually 
            parametrize the test function.  It's ok to add or remove keys from 
            the input dictionary, but keep in mind that every set of parameters 
            for a single test function must ultimately have the same keys.

            While it's possible to write your own schema functions, this 
            argument is meant to be used in conjunction with a schema library 
            such as voluptuous_ or schema_.

    The parameter file must be in one of the following formats, and must have a 
    corresponding file extension:

    ===========  ============
    Format       Extensions
    ===========  ============
    JSON_        .json
    YAML_        .yml .yaml
    TOML_        .toml
    NestedText_  .nt
    ===========  ============

    The top-level data structure in the parameter file should be a dictionary.  
    The keys of this dictionary should be the names of the individual tests, 
    and the values should be lists of parameter sets to provide to that test.  
    Each parameter set should be a dictionary, with the keys being the names of 
    the parameters and the values being the parameters themselves.  Each 
    parameter set within a list must have the same set of keys (except for the 
    specially-treated *id* and *marks* keys, described below).  There are no 
    restrictions on the values of the parameters (e.g. different parameter sets 
    within the same list can have values of different types).

    For example, here is a valid YAML_ parameter file.  This file specifies two 
    sets of parameters for each of two tests:

    .. code-block:: yaml

        test_addition:
          - operands: [0, 0]
            expected: 0

          - operands: [0, 1]
            expected: 1

        test_subtraction:
          - operands: [0, 0]
            expected: 0

          - operands: [0, 1]
            expected: -1

    There are two parameter names that are treated specially:
    
    :param str id:
      A name that will be used by pytest to refer to this particular set of 
      parameters, e.g. if they cause a test failure.  If not given, the 
      parameter set will be assigned a numeric id that counts up from 1.  It's 
      ok for multiple test cases to have the same id; pytest will distinguish 
      them by appending a numeric id that counts up from 0.
    
    :param str,list marks:
      One or more :doc:`marks <mark>` (like `skip <pytest.mark.skip>` or `xfail 
      <pytest.mark.xfail>`) that should be applied this particular set of 
      parameters.  If a plain string is given, it will be split on commas.  If 
      a list is given, each element should be a string.  Pytest will issue a 
      warning if you use a mark that it doesn't recognize.

    This decorator can be used with or without arguments, and the 
    :mod:`parametrize_from_file` module itself can be used directly as a 
    decorator.  The decorated function should accept arguments with the same 
    names as each of its parameters specified in the file.  It is possible to 
    decorate the same test function multiple times: all combinations of 
    parameters specified in this way will be tested.  Likewise, this decorator 
    can be combined freely with the `pytest.mark.parametrize ref` decorator.

    Example:
        Load parameters from a NestedText_ file, and assign types using a 
        schema:

        .. code-block:: yaml

            # test_utils.nt
            test_is_even:
              - 
                value: 1
                expected: False
              - 
                value: 2
                expected: True

        .. code-block:: py

            # test_utils.py
            import parametrize_from_file
            from voluptuous import Schema

            def is_even(x):
                return x % 2 == 0

            @parametrize_from_file(schema=Schema({str: eval}))
            def test_is_even(value, expected):
                assert is_even(value) == expected
    """

    def decorator(f):
        try:
            # The path is relative to the file the caller is defined in.
            module = inspect.getmodule(f)
            test_path = Path(module.__file__)

            ConfigError.push_info(
                    "test function: {test_func.__qualname__}()",
                    test_func=f,
                    test_module=module,
            )
            ConfigError.push_info(
                    "test file: {test_path}",
                    test_path=test_path,
            )

            param_path = _find_param_path(test_path, path)

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
            test_params = _get_test_params(suite_params, key or f.__name__)
            test_params = _validate_test_params(test_params, schema)
            keys, values = _init_parametrize_args(test_params)

            return pytest.mark.parametrize(keys, values)(f)

        finally:
            ConfigError.clear_info()

    if callable(path):
        f, path = path, None
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

        if param_path.suffix not in get_loaders():
            err = ConfigError(
                    rel_path=rel_path,
                    param_path=param_path,
                    known_extensions=get_loaders().keys(),
            )
            err.brief = "parametrization file must have a recognized extension"
            err.info += lambda e: '\n'.join((
                    "the following extensions are recognized:",
                    *e.known_extensions,
            ))
            err.blame += "the given extension is not recognized: {param_path.suffix}"
            raise err


    else:
        param_path_candidates = [
                test_path.with_suffix(x)
                for x in get_loaders()
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
            err.blame += lambda e: '\n'.join([
                "none of the following default paths exist:",
                *map(str, e.paths),
            ])
            raise err from None

    return param_path

@lru_cache()
def _load_and_cache_suite_params(path):
    # This should be guaranteed by _find_param_path().
    assert path.suffix in get_loaders()
    loader = get_loaders()[path.suffix]

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
    validated_params = []

    def stash_id_marks(obj):
        params = {}
        stash = {}

        for key, value in obj.items():
            if key in ('id', 'marks'):
                stash[key] = value
            else:
                params[key] = value

        return params, stash

    if not isinstance(test_params, list):
        raise ConfigError(
                "expected list of dicts, got {params!r}",
                params=test_params,
        )

    for case_params in test_params:
        if not isinstance(case_params, dict):
            raise ConfigError(
                    "expected dict, got {params!r}",
                    params=case_params,
            )

        params, stash = stash_id_marks(case_params)

        try:
            params = schema(params)
        except Exception as err1:
            err2 = ConfigError(
                    params=case_params,
            )
            err2.brief = "test case failed schema validation"
            err2.info += lambda e: (
                    "test case:\n" +
                    _format_case_params(e.params)
            )
            err2.blame += str(err1)
            raise err2 from err1

        params.update(stash)
        validated_params.append(params)

    return validated_params

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
            err.info += lambda e: (
                    "test case:\n" +
                    indent(_format_case_params(e.params), "    ")
            )
            err.blame += lambda e: (
                "the following parameters are missing:\n" +
                '\n'.join(e.missing)
            )
            raise err

    return test_param_keys

def _format_case_params(case_params):
    """
    Format a set of case parameters for inclusion in an error message.  Account 
    for the fact that while the case parameters are supposed to be a 
    dictionary, they could be anything.
    """
    try:
        return "\n".join(
                f'{k!r}: {v!r}' for k, v in case_params.items()
        )
    except:
        return repr(case_params)

