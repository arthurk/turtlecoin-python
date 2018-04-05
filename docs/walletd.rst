.. _walletd:

Walletd
=======

This document shows examples for the `walletd` JSON-RPC API.

Before you start using the Python integration, make sure that you have
`walletd` running with the `rpc-password` argument set:

.. code-block:: bash

    ./walletd -w test.wallet -p my_wallet_password --local --rpc-password test

Once it's running make sure that the blockchain is synchronized. The console log will
show an info message when it's done:

.. code-block:: console

    Wallet loading is finished.

The python integration can now be used.

Usage
-----

For all available methods see the full :ref:`API documentation <walletd_api>`.

Let's start by instantiating the Walletd class and printing the wallet
address as well as the balance.

.. code-block:: python

    from turtlecoin import Walletd

    wallet = Wallet(password='test')
    wallet.get_address()
    'TRTLuxBjcKs5Ubbopcwc...'
    wallet.get_balance()
    {'availableBalance': 1000, 'lockedAmount': 0}

Internally all amounts are represented as integers. To get the correct amount
you have to divide it by 100. For convenience you can use the `format_amount`
helper from the utils package:

.. code-block:: python

    from turtlecoin.utils import format_amount

    balance = wallet.get_balance()
    format_amount(balance['availableBalance'])
    100.00

Let's create a second address and transfer some funds to it.
You can either multiply the value by 100 or use the `parse_amount`
utility to convert the amount of TRLT into the internal integer
representation:

.. code-block:: python

    sender_address = wallet.get_address()
    receiver_address = wallet.create_address()

    amount = parse_amount(100.00)
    transfers = [{'address': receiver_address, 'amount': amount}]
    tx_hash = wallet.send_transaction(transfers, change_address=sender_address)

    wallet.get_balance(sender_address)
    {'availableBalance': 0, 'lockedAmount': 0}
    wallet.get_balance(receiver_address)
    {'availableBalance': 1000, 'lockedAmount': 0}
