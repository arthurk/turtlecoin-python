turtlecoin-python
=================

.. image:: https://img.shields.io/pypi/v/turtlecoin.svg
	:target: https://pypi.python.org/pypi/turtlecoin

.. image:: https://img.shields.io/pypi/pyversions/turtlecoin.svg
	:target: https://pypi.python.org/pypi/turtlecoin

.. image:: https://img.shields.io/pypi/l/turtlecoin.svg
	:target: https://pypi.python.org/pypi/turtlecoin

turtlecoin-python is a Python wrapper for the TurtleCoin JSON-RPC API.
It integrates with :ref:`walletd` and :ref:`turtlecoind`.

Source Code
-----------

You can find the source code at GitHub: https://github.com/arthurk/turtlecoin-python

Requirements
------------

- Python 3.6
- `TurtleCoin 0.5.0 <https://github.com/turtlecoin/turtlecoin/releases/tag/v0.5.0>`_

Installation
------------

You can install the latest version with pip:

.. code-block:: bash

    $ pip install turtlecoin

Contents
--------

.. toctree::
   :maxdepth: 2

   walletd
   Turtlecoind

The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api/wallet
   api/daemon

Development
-----------

If you plan to work on the turtlecoin-python itself, it is useful to have
DEBUG logging enabled. You can do this with the following code snippet:

.. code-block:: python

    import logging

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

Enabling this will let you see more detailed data for the request that is
being sent to the JSON-RPC interface::

    2018-04-05 16:20:09,193 DEBUG    {
        "jsonrpc": "2.0",
        "method": "getlastblockheader",
        "params": {},
        "password": ""
    }
    2018-04-05 16:20:09,204 DEBUG    Starting new HTTP connection (1): 127.0.0.1
    2018-04-05 16:20:09,206 DEBUG    http://127.0.0.1:11898 "POST /json_rpc HTTP/1.1" 200 406
