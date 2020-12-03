*********************
Parametrize From File
*********************

.. image:: https://img.shields.io/pypi/v/parametrize_from_file.svg
   :target: https://pypi.python.org/pypi/parametrize_from_file

.. image:: https://img.shields.io/pypi/pyversions/parametrize_from_file.svg
   :target: https://pypi.python.org/pypi/parametrize_from_file

.. image:: https://img.shields.io/readthedocs/parametrize_from_file.svg
   :target: https://parametrize_from_file.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/github/workflow/status/kalekundert/parametrize_from_file/Test%20and%20release/master
   :target: https://github.com/kalekundert/parametrize_from_file/actions

.. image:: https://img.shields.io/coveralls/kalekundert/parametrize_from_file.svg
   :target: https://coveralls.io/github/kalekundert/parametrize_from_file?branch=master

Parametrizing your tests---in other words, separating the test data from the 
test code---is frequently a good idea.  It makes it easier to add new test 
cases, while also making it easier to read and understand the test code.

``parametrize_from_file`` provides a convenient way to parametrize tests when 
using the popular pytest_ framework.  The central idea is to keep the 
parameters in their own files, separate from the test code.  This prevents long 
lists of parameters from dwarfing your test code, and often allows parameters 
to be specified more clearly and succinctly than would be possible in python.  
Below is the basic workflow that this package enables:

- Write test cases in a JSON_, YAML_, TOML_, or NestedText_ file::

    # test_misc.yml
    test_addition:
      - a: 1
        b: 2
        c: 3

- Decorate the corresponding test functions with `parametrize_from_file`::

    # test_misc.py
    import parametrize_from_file

    @parametrize_from_file
    def test_addition(a, b, c):
        assert a + b == c

- Run pytest_ as usual::

    $ pytest

.. _pytest: https://docs.pytest.org/en/stable/getting-started.html
.. _JSON: https://www.json.org/json-en.html
.. _YAML: https://yaml.org/
.. _TOML: https://toml.io/en/
.. _NestedText: https://nestedtext.org/en/latest/

