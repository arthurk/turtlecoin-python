.. _turtlecoind:

Turtlecoind
===========

This document shows how to use the `TurtleCoind` JSON-RPC API.

Running Turtlecoind
-------------------

Before you start using the Python integration, make sure that you are
running `TurtleCoind` with the `enable_blockexplorer` argument set:

.. code-block:: bash

    ./TurtleCoind --enable_blockexplorer

After starting it make sure the blockchain is synchronized.
This might take a while. The console log will show a message when it's done:

.. code-block:: console

    Successfully synchronized with the TurtleCoin Network

The python integration can now be used.

Usage
-----

For all available methods see the full :ref:`API documentation <turtlecoind_api>`.

To print the current block-height:

.. code-block:: python

    from turtlecoin import Turtlecoind

    turtle = TurtleCoind()
    turtle.getblockcount()['count']
    286373
