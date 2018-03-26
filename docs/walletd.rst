Walletd
=======

This document shows a few examples for the Walletd JSON-RPC API,
for the full API documentation head over to `xxx`.

Before you start using the Python integration, make sure that you have
`walletd` running with the `--rpc-password` argument set::

    ./walletd -w test.wallet -p my_wallet_password --local --rpc-password test

Once it's running make sure that the blockchain is synchronized. The console log will
show an info message when it's done::

    SYNCHRONIZED OK
    You are now synchronized with the network. You may now start simplewallet.

Now you're ready to use the Python integration.

Usage
-----

Let's start by instanciating the Walletd class, and printing
the wallet address and the balance.

.. code-block:: python

    from turtlecoin import Walletd

    wallet = Wallet(password='test')
    wallet.get_address()
    'xxx'
    wallet.get_balance()
    '{}'

Let's create a second address and transfer some funds between those
two addresses:

.. code-block:: python

    sender_address = wallet.get_address()
    receiver_address = wallet.create_address()

    transfers = [{'address': receiver_address, 'amount': 500}]
    tx_hash = wallet.send_transaction(transfers, change_address=sender_address)

    wallet.get_balance(sender_address)
    '{...}'
    wallet.get_balance(receiver_address)
    '{...}'
