start ../venv/Scripts/activate
del ./fntlib.rst
sphinx-apidoc -o . ../fntlib
.\make html