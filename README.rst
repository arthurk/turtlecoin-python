turtlecoin-python
=================

.. image:: https://img.shields.io/pypi/v/turtlecoin.svg
	:target: https://pypi.python.org/pypi/turtlecoin

.. image:: https://img.shields.io/pypi/pyversions/turtlecoin.svg
	:target: https://pypi.python.org/pypi/turtlecoin

.. image:: https://img.shields.io/pypi/l/turtlecoin.svg
	:target: https://pypi.python.org/pypi/turtlecoin

.. image:: https://readthedocs.org/projects/turtlecoin-python/badge/
    :target: http://turtlecoin-python.readthedocs.io/en/latest/

A Python wrapper for the TurtleCoin JSON-RPC API.

It integrates with `Walletd` and `TurtleCoind` and works with TurtleCoin 0.5.0.

Example
-------

.. code-block:: python

    wallet.get_addresses()
    'TRTLv1abcdef...'
    {'id': 0, 'jsonrpc': '2.0', 'result': {'addresses': ['TRTLv2R....']}}

    wallet.get_balance()
    {'id': 0, 'jsonrpc': '2.0', 'result': {'availableBalance': 50, 'lockedAmount': 0}}

    recipients = [{'address': 'TRTLv3abcd123...', 'amount': 50}]
    wallet.send_transaction(transfers=recipients)
    {'id': 0, 'jsonrpc': '2.0', 'result': {'transactionHash': 'ae57e...'}}

Installation
------------

You can install the latest version from PyPI:

.. code-block:: bash

    $ pip install turtlecoin

Documentation
-------------

The documentation is available at http://turtlecoin-python.readthedocs.io

Developer setup
---------------

Clone the repo and install the dependencies with ...pipenv:

.. code-block:: bash

    $ git clone ...
    $ cd turtlecoin-python
    $ pipenv install --dev

To generate the HTML documentation you need to have the turtlecoin module in
your PYTHONPATH. This is used to automatically generate the api docs.
Afterwards you can run the makefile target:

.. code-block:: bash

    $ pipenv run python setup.py develop
    $ pipenv run make html

The documentation on readthedocs is automatically updated on
each push to the master branch (via webhook).

To release a new version on PyPI, increment the version number
in `turtlecoin/__version__.py` and run:

.. code-block:: bash

    $ pipenv run python setup.py upload

This will also create a git tag with the version number.
