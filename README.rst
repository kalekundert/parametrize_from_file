*********************
Parametrize From File
*********************

.. image:: https://img.shields.io/pypi/v/parametrize_from_file.svg
   :target: https://pypi.python.org/pypi/parametrize_from_file

.. image:: https://img.shields.io/pypi/pyversions/parametrize_from_file.svg
   :target: https://pypi.python.org/pypi/parametrize_from_file

.. image:: https://img.shields.io/readthedocs/parametrize_from_file.svg
   :target: https://parametrize-from-file.readthedocs.io/

.. image:: https://img.shields.io/github/actions/workflow/status/kalekundert/parametrize_from_file/test.yml?branch=master
   :target: https://github.com/kalekundert/parametrize_from_file/actions

.. image:: https://img.shields.io/coveralls/kalekundert/parametrize_from_file.svg
   :target: https://coveralls.io/github/kalekundert/parametrize_from_file?branch=master

.. image:: https://img.shields.io/github/last-commit/kalekundert/parametrize_from_file?logo=github
   :target: https://github.com/kalekundert/parametrize_from_file

Parametrize From File is a library for reading unit test parameters from config 
files.  It works with the pytest_ framework.  Below is the basic workflow that 
this package enables:

- Write test cases in a JSON_, YAML_, TOML_, or NestedText_ file:

  .. code-block:: yaml

    # test_camelot.yml
    test_str_find:
    - str: sir lancelot
      sub: lance
      loc: 4

    - str: sir robin
      sub: brave
      loc: -1

- Decorate the corresponding test functions with ``@parametrize_from_file``:

  .. code-block:: py

    # test_camelot.py
    import parametrize_from_file

    @parametrize_from_file
    def test_str_find(str, sub, loc):
        assert str.find(sub) == loc

- Run pytest_ as usual::

    ============================= test session starts ==============================
    platform linux -- Python 3.10.0, pytest-7.4.0, pluggy-1.2.0
    rootdir: /home/arthur/holy_grail
    collected 2 items
    
    test_camelot.py ..                                                       [100%]
    
    ============================== 2 passed in 0.09s ===============================

Refer to the `online documentation <https://parametrize-from-file.rtfd.io>`_ 
for more information.

.. _pytest: https://docs.pytest.org/en/stable/getting-started.html
.. _JSON: https://www.json.org/json-en.html
.. _YAML: https://yaml.org/
.. _TOML: https://toml.io/en/
.. _NestedText: https://nestedtext.org/en/latest/

