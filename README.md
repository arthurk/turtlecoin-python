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

```python
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

Developer setup
---------------

Install dependencies with pipenv:

```
pipenv install
```
