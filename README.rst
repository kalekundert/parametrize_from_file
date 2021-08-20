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

.. image:: https://img.shields.io/github/last-commit/kalekundert/parametrize_from_file?logo=github
   :target: https://github.com/kalekundert/parametrize_from_file

Parametrize From File is a library for reading unit test parameters from config 
files.  It works with the pytest_ framework.  Below is the basic workflow that 
this package enables:

- Write test cases in a JSON_, YAML_, TOML_, or NestedText_ file::

    # test_misc.yml
    test_addition:
      - a: 1
        b: 2
        c: 3

      - a: 2
        b: 4
        c: 6

- Decorate the corresponding test functions with ``@parametrize_from_file``::

    # test_misc.py
    import parametrize_from_file

    @parametrize_from_file
    def test_addition(a, b, c):
        assert a + b == c

- Run pytest_ as usual::

    $ pytest
    ============================= test session starts ==============================
    platform linux -- Python 3.8.2, pytest-6.2.4, py-1.9.0, pluggy-0.13.1
    rootdir: /home/kale/hacking/projects/parametrize_from_file, configfile: pyproject.toml
    plugins: forked-1.1.3, anyio-3.1.0, xonsh-0.9.27, typeguard-2.12.1, cov-2.8.1, xdist-1.32.0, hypothesis-5.8.3, mock-2.0.0
    collected 1 item                                                               

    test_misc.py ..                                                          [100%]

    ============================== 1 passed in 0.12s ===============================

Refer to the `online documentation <https://parametrize-from-file.rtfd.io>`_ 
for more information.

.. _pytest: https://docs.pytest.org/en/stable/getting-started.html
.. _JSON: https://www.json.org/json-en.html
.. _YAML: https://yaml.org/
.. _TOML: https://toml.io/en/
.. _NestedText: https://nestedtext.org/en/latest/

