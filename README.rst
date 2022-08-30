fntlib
======

**fntlib** is a Python library to interact with bitmap font (.fnt) files. It offers a simple modern Pythonic API and an intuitive workflow with an object oriented design.

Author
----
Jaan#2897

Usage
----
First, you should load your .fnt file by using `fntlib.load` or `fntlib.loads`::

  with open(path_to_file, 'rb') as f: # the file should be in bytes!
      fnt = fntlib.load(f) # or fnt = fntlib.loads(f.read())

Next, feel free to edit whatever property you want :)

While writing and documenting this module, i've been using `the Angelcode's documentation <https://www.angelcode.com/products/bmfont/doc/file_format.html>`_ of the .fnt format.

In VS Code, you can press F12 with any fntlib's function and it will bring you to its definition and the definition of the classes parameters.

Finally, after all your edits, you will need to dump the .fnt to some location::

  with open(path_to_output_file, 'wb') as f: # # the file should be in bytes!
      fntlib.dump(fnt, f) # or fp.write(fntlib.dumps(fnt))
      
If you still have questions, text me in my discord (Jaan#2897) or check the `tests/example/test_main.py` file.
