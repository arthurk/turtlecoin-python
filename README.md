turtlecoin-walletd-rpc-python
=============================

A Python wrapper for the TurtleCoin walletd JSON-RPC interface

*In development*

TODO:

- Creating/sending delayed transactions
- Fusion transactions

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

Sending a transaction:

```
wallet = TurtleCoinWallet(password='test')

# transfer 10.00 TRTL to destination_address
recipents = [{'address': destination_address, 'amount': 1000}]

# mixin/anonymity is 3 and fee is 0.1 TRTL
wallet.send_transaction(
    anonymity=3,
    transfers=recipents,
    fee=10
)
```

Sending a transaction will return a transactionHash. You can enter it on the https://turtle-coin.com block explorer to see more details.
