turtlecoin-walletd-rpc-python
=============================

A Python wrapper for the TurtleCoin walletd JSON-RPC interface

*In development*

TODO:

- Creating/Deleting Transactions

Quickstart
----------

You need to have walletd running with rpc enabled:

```
# generate a test wallet
$ ./walletd -w test.wallet -p any_password_you_want -g

# launch walletd with test wallet
$ ./walletd -w test.wallet -p any_password_you_want --local --rpc-password test
```

Usage
-----

Example for creating and deleting an address:

```python
import turtlecoin

wallet = TurtleCoinWallet(password='test')

address = wallet.create_address()

wallet.get_balance(address)
wallet.get_view_key()
wallet.get_spend_keys(address)

wallet.delete_address(address)
```
