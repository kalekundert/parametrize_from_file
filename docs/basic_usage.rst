***********
Basic usage
***********

Installation
============
Install :mod:`parametrize_from_file` using ``pip``:

.. code-block:: console

  $ pip install parametrize_from_file

- Requires python≥3.6
- Follows `semantic versioning`_.

Writing the parameters
======================
In this tutorial, we'll write tests for a dot product function meant to work 
with a simple 2D vector class:

.. literalinclude:: examples/vector.py
   :caption: vector.py

We'll specify the parameters for the tests in their own file.  This file can be 
JSON_, YAML_, TOML_, or NestedText_.  I recommend NestedText_, because its 
simple and unambiguous syntax makes it easy to specify the kinds of values used 
in tests (which often look a lot like code).  The other formats tend to require 
lots of quoting or escaping for such values:

.. literalinclude:: examples/test_vector.nt
   :caption: test_vector.nt

Note that the parameters are indexed by test function (``test_dot`` in this 
case).  This allows parameters for multiple test functions to be specified in a 
single file.  The usual organization is to have one parameter file per test 
file, with both files having the same base name.

Writing the tests
=================
Write the test function as if you were using `pytest.mark.parametrize ref`.  
The function should accept an argument for each parameter, and the name of the 
argument should match the name of the parameter in the file.  Decorate the test 
function directly with the :mod:`parametrize_from_file` module.  

Note that in the parameter file shown above, the parameters are specified using 
python syntax.  This is a very common thing to do, since test inputs and 
outputs frequently need to be python objects.  We can easily convert these 
parameters to objects by using the *schema* argument as shown in the example 
below.  This schema specifies that `eval` should be called on all parameters 
before they are provided to the test function.  The helper lambda function is 
used to ensure that `eval` is called in the scope where *Vector* is defined.  
See the :doc:`api_reference` for a complete description 
of this argument.

.. literalinclude:: examples/test_vector.py
   :caption: test_vector.py

Running the tests
=================
Run the tests using pytest, in the same way you normally would.  Note that all 
four tests are run:

.. code-block:: console

  $ pytest test_vector.py
  ============================= test session starts ==============================
  platform linux -- Python 3.8.2, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
  rootdir: /home/kale/hacking/projects/parametrize_from_file, configfile: pyproject.toml
  plugins: forked-1.1.3, cov-2.8.1, xonsh-0.9.24, xdist-1.32.0, hypothesis-5.8.3, mock-2.0.0
  collected 4 items                                                              

  test_vector.py ....                                                      [100%]

  ============================== 4 passed in 0.15s ===============================

.. _`semantic versioning`: https://semver.org/
.. _JSON: https://www.json.org/json-en.html
.. _YAML: https://yaml.org/
.. _TOML: https://toml.io/en/
.. _NestedText: https://nestedtext.org/en/latest/
