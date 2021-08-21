*******************
Optional parameters
*******************

.. note::

   This tutorial build on the concepts from the `python_snippets` tutorial.

Many tests have parameters that don't really need to be specified for every 
case, e.g. parameters with reasonable defaults.  Specifying such parameters 
over and over again is not only tedious, but also error-prone.  Fortunately, 
there are two good ways to avoid doing this, described below.

To expand on the vector example from the `getting_started` tutorial, let's 
consider testing a ``from_angle()`` function that initializes a vector from a 
given angle (relative to the x-axis).  This function will have two optional 
parameters:

- *unit*: specify whether the given angle is in radians or degrees.
- *magnitude*: set the length of the resulting vector

.. literalinclude:: optional_params/vector.py
   :caption: vector.py

Schema approach
===============
The *schema* argument to `parametrize_from_file` can be used to fill in 
unspecified parameters with default values.  This takes advantage of the fact 
that, although every set of parameters needs to have all the same keys, the 
schema is applied before this check is made.  So it's possible for the schema 
to fill in any missing keys.  The following example uses voluptuous_, but any 
schema library will have support for this feature.  First, the parameter file:

.. literalinclude:: optional_params/test_vector_schema.nt
   :caption: test_vector.nt
   :language: nestedtext

Note that *unit* and *magnitude* are only specified for one test each.  The 
following schema fills in the defaults:

.. literalinclude:: optional_params/test_vector_schema.py
   :caption: test_vector.py

Note that the test function uses degrees as the default unit, while the 
function itself uses radians.  This is both a good thing and a bad thing.  It's 
good that our tests will be robust against changes to the default unit.  But 
it's bad that we're not actually testing the default unit.  If we would like to 
test this default, we can either write another test specifically for that or 
use the dict/list approach described in the next section.

Dict/list approach
==================
For functions that take a lot of arguments, it's sometimes simpler to define 
one parameter that contains a variable number of arguments (e.g. akin to *args* 
or *kwargs*) than it is to explicitly specify default values for every optional 
parameter.  This approach is often combined with the schema approach described 
in the previous section, such that an empty container is assumed if the 
top-level parameter isn't specified:

.. literalinclude:: optional_params/test_vector_kwargs.nt
   :caption: test_vector.nt
   :language: nestedtext

One nice feature of |NS_eval| (see below) is that it recursively handles 
dictionaries and lists, which allows use to specify *kwargs* using either 
python or NestedText_ syntax.  Note that this requires us to quote the *unit* 
parameter in the NestedText_ file, though.

.. literalinclude:: optional_params/test_vector_kwargs.py
   :caption: test_vector.nt
