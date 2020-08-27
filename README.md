# Symmetry Breaking Experiments

## Requirements

- [Python 3.6+](https://www.python.org)
  - [pip 20.0.1+](https://pypi.org/project/pip/) is standard fare
  - [wheel 0.34.0+](https://pypi.org/project/wheel/) is standard fare
  - [setuptools 48.0.0+](https://pypi.org/project/setuptools/) is standard fare
- [tabulate 0.8.1+](https://pypi.org/project/tabulate/) for nice output

Or, you can use a package manager such as [Poetry](https://github.com/python-poetry/poetry):
1. `$ pip install poetry`
2. `$ poetry install`

## Running

`$ python3 sym.py` is all you need to run it. Supports [PyPy3.6 v7.3.1+](https://www.pypy.org/).

## Verify

`$ python3 verify.py` will check `$ python3 sym.py`'s output for consistency and sanity.
