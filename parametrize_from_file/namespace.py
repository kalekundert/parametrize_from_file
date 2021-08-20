#!/usr/bin/env python3

import pytest
from copy import copy
from collections.abc import Mapping
from contextlib2 import nullcontext
from functools import partial

class Namespace(dict):
    """\
    Evaluate and/or execute snippets of python code, with powerful control over the 
    names available to those snippets.

    .. note::
    
        It is conventional to:

        - Name your namespaces: ``with_{short description}``

        - Create any namespaces you will need in a single helper file (e.g.  
          ``param_helpers.py``) to be imported in test scripts as necessary.

    Examples:

        The first step when using a namespace specify which names it should 
        include.   This can be done using...

        ...strings (which will be `python:exec`'d):
            
            >>> with_math = Namespace('import math')
            >>> with_math.eval('math.sqrt(4)')
            2.0

        ...dictionaries:

            >>> import math
            >>> with_math = Namespace(globals())
            >>> with_math.eval('math.sqrt(4)')
            2.0

        ...keyword arguments:

            >>> with_math = Namespace(math=math)
            >>> with_math.eval('math.sqrt(4)')
            2.0

        ...other namespaces (`Namespace.use` works just like the constructor):

            >>> with_np = with_math.copy().use('import numpy as np')
            >>> with_np.eval('np.arange(3) * math.sqrt(4)')
            array([0., 2., 4.])

        ...the `Namespace.all` method:

            >>> with_math = Namespace().all(math)
            >>> with_math.eval('sqrt(4)')
            2.0

        Once you have an initialized a namespace, you can use it to...

        ...evaluate expressions:

            >>> with_math.eval('sqrt(4)')
            2.0
            
        ...execute blocks of code:

            >>> ns = with_math.exec('''
            ... a = sqrt(4)
            ... b = sqrt(9)
            ... ''')
            >>> ns['a']
            2.0
            >>> ns['b']
            3.0
            >>> ns.eval('a + b')
            5.0

        ...make error-detecting context managers:

            >>> class MyError(Exception):
            ...     pass
            ...
            >>> with_err = Namespace(MyError=MyError)
            >>> err_cm = with_err.error({'type': 'MyError', 'message': r'\\d+'})
            >>> with err_cm:
            ...    raise MyError('404')

    If you plan to use a namespace as part of a schema, you probably want 
    `voluptuous.Namespace` instead of this class.
    """

    def __init__(self, *args, **kwargs):
        """
        See `use`.
        """
        super().__init__()
        self.use(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    def use(self, *args, **kwargs):
        """
        Add the given names to the namespace.

        Arguments:
            args (str,dict):
                If string: The string will be executed as python code and any 
                names that are defined by that code will be added to the 
                namespace.  Any names previously added to the namespace will be 
                available to the code.

                If dict: The items in the dictionary will the directly added to 
                the namespace.  All of the dictionary keys must be strings.

                The *args* are processed in order, so later *args* may 
                overwrite earlier *args*.

            kwargs:
                Each key/value pair will be added to the namespace.  The 
                *kwargs* are processed after the *args*, so if the same key is 
                defined by both, the *kwargs* definition will be used.

        Returns:
            The namespace itself is returned, to support method chaining.
        """
        for arg in args:
            if isinstance(arg, Mapping):
                self.update(arg)
            else:
                exec(arg, self)

        self.update(kwargs)
        return self

    def all(self, module):
        """
        Add all names from the given module to the namespace.

        This method follows the same rules as ``from <module> import *``:

        - If the given module defines ``__all__``, only those names will be 
          used.
        - Otherwise, all names without leading underscores will be used.

        Returns:
            The namespace itself is returned, to support method chaining.
        """
        try:
            keys = module.__all__
        except AttributeError:
            keys = (k for k in module.__dict__ if not k.startswith('_'))

        self.update({
                k: module.__dict__[k]
                for k in keys
        })
        return self

    def copy(self):
        """
        Return a shallow copy of this namespace.  This is meant to help support 
        method chaining.
        """
        return copy(self)

    def eval(self, *src, eval_keys=False):
        """
        Evaluate the given expression within this namespace.
        this object.

        Arguments:
            src (str,list,dict):
                The expression (or expressions) to evaluate.  Strings are 
                directly evaluated.  List items and dict values are recursively 
                evaluated.  Dict keys are not evaluated unless *eval_keys* is 
                true.  This allows you to switch freely between structured text 
                and python syntax, depending on which makes most sense for each 
                particular input.

            eval_keys (bool):
                If true, evaluate dictionary keys.  Disabled by default because 
                most dictionary keys are strings, and it's annoying to have to 
                quote them.

        Returns:
            Any: The result of evaluating the given expressions.  
        """
        src = src[0] if len(src) == 1 else list(src)
        recurse = partial(self.eval, eval_keys=eval_keys)

        if type(src) is list:
            return [recurse(x) for x in src]
        elif type(src) is dict:
            f = recurse if eval_keys else lambda x: x
            return {f(k): recurse(v) for k, v in src.items()}
        else:
            return eval(src, self)

    def exec(self, src):
        """
        Execute the given python snippet within this namespace.

        Arguments:
            src (str): A snippet of python code to execute.

        Returns:
            Namespace: A new namespace containing all of the variables defined 
            in the snippet.

        """
        globals = self.copy()
        exec(src, globals)
        return globals

    def exec_and_lookup(self, key):
        """
        Execute a python snippet and return a specific variable.

        Arguments:
            key (str, collections.abc.Callable):
                If string: the name of the variable to return.  
                
                If callable: The given function will be passed a dictionary 
                containing all the names defined in the given snippet.  
                Whatever that function returns will be passed on to the caller.

        Returns:
            collections.abc.Callable:
                A closure that takes a snippet of python code, executes it, and 
                returns the value indicated by the given key.  While it may 
                seem counter-intuitive for this method to return a 
                snippet-executing function instead of simply executing snippets 
                itself, this API is designed to be used when defining schemas.  
                Be aware that having schemas execute large blocks of code is 
                usually a :ref:`bad idea <schema-be-careful>`, though.
        """

        def do_exec(src):
            globals = self.exec(src)

            if callable(key):
                return key(globals)
            else:
                return globals[key]

        return do_exec

    def error(self, params):
        """\
        Create a context manager that will check that a particular error is 
        raised.

        Arguments:
            params (str, dict):
                This argument specifies what exception to expect (and 
                optionally how to check its message).

                If string: A string that should evaluate to an exception type.  
                This can also be ``"none"`` to specify that the returned 
                context manager should not expect any exception to be raised.

                If dict: The following keys are understood:

                - "type" (required): A string that should evaluate to an 
                  exception type.  The context manager will require that an 
                  exception of that type is raised.

                - "message" (optional): A string or list of strings that should 
                  appear in the error message.  Each string is interpreted as a 
                  regular expression, in the same manner as the *match* 
                  argument to `pytest.raises`.

                Note that everything is expected to be strings, because this 
                method is meant to help with parsing exception information from 
                a text file, e.g. in the NestedText_ format.

        Returns:
            A context manager that can be used to check if the kind of 
            exception specified by *params* was raised.

        Examples:
            Using a built-in exception (so no need to specify globals) and not 
            checking the error message::

                >>> p = {'type': 'ZeroDivisionError'}
                >>> with Namespace().error(p):
                ...    1/0

            Using a custom exception::

                >>> class MyError(Exception):
                ...     pass
                ...
                >>> with_err = Namespace(MyError=MyError)
                >>> p = {'type': 'MyError', 'message': r'\\d+'}
                >>> with with_err.error(p):
                ...    raise MyError('404')

        Details:
            The returned context manager is re-entrant, which makes it possible 
            to stack :deco:`parametrize_from_file` invocations that make use of 
            method (e.g. via the *schema* argument).
        """
        if params == 'none':
            return nullcontext()

        if isinstance(params, str):
            err_type = self.eval(params)
            err_messages = []
        else:
            err_type = self.eval(params['type'])
            err_messages = params.get('message', [])
            if not isinstance(err_messages, list):
                err_messages = [err_messages]

        # Normally I'd use `@contextmanager` to make a context manager like 
        # this, but generator-based context managers cannot be reused.  This is 
        # a problem for tests, because if a test using this context manager is 
        # parametrized, the same context manager instance will need to be 
        # reused multiple times.  The only way to support this is to implement 
        # the context manager from scratch.

        class ExpectError:

            def __repr__(self):
                return f'<{self.__class__.__name__} type={err_type!r} messages={err_messages!r}>'

            def __enter__(self):
                self.raises = pytest.raises(err_type)
                self.err = self.raises.__enter__()

            def __exit__(self, *args):
                if self.raises.__exit__(*args):
                    for msg in err_messages:
                        self.err.match(msg)
                    return True

        return ExpectError()

