# Symmetry Breaking Experiments

## Requirements

- [Python 3.6+](https://www.python.org)
  - [pip 20.0.1+](https://pypi.org/project/pip/) is standard fare
  - [wheel 0.34.0+](https://pypi.org/project/wheel/) is standard fare
  - [setuptools 48.0.0+](https://pypi.org/project/setuptools/) is standard fare
- [humanize 2.0.0+](https://pypi.org/project/humanize) for nice memory readouts
- [psutil 5.0.0+](https://pypi.org/project/psutil) for nice OOM preemption
- [tabulate 0.8.1+](https://pypi.org/project/tabulate/) for nice output
- [tqdm 4.30.0+](https://pypi.org/project/tqdm/) for a nice progress bar

Or, you can use a package manager such as [Poetry](https://github.com/python-poetry/poetry):
1. `$ pip install poetry`
2. `$ poetry install`

## Running

`$ python3 sym.py [midrc|rings1|rings2|rings3]`, i.e.
- `$ python3 sym.py midrc`
- `$ python3 sym.py rings1`

Supports [PyPy3.6 v7.3.1+](https://www.pypy.org/).
