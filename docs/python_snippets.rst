***************
Python snippets
***************

Very often, it is convenient to specify test parameters that are python 
objects.  There are two ways to do this: either with expressions that evaluate 
to the desired object, or with multi-line snippets that assign the desired 
object to a predetermined variable name.  Both cases are described below:

Expressions
===========
For a concrete example where it would make sense to parametrize a test with 
python expressions, let's revisit the dot product example from the 
`getting_started` tutorial:

.. literalinclude:: getting_started/vector.py
   :caption: vector.py

The *a* and *b* arguments to the ``dot()`` function are meant to be vector 
objects, so it makes sense to use python syntax when specifying these arguments 
in the parameter file.  This approach provides a lot of flexibility compared to 
*not* using python syntax (e.g. just specifying coordinates and constructing 
the actual ``Vector`` object in the test function, as we did in the 
`getting_started` tutorial):

- We can test subclasses, e.g. ``Vector3D(0, 0, 1)``.

- We can instantiate the vectors in different ways, e.g. ``Vector.null()`` or 
  ``Vector(1, 0) + Vector(0, 1)``.

- We can test invalid inputs, e.g. ``None``, and make sure the proper exception 
  is raised.  See `exceptions` for more information on this topic.

Below is the parameter file from the `getting_started` tutorial rewritten using 
python syntax.  Note that the file is also rewritten in the NestedText_ format.  
NestedText_ never requires any quoting or escaping, so I strongly recommend it 
for any tests with code-like syntax [#]_.  Alternative formats like YAML_ and 
TOML_ tend to require a lot of quoting and/or escaping for values that look 
like code [#]_.

.. literalinclude:: python_snippets/eval/test_vector.nt
   :caption: test_vector.nt
   :language: nestedtext

The simplest way to load a python object from a string is to use the built-in 
`python:eval` function.  But there is an additional wrinkle, which is that we 
want the name ``Vector`` to be available when evaluating each expression.  More 
generally, we will want a lot names from the package being tested to be 
available to the expressions we write.  This is tedious to do with 
`python:eval`, so |PFF| includes an |NS| helper class to make this easier:

.. literalinclude:: python_snippets/eval/test_vector.py
   :caption: test_vector.py

Multi-line snippets
===================
For an example of when it would be useful to specify multiple lines of python 
code as a test parameter, consider a function that is meant to instantiate a 
vector from several different kinds of input:

.. literalinclude:: python_snippets/exec/vector.py
   :caption: vector.py
   :start-after: # start here

.. note:: 

   This function should raise an exception in the case where the given object 
   can't be converted to a vector.  Testing exceptions is covered in the 
   `exceptions` tutorial, though, so for now we'll ignore that detail.

In order to thoroughly test this function, we'll need to instantiate an object 
with ``x`` and ``y`` attributes.  This could be done with an expression, but 
it's more clear to define and instantiate a custom class:

.. literalinclude:: python_snippets/exec/test_vector.nt
   :caption: test_vector.nt
   :language: nestedtext

Beyond this simple example, multi-line snippets are also very useful when 
testing classes that are meant to be subclassed and objects that need several 
steps of initialization.

As in the previous section, we can use the |NS| helper class to easily execute 
these snippets in a context where the name ``Vector`` is defined.  Note that 
|NS_exec| returns a dictionary of all the variables defined while executing the 
snippet, and we are specifically interested in the value of the ``obj`` 
variable:

.. literalinclude:: python_snippets/exec/test_vector.py
   :caption: test_vector.py

.. _schema-be-careful:

Schema argument: Be careful!
============================
Be careful when using |NS_eval| and especially |NS_exec| with the *schema* 
argument to `parametrize_from_file`.  This can be convenient, but it's 
important to be cognizant of the fact that schema are evaluated during test 
collection (i.e.  outside of the tests themselves).  This has a couple 
consequences:

- Any errors that occur when evaluating parameters will not be handled very 
  gracefully.  In particular, no tests will run until all errors are fixed (and 
  it can be hard to find errors without being able to run any tests).

- Even if you only ask to run a single test, the parameters for every test will 
  have to be evaluated.  This can take a substantial amount of time if you've 
  written snippets that do a lot of work (more likely with |NS_exec| than 
  |NS_eval|, but possible with both).

My general recommendation is to only use |NS_eval| and |NS_exec| with the 
*schema* argument if the snippets in question don't involve any code from the 
package being tested (e.g. built-ins or third-party packages only).  For 
example, here is a version of ``test_dot()`` that uses a schema:

.. literalinclude:: python_snippets/schema/test_vector.py
   :caption: test_vector.py

A few things to note about this example:

- This also is a good example of how the |NS| class can be used to control 
  which names are available when evaluating expressions.  Here we make two 
  namespaces: one for just built-in names (including all the names from the 
  math module), and another for our vector package.  This distinction allows us 
  to avoid the possibility of evaluating vector code from the schema.

- This example uses `voluptuous.Namespace` instead of just |NS|.  These two 
  classes are largely equivalent, but `voluptuous.Namespace` includes some 
  voluptuous_-specific tweaks, e.g. raising the kind of exceptions expected by 
  voluptuous_ if `python:eval` or `python:exec` fail.  Currently there are no 
  custom |NS| classes for any other schema libraries, but if you write one, I'd 
  be happy to accept a pull request.

- The ``Vector`` expressions used in these examples are actually a bit of a 
  grey area, because they're simple enough that (i) they're unlikely to break 
  in confusing ways and (ii) they won't significantly impact runtime.  If I 
  were writing these tests for a real project, I would probably be ok with 
  having the schema evaluate such expressions.  Regardless, the above example 
  shows the "right" way to do things.  Use your best judgment.


.. [#] In fact, I recommend NestedText_ for every kind of test, but the 
   advantage is most clear with parameters that involve a lot of syntax-like 
   characters.

.. [#] For example, consider a test parameter that can either be a string or a 
   callable.  `pandas.DataFrame.aggregate` has *func* argument that works like 
   this: a string can be used to identify one of a handful of standard 
   algorithms, while a callable can be used to provide a custom algorithm:
   
   In NestedText_:

   .. code-block:: nestedtext

       test_agg:
         -
           func: 'string'
         -
           func: lambda x: x

   In YAML_:

   .. code-block:: yaml

       test_agg:
         - func: "'string'"
         - func: "lambda x: x"

   In TOML_:

   .. code-block:: toml

       [[test_agg]]
       func = "'string'"

       [[test_agg]]
       func = "lambda x: x"

   Note that YAML_ and TOML_ both have to double-quote the string, because the 
   first set of quotes are interpreted as part of the file format.  YAML_ 
   additionally needs to quote the lambda function, because it looks too much 
   like a dictionary item.

