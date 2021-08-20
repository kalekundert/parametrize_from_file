***************
Getting started
***************

Rationale
=========
Parametrizing your tests—in other words, separating the test data from the test 
code—is frequently a good idea.  It makes it easier to add new test cases, 
while also making it easier to read and understand the test code.

|PFF| provides a convenient way to parametrize tests when using the popular 
pytest_ framework.  The central idea is to keep the parameters in their own 
files, separate from the test code.  This prevents long lists of parameters 
from dwarfing your test code, and often allows parameters to be specified more 
clearly and succinctly than would be possible in python.  

Installation
============
Install |PFF| using ``pip``:

.. code-block:: console

  $ pip install parametrize_from_file

- Requires python≥3.6
- Follows `semantic versioning`_.

Writing the parameters
======================
In this tutorial, we'll write some tests for a dot product function meant to 
work with a simple 2D vector class:

.. literalinclude:: getting_started/vector.py
   :caption: vector.py

We'll specify the parameters for the tests in their own file.  This file can be 
JSON_, YAML_, TOML_, or NestedText_.  We'll use YAML_ for this example, since 
it's simple and well-known, but I'll note that NestedText_ is generally a 
better choice for real tests (for the reasons discussed :doc:`here 
<python_snippets>`).

.. literalinclude:: getting_started/test_vector.yml
   :caption: test_vector.yml
   :language: yaml

Note that the parameters are indexed by test function (``test_dot`` in this 
case).  This allows parameters for multiple test functions to be specified in a 
single file.  The usual organization is to have one parameter file per test 
file, with both files having the same base name and containing the same set of 
tests.

Writing the tests
=================
Write the test function as if you were using `pytest.mark.parametrize ref`.  
The function should accept an argument for each parameter, and the name of the 
argument should match the name of the parameter in the file.  Decorate the test 
function directly with the :mod:`parametrize_from_file` module.  

.. literalinclude:: getting_started/test_vector.py
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
