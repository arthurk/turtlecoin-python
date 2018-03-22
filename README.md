turtlecoin-python
=================

![PyPI](https://img.shields.io/pypi/v/turtlecoin.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/turtlecoin.svg)
![PyPI - License](https://img.shields.io/pypi/l/turtlecoin.svg)
[![Documentation Status](https://readthedocs.org/projects/turtlecoin-python/badge/?version=latest)](http://turtlecoin-python.readthedocs.io/en/latest/?badge=latest)

A Python wrapper for the TurtleCoin JSON-RPC API.

**In development**

TODO:

* create_address: creating address from a spend key doesnt work

Installation
------------
You can install the latest version from PyPI:

Requires Python 3.6

```
pip install turtlecoin
```

Documentation
-------------

The documentation is available at http://turtlecoin-python.readthedocs.io

Note
----

You need to have walletd running with rpc enabled:

```
# generate a test wallet
$ ./walletd -w test.wallet -p any_password_you_want -g

# launch walletd with test wallet
$ ./walletd -w test.wallet -p any_password_you_want --local --rpc-password test
```

Example
----------

A short example which shows how to transfer funds between two addresses:

```
# this is the address that was created when the wallet was generated
sender = wallet.get_addresses()[0]

# we create a new address in this wallet
receiver = wallet.create_address()

# send 0.5 TRLT to the new address
recipients = [{'address': receiver, 'amount': 50}]

# if a wallet has multiple addresses a change address needs to be set
tx_hash = wallet.send_transaction(transfers=recipients, change_address=sender)

# after a while the funds should have arrived
print(wallet.get_balance(receiver))
{'availableBalance': 50, 'lockedAmount': 0}
```

Delayed Transactions
--------------------

```python
# Create a delayed transaction
>>> tx_hash = wallet.create_delayed_transaction(
    anonymity=3,
    transfers=[
        {
            'address': 'TRTL...',
            'amount': 50
        }
    ]
)

# List all delayed transactions
>>> wallet.get_delayed_transaction_hashes()
['bfcc4735a975f0ac0c27806b7abf9107adbd7a8a0c7c8ea91ca363eacda7f79x']

# Send delayed transaction
>>> wallet.send_delayed_transaction(tx_hash)
```

Developer setup
---------------

Install dependencies with pipenv:

```
pipenv install
```
