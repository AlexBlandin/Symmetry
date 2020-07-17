# Symmetry

Symmetry Breaking Experiments

## Requirements

- [Python 3.6+](https://www.python.org) (but really you should be using 3.7 or 3.8)
  - [pip 20.0.1+](https://pypi.org/project/pip/) is standard fare
  - [wheel 0.34.0+](https://pypi.org/project/wheel/) is standard fare
  - [setuptools 48.0.0+](https://pypi.org/project/setuptools/) is standard fare
  - [requests 2.23.0+](https://pypi.org/project/requests/) is needed for `poetry install`
- [humanize 2.0.0+](https://pypi.org/project/humanize/)
- [psutil 5.0.0+](https://pypi.org/project/psutil/)
- [tabulate 0.8.1+](https://pypi.org/project/tabulate/)
- [tqdm 4.30.0+](https://pypi.org/project/tqdm/)
  - [colorama 0.4.3+](https://pypi.org/project/colorama/) on Windows

Or either of:
- [poetry 0.12+](https://github.com/python-poetry/poetry)
- [upm 1.0.0+](https://github.com/replit/upm) includes `poetry`

To install requirements:
- `pip install humanize psutil tabulate tqdm colorama`
  - `pip install --update pip wheel setuptools requests` may be necessary
- `poetry install`
- `upm install`

## Running

`$ python3 sym.py` is all that's needed. Supports [PyPy3.6 v7.3.1+](https://www.pypy.org/).
