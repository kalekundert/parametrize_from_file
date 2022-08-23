import pytest, re
from .errors import ConfigError
from unittest.mock import MagicMock
from more_itertools import always_iterable
from contextlib2 import nullcontext

def cast(**funcs):
    """
    Return a schema function that will apply functions to the given test 
    parameters.

    Arguments:
        funcs (dict):
            Keyword arguments where each key is the name of a parameter and 
            each value is either a function or a list of functions to transform 
            that parameter with.  When lists of functions are given, the 
            functions will be applied in order, with the return value of each 
            becoming the input to the next.

    Any keys that are missing will be silently ignored; this makes it easier to 
    provide default values with `defaults`.  Note that if you use `defaults` 
    before `cast`, then the default values will be transformed as if they had 
    been read from the parameter file.  In contrast, if you use `cast` before 
    `defaults`, then the default values will be used directly.

    See the :doc:`/python_snippets` and :doc:`/optional_params` tutorials for 
    some good in-context examples.

    Example:

        >>> f = cast(a=int)
        >>> f({'a': '1'})
        {'a': 1}
        >>> f({})
        {}
        >>> from math import sqrt
        >>> g = cast(a=[int, sqrt])
        >>> g({'a': '4'})
        {'a': 2.0}
    """

    def schema(params):
        for key, func in funcs.items():
            if key in params:
                for f in always_iterable(func):
                    params[key] = f(params[key])

        return params

    return schema

def defaults(**defaults):
    """
    Return a schema function that will add the given default values to test 
    cases.  In other words, this is an easy way to provide default values for 
    one or more test parameters.

    Arguments:
        defaults:
            Keyword arguments where each key is the name of a parameter and 
            each value is the corresponding default.

    See the :doc:`/optional_params` tutorial more much more info.

    Example:
        
        >>> f = defaults(a=0, b=0)
        >>> f({'b': 1})
        {'a': 0, 'b': 1}
    """
    return lambda params: {**defaults, **params}

def error(exc_spec, *, globals=None):
    """\
    Create a context manager that will check that the specified exception is
    raised.

    Arguments:
        exc_spec (str, list, dict):
            This argument specifies what kind of exception to expect (and 
            optionally how to check various aspects of it).

            If string: A string that evaluates to an exception type.  This can 
            also be ``"none"`` to specify that the returned context manager 
            should not expect any exception to be raised.

            If list: A list of the above strings that evaluate to exception 
            types.  The actual exception must be one of these types.

            If dict: The following keys are understood:

            - "type" (required): A string or list of strings that evaluate 
              to exception types.  The context manager will require that 
              an exception of one of the given types is raised.

            - "message" (optional): A string or list of strings that should 
              appear verbatim in the error message.

            - "pattern" (optional): A string or list of strings 
              representing patterns that should appear in the error 
              message.  Each string is interpreted as a regular expression, 
              in the same manner as the *match* argument to 
              `pytest.raises`.

            - "attrs" (optional): A dictionary of attributes that the 
              exception object should have.  The dictionary keys give the 
              attribute names, and should be strings.  The dictionary 
              values give the attribute values, and should also be strings.  
              Each value string will be evaluated in the context of the given  
              namespace to get the expected values.

            - "assertions" (optional): A string containing python code that 
              will be executed when the expected exception is detected.  Any 
              *globals* specified will be available to this code.  In addition, 
              the exception object itself will be available via the *exc* 
              variable.  This field is typically used to make free-form 
              assertions about the exception object.

            - "cause" (optional): An integer (or string that can be converted 
              to an integer) 'n'.  All other checks will apply to the n-th 
              direct cause of the caught exception, instead of the exception 
              itself.  This is useful in cases where the exception you want to 
              test is wrapped in some other exception.

            Note that string values are accepted for every one of these keys, 
            because this method is meant to help with parsing exception 
            information from a text file, e.g. in the NestedText_ format.  All 
            evaluations and executions are deferred for as long as possible.

        globals (dict):
            The global variables to use when evaluating/executing code related 
            to the exception.  This can be any kind of mapping, including 
            `Namespace`.  By default, only the built-in variables are 
            available.

    Returns:
        A context manager that can be used to check if the kind of 
        exception specified by *exc_spec* was raised.

    Examples:
        Using a built-in exception (so no need to specify a namespace) and not 
        checking the error message::

            >>> p = {'type': 'ZeroDivisionError'}
            >>> with error(p):
            ...    1/0

        Using a custom exception::

            >>> class MyError(Exception):
            ...     pass
            ...
            >>> with_err = Namespace(MyError=MyError)
            >>> p = {'type': 'MyError', 'pattern': r'\\d+'}
            >>> with with_err.error(p):
            ...    raise MyError('404')

    Details:
        The returned context manager is re-entrant, which makes it possible 
        to stack :deco:`parametrize_from_file` invocations that make use of 
        method (e.g. via the *schema* argument).
    """

    if exc_spec == 'none':
        return ExpectSuccess()

    err = ExpectError(globals=globals)

    if isinstance(exc_spec, str):
        err.type_str = exc_spec
    else:
        def require_list(x):
            return x if isinstance(x, list) else [x]

        err.type_str = exc_spec['type']
        err.messages = require_list(exc_spec.get('message', []))
        err.patterns = require_list(exc_spec.get('pattern', []))
        err.attr_strs = exc_spec.get('attrs', {})
        err.assertions_str = exc_spec.get('assertions', '')
        err.cause_str = exc_spec.get('cause', '')

    return err

def error_or(*expected, globals=None, param='error', mock_factory=MagicMock):
    """
    Return a schema function that will expect to be given either an error or 
    the specified set of expected values.

    Arguments:
        expected (str):
            Any test parameters that must be specified when an exception is 
            *not* expected.  These parameters will be replaced with mocks when 
            an exception is expected.

        globals (dict):
            The global variables to use when building the `error` context 
            manager, e.g. for evaluating the exception type.  This can be any 
            kind of mapping, including `Namespace`.

        param (str):
            The name of the test parameter specifying the expected exception.

        mock_factory (Callable):
            A no-argument callable that can be used to create mock expected 
            values when an exception is expected.

    The purpose of this schema is to make it easier to test functions that can 
    raise exceptions.  Towards this end, this schema understands two sets of 
    parameters: one that defines an expected outcome when no exceptions are 
    expected, and another that defines an expected exception.  These parameter 
    sets are mutually exclusive: you cannot specify both at once.

    By default, exceptions are specified using the *error* parameter.  (The 
    name of this parameter can be changed via the *param* argument.)  If this 
    parameter is found, it will be processed by |NS_error|.  That means: (i) it 
    should match the format expected by that method and (ii) it will be 
    converted into a context manager that can be used to detect whether the 
    expected exception was in fact raised.  All of the *expected* keys will be 
    added to the output dictionary, and will be set to |MagicMock| objects.  
    These mocks are pretty good at standing in for other objects, so if you 
    need to do some mild processing on the expected values before performing 
    the actual test, it will often just work.  When it doesn't, the *error* 
    parameter will be truthy if an exception is expected and falsey otherwise, 
    so you can use that information to skip this kind of processing as 
    necessary.

    If the *error* parameter is not given, the resulting output will contain an 
    *error* key set to a no-op context manager.  All of the *expected* keys 
    will be passed through unchanged.

    For more information, see the :doc:`/exceptions` tutorial.

    Example:
        This example is somewhat contrived, but it shows how to easily test a 
        function that raises a custom exception for certain inputs.
        
           >>> from parametrize_from_file import Namespace, error_or

           >>> class DontGreet(Exception):
           ...     pass
           ...
           >>> def greet(name):
           ...     if name == 'Bob':
           ...         raise DontGreet(name)
           ...     return f"Hello, {name}!"
           ...
           >>> with_greet = Namespace(globals())
           >>> schema = with_greet.error_or('expected')
           >>> p1 = schema({
           ...         'given': 'Alice',
           ...         'expected': 'Hello, Alice!',
           ... })
           >>> with p1['error']:
           ...    assert greet(p1['given']) == p1['expected']
           ...
           >>> p2 = schema({
           ...         'given': 'Bob',
           ...         'error': {
           ...             'type': 'DontGreet',
           ...             'message': 'Bob',
           ...         },
           ... })
           >>> with p2['error']:
           ...    assert greet(p2['given']) == p2['expected']
           ...
        
        Note that the with block is the exact same for both assertions, even 
        though one tests for an error and the other doesn't.  This is what 
        makes `error_or()` useful for writing parametrized tests.
    """

    error_key = param

    def schema(params):
        if error_key not in params:
            params[error_key] = ExpectSuccess()

        else:
            bad_keys = set(params) & set(expected)
            if bad_keys:
                err = ConfigError(
                        bad_keys=bad_keys,
                        error_key=error_key,
                )
                err.brief = "must specify either an expected value or an error, not both"
                err.info += lambda e: f"expected value parameter(s): {','.join(e.bad_keys)}"
                err.info += "error parameter: {error_key}"
                raise err

            params[error_key] = error(
                    params[error_key],
                    globals=globals,
            )
            for key in expected:
                params[key] = mock_factory()

        return params

    return schema

class ExpectSuccess(nullcontext):

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def __bool__(self):
        return False

class ExpectError:

    # Normally I'd use `@contextmanager` to make a context manager like this, 
    # but generator-based context managers cannot be reused.  This is a problem 
    # for tests, because if a test using this context manager is parametrized, 
    # the same context manager instance will need to be reused multiple times.  
    # The only way to support this is to implement the context manager from 
    # scratch.

    def __init__(self, *, globals=None, type_str=Exception, messages=[], patterns=[], attr_strs={}, assertions_str='', cause_str=''):
        if globals is None:
            globals = {}

        self.globals = globals
        self.type_str = type_str
        self.messages = messages
        self.patterns = patterns
        self.attr_strs = attr_strs
        self.assertions_str = assertions_str
        self.cause_str = cause_str

    def __repr__(self):
        attrs = {
                'type': self.type_str,
                'messages': self.messages,
                'patterns': self.patterns,
                'attrs': self.attr_strs,
                'assertions': self.assertions_str,
                'cause': self.cause_str,
        }
        attr_str = ' '.join(
                f'{k}={v!r}'
                for k, v in attrs.items() if v
        )
        return f'<{self.__class__.__name__} {attr_str}>'

    def __bool__(self):
        return True

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        from .namespace import Namespace

        # Don't include this method in stack traces generated by pytest.
        __tracebackhide__ = True

        ns = Namespace(self.globals)
        type = ns.eval(self.type_str)
        if isinstance(type, list):
            type = tuple(type)

        assert exc_type is not None, f"DID NOT RAISE {type}"

        del exc_type, exc_tb
        for i in range(int(self.cause_str or 0)):
            assert exc_value.__cause__ is not None, f"{exc_value.__class__.__name__} has no direct cause"
            exc_value = exc_value.__cause__

        if not isinstance(exc_value, type):
            return False

        exc_str = str(exc_value)

        for msg in self.messages:
            assert msg in exc_str, f'{msg!r} not in {exc_str!r}'

        for pat in self.patterns:
            assert re.search(pat, exc_str), "regex pattern {pat!r} does not match {exc_str!r}"

        for attr, value_str in self.attr_strs.items():
            assert hasattr(exc_value, attr)
            assert getattr(exc_value, attr) == ns.eval(value_str)

        if self.assertions_str:
            ns.fork(exc=exc_value).exec(self.assertions_str)

        return True

