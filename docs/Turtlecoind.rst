Turtlecoind
===========

This document shows examples for the TurtleCoind JSON-RPC API.

Running Turtlecoind
-------------------

Before you start using the Python integration, make sure that you have
`TurtleCoind` running with the `--enable_blockexplorer` argument set::

    ./TurtleCoind --enable_blockexplorer

Once it's running make sure that the blockchain is synchronized.
The console log will show an info message when it's done::

    SYNCHRONIZED OK
    You are now synchronized with the network. You may now start simplewallet.

Now you're ready to use the Python integration.

Usage
-----

For all available methods see the `API documentation`.

Here we instanciate the Turtlecoind class and print
the current blockchain height.

.. code-block:: python

    from turtlecoin import Turtlecoind

    turtle = TurtleCoind()
    turtle.getblockcount()['count']
    286373
