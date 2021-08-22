#!/usr/bin/env python3

import pytest
import inspect

from .loaders import get_loaders
from .utils import zip_with_scalars, is_iterable
from .errors import ConfigError
from pathlib import Path
from functools import lru_cache
from textwrap import indent
from more_itertools import first, UnequalIterablesError
from copy import copy

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

def parametrize_from_file(
        path=None,
        key=None,
        *,
        preprocess=None,
        schema=None,
    ):
    """
    Parametrize a test function with values read from a config file.

    Arguments:
        path (str,pathlib.Path,list):
            The path to the parameter file, relative to the directory 
            containing the test file.  By default, the parameter file will be 
            assumed to have the same base name as the test file and one of the 
            extensions listed in the file format table below.

            If multiple paths are specified, the parameters from each will be 
            loaded and concatenated.  The *key* argument in this case must be 
            either be a string (meaning: lookup the same key in each file) or a 
            list of strings with the same length as this argument (meaning: 
            look up the corresponding key in each file).

        key (str,list):
            The key that will be used to identify the parameters affiliated 
            with the decorated test function.  The default is to use the name 
            of the test function.  See below for more detail about the 
            structure of the parameters file.

            If multiple keys are specified, the parameters for each will loaded 
            and concatenated.  The *path* argument in this case must be either 
            a single path (meaning: lookup all keys in the same file) or a list 
            of paths with the same length as this argument (meaning: look up 
            each key in the corresponding file).

        preprocess (collections.abc.Callable):
            A function that will be allowed to modify the list of test cases 
            loaded from the parameter file, e.g. to programmatically generate 
            and/or prune test cases.  The function should have the following 
            signature::

                def preprocess(params: Any) -> List[Dict[str, Any]]

            The argument will be the value associated with the given key in the 
            parameter file.  Typically this value is a list, but it could be 
            anything.  If multiple parameter files and/or keys are specified, 
            this function is called separately on each one.  The return value 
            must be a list of dicts.  Each of these dicts will be further 
            processed by the *schema* argument before being used to parametrize 
            the test function.  Note that this function does get access to the 
            special *id* and *marks* fields, unlike the *schema* function.

        schema (collections.abc.Callable):
            A function that will be used to validate and/or transform each set 
            of parameters.  The function should have the following signature::

                def schema(params: Dict[str: Any]) -> Dict[str, Any]:

            The argument will be the set of parameters for a single test case, 
            excluding the special *id* and *marks* fields.  The return value 
            will be used to actually parametrize the test function.  It's ok to 
            add or remove keys from the input dictionary, but keep in mind that 
            every set of parameters for a single test function must ultimately 
            have the same keys.  The schema may also set the *id* and *marks* 
            fields, but any values set in the file will override those set by 
            the schema.

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
        # The path is relative to the file the caller is defined in.
        module = inspect.getmodule(f)
        test_path = Path(module.__file__)

        with ConfigError.add_info(
                "test function: {test_func.__qualname__}()",
                "test file: {test_path}",
                test_func=f,
                test_module=module,
                test_path=test_path,
        ):
            keys, values = load_parameters(
                    _resolve_param_path(test_path, path),
                    key or f.__name__,
                    preprocess=preprocess,
                    schema=schema,
            )
            return pytest.mark.parametrize(keys, values)(f)

    if callable(path):
        f, path = path, None
        return decorator(f)
    else:
        return decorator

def load_parameters(
        path,
        key,
        *,
        preprocess=None,
        schema=None,
    ):
    """
    Load test parameters from a file.

    Arguments:
        path (str, pathlib.Path, list):
            The path to the file containing the parameters.  Unlike with 
            :deco:`parametrize_from_file`, this path is expected to be 
            absolute.  If it's not absolute, it's interpreted relative to the 
            current working directory.

        key (str, list):
            See: :deco:`parametrize_from_file`

        preprocess (collections.abc.Callable):
            See: :deco:`parametrize_from_file`

        schema (collections.abc.Callable):
            See: :deco:`parametrize_from_file`

    Returns:
        tuple:
            - A list of parameter names
            - A list of `pytest.param` instances

    This function does almost the same thing as :deco:`parametrize_from_file`, 
    except that instead of decorating a test function, it simply returns the 
    parameters it loads.  This might be useful in some unusual situations.  For 
    example, you could use this function to load test parameters from a file in 
    order to merge them with parameters derived from some other source and 
    apply them all to the same test function.
    """
    test_params = []

    try:
        for path_i, key_i in zip_with_scalars(path, key, strict=True):
            with ConfigError.add_info(
                    "parameter file: {param_path}",
                    param_path=path_i,
            ):
                p = _load_test_params(path_i, key_i)

                with ConfigError.add_info(
                        "top-level key: {key}",
                        key=key_i,
                ):
                    p = _process_test_params(p, preprocess, schema)
                    test_params += p

    except UnequalIterablesError:
        err = ConfigError(
                paths=path,
                keys=key,
        )
        err.brief = "must specify matching numbers of paths and keys"
        err.info += "paths: {paths!r}"
        err.info += "keys: {keys!r}"
        raise err

    return _init_parametrize_args(test_params)


def _resolve_param_path(test_path, rel_path):
    if rel_path:
        if is_iterable(rel_path):
            return [test_path.parent / p for p in rel_path]
        else:
            return test_path.parent / rel_path

    param_path_candidates = [
            test_path.with_suffix(x)
            for x in get_loaders()
    ]
    param_paths = [
            x for x in param_path_candidates if x.exists()
    ]

    if len(param_paths) < 1:
        err = ConfigError(
                paths=param_path_candidates,
        )
        err.brief = "can't find parametrization file"
        err.info += "no relative path specified"
        err.blame += lambda e: '\n'.join([
            "none of the following default paths exist:",
            *map(str, e.paths),
        ])
        raise err

    if len(param_paths) > 1:
        err = ConfigError(
                paths=param_paths,
        )
        err.brief = "found multiple parametrization files"
        err.info += "no relative path specified"
        err.blame += lambda e: '\n'.join([
            "don't know which file to use:",
            *map(str, e.paths),
        ])
        raise err

    return param_paths[0]

@lru_cache()
def _load_and_cache_suite_params(param_path):
    if not param_path.exists():
        err = ConfigError(
                param_path=param_path,
        )
        err.brief = "can't find parametrization file"
        err.blame += "'{param_path}' does not exist."
        raise err

    loaders = get_loaders()

    try:
        loader = loaders[param_path.suffix]

    except KeyError:
        err = ConfigError(
                param_path=param_path,
                known_extensions=loaders.keys(),
        )
        err.brief = "parametrization file must have a recognized extension"
        err.info += lambda e: '\n'.join((
                "the following extensions are recognized:",
                *e.known_extensions,
        ))
        err.blame += "the given extension is not recognized: {param_path.suffix}"
        raise err from None

    try:
        return loader(param_path)

    except Exception as e:
        err = ConfigError(
                load_func=loader,
        )
        err.brief = "failed to load parametrization file"
        err.info += "attempted to load file with: {load_func.__module__}.{load_func.__qualname__}()"
        err.blame += str(e)
        raise err from None

def _load_test_params(param_path, test_name):
    suite_params = _load_and_cache_suite_params(param_path)

    try:
        return suite_params[test_name]

    except KeyError:
        err = ConfigError(
                test_name=test_name,
        )
        err.brief += "must specify parameters for '{test_name}'"
        err.hints += "make sure the top-level data structure in the parameter file is a dictionary where the keys are the names of test functions, and the values are dictionaries of test parameters."
        raise err from None

def _process_test_params(test_params_in, preprocess, schema):
    if preprocess:
        test_params_in = preprocess(test_params_in)

    if not isinstance(test_params_in, list):
        raise ConfigError(
                lambda e: (
                    f"expected preprocess to return list of dicts, got {e.params!r}"
                    if e.preprocess else
                    f"expected list of dicts, got {e.params!r}"
                ),
                params=test_params_in,
                preprocess=preprocess,
        )

    test_params_out = []

    def stash_id_marks(obj):
        params = {}
        stash = {}

        for key, value in obj.items():
            if key in ('id', 'marks'):
                stash[key] = value
            else:
                params[key] = value

        return params, stash

    for case_params_in in test_params_in:
        if not isinstance(case_params_in, dict):
            raise ConfigError(
                    "expected dict, got {params!r}",
                    params=case_params_in,
            )

        if not schema:
            case_params_out = case_params_in
        else:
            params, stash = stash_id_marks(case_params_in)

            try:
                params = schema(params)
            except Exception as err1:
                err2 = ConfigError(
                        params=case_params_in,
                )
                err2.brief = "test case failed schema validation"
                err2.info += lambda e: (
                        "test case:\n" +
                        _format_case_params(e.params)
                )
                err2.blame += str(err1)
                raise err2 from err1

            if not isinstance(params, dict):
                raise ConfigError(
                        "expected schema to return dict, got {params!r}",
                        params=params,
                )

            case_params_out = {**params, **stash}

        test_params_out.append(case_params_out)

    return test_params_out

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

