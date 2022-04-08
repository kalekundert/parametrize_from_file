***************
Temporary files
***************

.. note::

  This tutorial makes use of concepts from the `python_snippets` and 
  `exceptions` tutorials, although neither are central to the main points.

In order to test functions that interact with the file system, it is often 
necessary to construct a handful of files or directories for each test.  Such 
tests typically use the :std:fixture:`tmp_path` fixture provided by pytest to 
create a unique temporary directory for each test.  However, that directory 
still needs to be filled in with the files relevant to the test.  For that, 
*Parametrize From File* (in conjunction with the |tmp_files| plugin) is a 
powerful tool.

To give an example, let's return to the ``Vector`` class from the 
`getting_started` tutorial and add a function to parse a list ``Vector`` 
objects from a text file.  The format is straight-forward: each line should 
have exactly two space-separated numbers which will be interpreted as the x- 
and y-coordinates of a vector:

.. literalinclude:: temp_files/vector.py
   :caption: vector.py

Below are five test cases, three for files that should load successfully and 
two for files that shouldn't.  The *tmp_files* parameters specify the files to 
create for each test case, as mappings of file names to file contents.  Refer 
to the |tmp_files| documentation for more information on how to specify this 
parameter.

.. literalinclude:: temp_files/test_vector.nt
   :caption: test_vector.nt

There are a few things to note about the test function itself:

- The ``indirect=['tmp_files']`` argument is critical.  This is how the 
  |tmp_files| fixture knows to create the files specified by the *tmp_files* 
  parameters.
  
- All of the tests use the same hard-coded file name.  If we had wanted the 
  file name to be part of the test (e.g. to parse differently based on the file 
  extension, to test the "file not found" error, etc.), we would've added 
  another parameter specifying which file to load.

- The advantage of using *Parametrize From File* in conjunction with 
  |tmp_files|, as opposed to just using |tmp_files| by itself, is readability.  
  The python syntax for specifying parameters becomes hard to read when lots of 
  multi-line strings are used, and files tend to have multiple lines.  File 
  formats like YAML_, TOML_, and NestedText_ do not have this problem.
  
- This test also checks that the appropriate exceptions are raised for 
  malformed files.  This isn't directly relevant to the task of using temporary 
  files in tests, but it's an important part of testing a parser.

.. literalinclude:: temp_files/test_vector.py
   :caption: test_vector.py

.. |tmp_files| replace:: `tmp_files <pytest_tmp_files.tmp_files>`
