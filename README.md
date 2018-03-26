turtlecoin-python
=================

![PyPI](https://img.shields.io/pypi/v/turtlecoin.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/turtlecoin.svg)
![PyPI - License](https://img.shields.io/pypi/l/turtlecoin.svg)
[![Documentation Status](https://readthedocs.org/projects/turtlecoin-python/badge/?version=latest)](http://turtlecoin-python.readthedocs.io/en/latest/?badge=latest)

A Python wrapper for the TurtleCoin JSON-RPC API.

It integrates with `Walletd` and `TurtleCoind` and works with TurtleCoin 0.3.x.

TODO:

* create_address: creating address from a spend key doesnt work

Example
-------

```python
wallet.get_address()
'TRTLv1abcdef...'

wallet.get_balance()
{'availableBalance': 50, 'lockedAmount': 0}

recipients = [{'address': 'TRTLv3abcd123...', 'amount': 50}]
wallet.send_transaction(transfers=recipients)
'dc1221181e574...'
```

Installation
------------

You can install the latest version from PyPI:

```
pip install turtlecoin
```

Documentation
-------------

The documentation is available at http://turtlecoin-python.readthedocs.io

Developer setup
---------------

Install dependencies with pipenv:

```
git clone ...
cd turtlecoin-python
pipenv install --dev
```

To generate the documentation run:

```
pipenv run make html
```

To release a new version on PyPI, increment the version number
in `turtlecoin/__version__.py` and run:

```
pipenv run python setup.py upload
```

This will also create a git tag with the version number.
The documentation on readthedocs is automatically updated (via webhook).
