#!/usr/bin/env python3

from .namespace import Namespace as BaseNamespace
from voluptuous import Schema, Optional, Invalid, Or, All
from unittest.mock import MagicMock
from tidyexc import only_raise

class Namespace(BaseNamespace):
    """
    A variant of the |NS| class, with tweaks to work better with voluptuous_.
    """

    @only_raise(Invalid)
    def eval(self, *src, **kwargs):
        """
        |NS_eval|, with tweaks to work better with voluptuous_.

        Specifically, this function is guaranteed to raise `voluptuous.Invalid 
        <voluptuous>`_ if for any reason the given expression(s) can not be 
        successfully evaluated.  This ensures that voluptuous_ will be able to 
        produce good error messages.
        """
        return super().eval(*src, **kwargs)

    @only_raise(Invalid)
    def exec(self, src):
        """
        |NS_exec|, with tweaks to work better with voluptuous_.

        See `eval` for details.
        """
        return super().exec(src)

    def exec_and_lookup(self, key):
        """
        |NS_exec_lookup|, with tweaks to work better with voluptuous_.

        See `eval` for details.
        """
        f = super().exec_and_lookup(key)
        return only_raise(Invalid)(f)

    @only_raise(Invalid)
    def error(self, params):
        """
        |NS_error|, with tweaks to work better with voluptuous_.

        See `eval` for details.
        """
        return super().error(params)

    def error_or(self, expected):
        """\
        Build a schema that will expect to be given either an error or the 
        specified set of expected values.

        Arguments:
            expected (dict):
                Any test parameters that must be specified when an error is 
                *not* expected.  This dictionary has can be almost anything 
                that you would pass to `voluptuous.Schema <voluptuous>`_, 
                except that the keys must be either strings or 
                `voluptuous.Optional <voluptuous>`_.

        Returns:
            dict:
                A voluptuous schema that can accept either a single parameter 
                named *error*, or whatever parameters are specified by the 
                *expected* argument.  When this schema is evaluated, the 
                results will depend on which parameter(s) are given:

                If the *error* parameter is given, it will be processed by 
                |NS_error|.  That means: (i) it should match the format 
                expected by that method and (ii) it will be converted into a 
                context manager that can be used to detect whether the expected 
                exception was in fact raised.  All of the keys in the 
                *expected* schema passed to this function will also be present 
                in the resulting output, and will be set to |MagicMock| objects.  
                This ensures that any comparisons involving those keys will 
                succeed, to help prevent the expected exception from being 
                preempted by some missing value.

                If the *error* parameter is not given, the resulting output 
                will contain an *error* key set to a no-op context manager.  
                All of the keys in the *expected* schema will be evaluated as 
                usual.

        Example:
            This example is somewhat contrived, but it shows how to easily test a 
            function that raises a custom exception for certain inputs.
            
               >>> from voluptuous import Schema
               >>> from parametrize_from_file.voluptuous import Namespace

               >>> class DontGreet(Exception):
               ...     pass
               ...
               >>> def greet(name):
               ...     if name == 'Bob':
               ...         raise DontGreet(name)
               ...     return f"Hello, {name}!"
               ...
               >>> with_greet = Namespace(globals())
               >>> schema = Schema({
               ...    'given': str,
               ...    **with_greet.error_or({
               ...        'expected': str,
               ...    }),
               ... })
            
               >>> p1 = schema({
               ...         'given': 'Alice',
               ...         'expected': 'Hello, Alice!',
               ... })
               >>> with p1['error']:
               ...    assert greet(p1['given']) == p1['expected']
            
               >>> p2 = schema({
               ...         'given': 'Bob',
               ...         'error': {
               ...             'type': 'DontGreet',
               ...             'message': 'Bob',
               ...         },
               ... })
               >>> with p2['error']:
               ...    assert greet(p2['given']) == p2['expected']
            
            Note that the with block is the exact same for both assertions, even 
            though one tests for an error and the other doesn't.  This is what 
            makes `error_or()` useful for writing parametrized tests.
        """

        # With the API I'm using (accept a dictionary, return a dictionary), 
        # it's not actually possible to validate that only an error or the 
        # expected values are passed.  To do so requires some validator that 
        # runs on the whole data structure, which would have to be setup like 
        # so:
        #
        #     schema = Schema(
        #             All(
        #                 ...,
        #                 ns.error_or({
        #                     ...
        #                 }),
        #             )
        #     )
        #
        # I could simplify this a bit by wrapping `Schema`:
        #
        #     schema = ns.Schema({
        #                 ...,
        #             },
        #             error_or={
        #             },
        #     )
        #
        # Another problem with the current API is that optional expected keys 
        # need to be handled specially.  All of the expected keys need to be 
        # made optional, but I don't want to override the default value for any 
        # already-optional keys, because that will affect how they behave in 
        # non-error tests.
        # 
        # Despite all that, I still like this API.  The alternatives are too 
        # complex.  I think the best way to think about `error_or()` is that 
        # it's an intuitive shortcut for common use cases.  The user can always 
        # build their own schemas using `error()` if they need something more 
        # complicated.

        schema = {
                Optional('error', default='none'): self.error,
        }

        def check(schema):
            # This function basically just reimplements `Or`, but with a better 
            # error message.  The error message for `Or` is confusing because it 
            # only mentions the first option and not the second.  That's especially 
            # bad in this case, where the first option is basically an internal 
            # implementation detail.  This function changes the error message so 
            # that only the second option is mentioned, which is the least 
            # confusing in this case.
            # 
            # It's worth noting that the real problem is that voluptuous checks 
            # default values.  I can't imagine a case where this is actually 
            # useful. I might think about making a PR for that.

            def do_check(x):
                if isinstance(x, MagicMock):
                    return x
                return Schema(schema)(x)

            return do_check

        for k, v in expected.items():
            if k == 'error':
                raise ValueError("the key 'error' is reserved for use by error_or()")
            elif isinstance(k, str):
                schema[Optional(k, default=MagicMock)] = check(v)
            elif isinstance(k, Optional):
                schema[k] = v
            else:
                raise TypeError("'error_or()' only supports the following key types: str, voluptuous.Optional")

        return schema

