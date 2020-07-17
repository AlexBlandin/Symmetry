# Symmetry Breaking Experiments

## Requirements

- [Python 3.6+](https://www.python.org) (but really you should be using 3.7 or 3.8)
  - [pip 20.0.1+](https://pypi.org/project/pip/) is standard fare
  - [wheel 0.34.0+](https://pypi.org/project/wheel/) is standard fare
  - [setuptools 48.0.0+](https://pypi.org/project/setuptools/) is standard fare
  - [requests 2.18+](https://pypi.org/project/requests/) required for `poetry install`
- [humanize 2.0.0+](https://pypi.org/project/humanize/)
- [psutil 5.0.0+](https://pypi.org/project/psutil/)
- [tabulate 0.8.1+](https://pypi.org/project/tabulate/)
- [tqdm 4.30.0+](https://pypi.org/project/tqdm/)
  - [colorama 0.4.3+](https://pypi.org/project/colorama/) on Windows

Or a package manager, such as either [Poetry 0.12+](https://github.com/python-poetry/poetry) (which requires [requests 2.18+](https://pypi.org/project/requests/))

To install requirements:
- `pip install humanize psutil tabulate tqdm colorama`
  - `pip install --update pip wheel setuptools requests` may be necessary
- `poetry install`

## Running

`$ python3 sym.py` is all that's needed. Supports [PyPy3.6 v7.3.1+](https://www.pypy.org/).
