Quickstart
==========

Begin by connecting to the walletd rpc interface and showing
the available public addresses:

Each response has the following format: `{'id': 0, 'jsonrpc': '2.0', 'result': ...}`.
In all examples below only the `result` is included.

.. code-block:: python

    from turtlecoin import Wallet

    wallet = Wallet(password='test')

    wallet.get_addresses()
    ['TRTLuxqgEUr13cw6dWKEJnNHRWk8SgbpgfERJUX4WDys5xACTUu6zTZBR32BFi8TavSNei6cU9ym6DPECaTrqQaaaFRgF3xKE73']


Now let's check the available balance:

 .. note::

    If you don't have any TRTL available make sure to visit the Faucet at https://faucet.trtl.me. You can enter your public address (from the example above) and it will send you 1 TRTL.

.. code-block:: python

    # this is the balance for all the addresses
    wallet.get_balance()
    {'availableBalance': 1000, 'lockedAmount': 0}

    # if you want the balance for a specific address, you can pass
    # the wallet address
    address = wallet.get_addresses()[0]
    wallet.get_balance(address=address)
    {'availableBalance': 1000, 'lockedAmount': 0}

Creating a transaction
----------------------

Let's create one more address and transfer TRLT between them.

.. code-block:: python

    sender = wallet.get_addresses()[0]
    receiver = wallet.create_address()

    print(receiver)
    'TRTLv3bEJu62XFy21JhsbUMLcQN72ooxvJGvPzfgG4kFgE78cbSQKSPBR32BFi8TavSNei6cU9ym6DPECaTrqQaaaFRgF4TV2tG'

    # specify the address and the amount which to send
    # here we send 0.5 TRLT
    recipients = [{'address': receiver, 'amount': 50}]

    # if a wallet has multiple addresses, a change address needs to be set
    tx_hash = wallet.send_transaction(transfers=recipients, change_address=sender)
    print(tx_hash)
    '61941df8828107a09f449597adf82d9daaf5f9957577aabe02c45f89cd34f9bd'

.. note::

    If you prefer a Web interface you can visit https://blocks.turtle.link and enter your tx_hash to see more information.

Now, let's get more information about our transaction:


.. code-block:: python

    wallet.get_transaction(tx_hash)

    {'amount': -10,
     'blockIndex': 286304,
     'extra': '01dc6f909744949f7e123801fe5f5673999bd3a0165d1c2d1c29154beb176a90c3',
     'fee': 10,
     'isBase': False,
     'paymentId': '',
     'state': 0,
     'timestamp': 1521729349,
     'transactionHash': '61941df8828107a09f449597adf82d9daaf5f9957577aabe02c45f89cd34f9bd',
     'transfers': [{'address': 'TRTLv2PAogjQ1jhLMooJZPDahnXj6fhNggNsrntRAdXgUX1SLNvCQwHBR32BFi8TavSNei6cU9ym6DPECaTrqQaaaFRgF3nGGBR',
                    'amount': 50,
                    'type': 0},
                   {'address': 'TRTLuxqgEUr13cw6dWKEJnNHRWk8SgbpgfERJUX4WDys5xACTUu6zTZBR32BFi8TavSNei6cU9ym6DPECaTrqQaaaFRgF3xKE73',
                    'amount': 840,
                    'type': 2},
                   {'address': 'TRTLuxqgEUr13cw6dWKEJnNHRWk8SgbpgfERJUX4WDys5xACTUu6zTZBR32BFi8TavSNei6cU9ym6DPECaTrqQaaaFRgF3xKE73',
                    'amount': -900,
                    'type': 0}],
     'unlockTime': 0}

    # Check the balance for the second address
    # It should have received the money (after the block has been processed, which might take a few seconds)
    print(wallet.get_balance(receiver))
    {'availableBalance': 50, 'lockedAmount': 0}


Delayed Transactions
--------------------

You can create delayed transactions too.

.. code-block:: python

    tx_hash = wallet.create_delayed_transaction(
        anonymity=3,
        transfers=[
            {
                'address': 'TRTL...',
                'amount': 50
            }
        ]
    )

    # List all delayed transactions
    wallet.get_delayed_transaction_hashes()
    ['bfcc4735a975f0ac0c27806b7abf9107adbd7a8a0c7c8ea91ca363eacda7f79x']

    # Send delayed transaction
    wallet.send_delayed_transaction(tx_hash)
