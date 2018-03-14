import json
import string
import random
import requests


def generate_payment_id():
    """
    Generate a random payment_id for transactions
    """
    return ''.join(random.choices(string.hexdigits, k=64)).lower()


def format_amount(amount):
    """
    Format amount into user-friendly format
    """
    return float(amount/100)


def parse_amount(amount):
    """
    Format amount from user-friendly format to internal representation
    """
    return int(amount*100)


class TurtleCoinWallet:
    def __init__(self, password, host='127.0.0.1', port=8070):
        self.url = f'http://{host}:{port}/json_rpc'
        self.headers = {'content-type': 'application/json'}
        self.password = password

    def _make_request(self, method, **kwargs):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "password": self.password,
            "id": 0,
            "params": kwargs
        }
        print(json.dumps(payload, indent=4))
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response['result']

    def save(self):
        return self._make_request('save')

    def export(self, file_name):
        kwargs = {'fileName': file_name}
        return self._make_request('export', **kwargs)

    def get_balance(self, address=''):
        """
        Returns the balance.

        Note:
            Amount needs to be divided by 100 to get decimal places.
            If balance returned is 1000 it means 10.00 TRTL

        Args:
            address (str): The address for which to return the balance

        Returns:
            dict: available balance (int) and locked amount (int)

                {
                    'availableBalance': 1000,
                    'lockedAmount': 0
                }
        """
        kwargs = {'address': address}
        return self._make_request('getBalance', **kwargs)

    def get_status(self):
        return self._make_request('getStatus')

    def get_addresses(self):
        return self._make_request('getAddresses')['addresses']

    def get_view_key(self):
        return self._make_request('getViewKey')

    def get_spend_keys(self, address):
        kwargs = {'address': address}
        return self._make_request('getSpendKeys', **kwargs)

    def get_unconfirmed_transaction_hashes(self, addresses=None):
        kwargs = {'addresses': addresses}
        return self._make_request('getUnconfirmedTransactionHashes', **kwargs)


    def create_address(self, spend_secret_key='', spend_public_key=''):
        kwargs = {'spendSecretKey': spend_secret_key}
        # kwargs = {'spendPublicKey': spend_public_key}
        return self._make_request('createAddress', **kwargs)

    def create_address_list(self, spend_secret_keys):
        kwargs = {'spendSecretKeys': spend_secret_keys}
        return self._make_request('createAddressList', **kwargs)

    def delete_address(self, address):
        kwargs = {'address': address}
        self._make_request('deleteAddress', **kwargs)
        return True

    def get_block_hashes(self, first_block_index, block_count):
        kwargs = {'firstBlockIndex': first_block_index,
                  'blockCount': block_count}
        return self._make_request('getBlockHashes', **kwargs)

    def get_transaction(self, transaction_hash):
        kwargs = {'transactionHash': transaction_hash}
        self._make_request('getTransaction', **kwargs)

    def get_transactions(self, addresses, block_hash_string, block_count,
                         payment_id):
        kwargs = {'addresses': addresses,
                  'blockHashString': block_hash_string,
                  'blockCount': block_count,
                  'paymentId': payment_id}
        self._make_request('getTransactions', **kwargs)

    def get_transaction_hashes(self, addresses, block_hash, block_count,
                               payment_id):
        kwargs = {'addresses': addresses,
                  'blockHash': block_hash,
                  'blockCount': block_count,
                  'paymentId': payment_id}
        return self._make_request('getTransactionHashes', **kwargs)

    def send_transaction(self, anonymity, transfers, fee=10, source_addresses='',
                         change_address='', extra='', payment_id='', unlock_time=0):
        """
        Send a transaction to one or multiple addresses.

        Note:
            The amount/fee need to be multiplied by 100 to get TRTL amount.

            If you want to transfer 10 TRTL with a fee of 0.1 TRLT you should
            set transfer amount to 1000 and fee to 10

        Params:
            anonymity: mixin amount
            transfers: address where to send the funds to. (address, amount)
            fee: transaction fee (default 100 (0.1 TRTL))
            source_addresses: addresses from which to take the funds from.
            change_address: address where to send the change to.
            extra: ...
            payment_id: can be given to receiver to identify transaction
            unlock_time: ...


        Example:
            >>> wallet.send_transaction(
                anonymity=3,
                transfers=[
                    {'address': 'TRTL...', 
                     'amount': 500}],
                fee=10
            )
            {'transactionHash': '1b87a........'}

        binascii.hexlify(b'TUT TUT').decode()

        payment_id key should not be present in kwargs dict if
        extra is passed too

        """
        if payment_id and extra:
            raise ValueError('payment_id and extra cannot be set together')

        kwargs = {'sourceAddresses': source_addresses,
                  'transfers': transfers,
                  'changeAddress': change_address,
                  'fee': fee,
                  'anonymity': anonymity,
                  'paymentId': payment_id,
                  #'extra': extra,
                  'unlockTime': unlock_time}
        return self._make_request('sendTransaction', **kwargs)

    def get_delayed_transaction_hashes(self):
        """
        Returns a list of delayed transaction hashes
        """
        r = self._make_request('getDelayedTransactionHashes')
        return r['transactionHashes']

    def create_delayed_transaction(self, anonymity, transfers, fee=10, source_addresses='',
                         change_address='', extra='', payment_id='', unlock_time=0):
        kwargs = {'sourceAddresses': source_addresses,
                  'transfers': transfers,
                  'changeAddress': change_address,
                  'fee': fee,
                  'anonymity': anonymity,
                  'paymentId': payment_id,
                  #'extra': extra,
                  'unlockTime': unlock_time}
        r = self._make_request('createDelayedTransaction', **kwargs)
        return r['transactionHash']

    def send_delayed_transaction(self, transaction_hash):
        """
        Send a delayed transaction

        Example:

            >>> wallet.send_delayed_transaction('8dea3...')

        Raises:
            If the delayed tx is not valid:

            ValueError: {
                'code': -32000,
                'data': {'application_code': 15},
                'message': 'Transaction transfer impossible'
            }
        """
        kwargs = {'transactionHash': transaction_hash}
        self._make_request('sendDelayedTransaction', **kwargs)
        return True

    def delete_delayed_transaction(self, transaction_hash):
        """
        Delete a delayed transaction

        Example:

            >>> wallet.delete_delayed_transaction('8dea3....')
        """
        kwargs = {'transactionHash': transaction_hash}
        self._make_request('deleteDelayedTransaction', **kwargs)
        return True

    # def send_fusion_transaction(self, threshold, anonymity, addresses,
    #                             destination_address):
    #     kwargs = {'threshold': threshold,
    #               'anonymity': anonymity,
    #               'addresses': addresses,
    #               'destinationAddress': destination_address}
    #     self._make_request('sendFusionTransaction', **kwargs)

    # def estimate_fusion(self, threshold, addresses):
    #     kwargs = {'threshold': threshold,
    #               'addresses': addresses}
    #     self._make_request('estimateFusion', **kwargs)


### Following code is for debugging

# initialize wallet
# wallet = TurtleCoinWallet(password='test')
# import ipdb; ipdb.set_trace()
