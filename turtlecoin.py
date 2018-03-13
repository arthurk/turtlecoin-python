import json
import requests


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

    def get_delayed_transaction_hashes(self):
        return self._make_request('getDelayedTransactionHashes')

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

    def send_transaction(self, anonymity, transfers, fee, source_addresses='',
                         change_address='', extra='', payment_id='', unlock_time=''):
        """
        Send a transaction to one or multiple addresses.

        Note:
            The amount/fee need to be multiplied by 100 to get TRTL amount.

            If you want to transfer 10 TRTL with a fee of 0.1 TRLT you should
            set transfer amount to 1000 and fee to 10

        Params:
            anonymity: mixin amount
            transfers: address where to send the funds to. (address, amount)
            fee: transaction fee
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

        """
        kwargs = {#'sourceAddresses': source_addresses,
                  'transfers': transfers,
                  #'changeAddress': change_address,
                  'fee': fee,
                  'anonymity': anonymity,
                  #'extra': extra,
                  #'paymentId': payment_id,
                  #'unlockTime': unlock_time}
                  }
        return self._make_request('sendTransaction', **kwargs)

    # def create_delayed_transaction(self, addresses, transfers, change_address,
    #                                fee, anonymity, extra, payment_id,
    #                                unlock_time):
    #     kwargs = {'addresses': addresses,
    #               'transfers': transfers,
    #               'changeAddress': change_address,
    #               'fee': fee,
    #               'anonymity': anonymity,
    #               'extra': extra,
    #               'paymentId': payment_id,
    #               'unlockTime': unlock_time}
    #     self._make_request('sendTransaction', **kwargs)

    # def delete_delayed_transaction(self, transaction_hash):
    #     kwargs = {'transactionHash': transaction_hash}
    #     self._make_request('deleteDelayedTransaction', **kwargs)

    # def send_delayed_transaction(self, transaction_hash):
    #     kwargs = {'transactionHash': transaction_hash}
    #     self._make_request('sendDelayedTransaction', **kwargs)

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



### FOllowing code is for debugging

# initialize wallet
# wallet = TurtleCoinWallet(password='test')
# import ipdb; ipdb.set_trace()

# create a new address
#print(wallet.create_address())

# create a new spend address from secret key
#print(wallet.create_address(spend_secret_key='5dd6d60b02927512a1acefd9814672fad757114cc21b794de8105a072f0e0b05'))

# create a new spend address from public key
# XXX doesnt work: application_code': 22}, 'message': 'Wrong parameters passed
#print(wallet.create_address(spend_public_key='0a5295482ac8a921090113679ce11052aa4934081ced3d375e6fa59e9998a58e'))

# print all addresses in this wallet
#addrs = wallet.get_addresses()
#print(addrs)

# print spend keys for first address
# print(addrs[0])
# print(wallet.get_spend_keys(addrs[0]))

# delete all addresses
# for a in addrs:
#     print(wallet.delete_address(a))

#print(wallet.get_view_key())
#print(wallet.get_spend_keys(address=addr))
# print(wallet.get_transaction_hashes(10, 0, block_hash='7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c',
#                                     addresses=[], payment_id=1))
