**********
Exceptions
**********

Testing functions that are expected to raise exceptions for some inputs is a 
very common task.  The usual approach is to write separate test functions for 
the valid and invalid inputs, but this adds boilerplate and often means 
duplicating the code that helps setup the test.  Instead, this tutorial will 
show an elegant way to use the same test function for all inputs.  The key is a 
`helper function <voluptuous.Namespace.error_or>` that:

- Produces a schema that accepts either an expected value or an expected error.
- When that schema is evaluated, creates a context manager that can be used to 
  check whether or not the expected exception was raised.

To give a concrete example, we'll extend the ``Vector`` class from the 
`getting_started` tutorial with a ``normalize()`` method, which should raise a 
``NullVectorError`` exception when called on a null vector:

.. literalinclude:: exceptions/vector.py
   :caption: vector.py

Each test case for this method specifies either an *expected* parameter or an 
*error* parameter.  The *expected* parameter is just a value, the same as all 
the other test parameters we've seen in these tutorials.  The *error* parameter 
is special, in that it should specify a kind of exception to expect.  There are 
a few ways to do this (see |NS_error| for details), but the simplest is to give 
a string that will evaluate to an exception type:

.. literalinclude:: exceptions/test_vector.nt
   :caption: test_vector.nt
   :language: nestedtext

To write the test function, we'll make use of `voluptuous.Namespace.error_or`.  
This function builds a schema that will accept either an implicit *error* 
parameter or whatever "expected" parameters are explicitly provided to it.  
Either way, the test function will receive arguments corresponding to the error 
*and* every "expected" parameter.  The error argument will be a context manager 
that will either check that the expected error was raised (if an error was 
specified) or do nothing (otherwise).  The "expected" arguments will be either 
be passed directly through to the test function (if no error was specified) or 
be replaced with `MagicMock <unittest.mock.MagicMock>` objects (otherwise).  
The purpose of replacing the "expected" arguments with `MagicMock 
<unittest.mock.MagicMock>` objects is to help avoid the intended exception from 
getting preempted by some other exception caused by an unspecified expected 
value.

.. note::

  Functions like `voluptuous.Namespace.error_or` are not currently provided for 
  any schema libraries except voluptuous_.  If you implement something similar 
  for another schema library, I'd be happy to accept a pull request.

This sounds complicated, but in practice it's not bad.  Hopefully the following 
example code will help make everything clear:

.. literalinclude:: exceptions/test_vector.py
   :caption: test_vector.py

A shortcoming of this example is that it does not show how to check that the 
exception has the expected error message.  For more information on that, 
consult: `voluptuous.Namespace.error_or`
