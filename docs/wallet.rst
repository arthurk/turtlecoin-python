Wallet
======

The ``Wallet`` class integrates with the Walletd JSON-RPC API.

In order to connect to the daemon, you need to run `Walletd` with `--rpc-password` set::

    ./walletd -w test.wallet -p any_password_you_want --local --rpc-password test

Make sure that the blockchain is synchronized. The console log will show an info message::

    SYNCHRONIZED OK
    You are now synchronized with the network. You may now start simplewallet.

Instantiation
-------------

.. code-block:: python

    from turtlecoin import Wallet

    wallet = Wallet(password='test')
