import json
import logging
import requests

from .utils import convert_bytes_to_hex_str


class Walletd:
    """
    Integrates with Walletd RPC interface.

    Run Walletd like this::

        $ walletd -w test.wallet -p mypw --local --rpc-password test
    """

    def __init__(self, password, host='127.0.0.1', port=8070):
        self.url = f'http://{host}:{port}/json_rpc'
        self.headers = {'content-type': 'application/json'}
        self.password = password

    def _make_request(self, method, **kwargs):
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'password': self.password,
            'id': 0,
            'params': kwargs
        }
        logging.debug(json.dumps(payload, indent=4))
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response

    def reset(self, view_secret_key):
        """
        Re-syncs the wallet

        Note:
            If the view_secret_key parameter is not specified, the reset() method resets the 
            wallet and re-syncs it. If the view_secret_key argument is specified, reset() 
            method substitutes the existing wallet with a new one with a specified
            view_secret_key and creates an address for it.
            
        """
        params = {'viewSecretKey': view_secret_key}
        return self._make_request('reset', **params)
    
    def save(self):
        """
        Save the wallet
        """
        return self._make_request('save')

    def export(self, file_name):
        params = {'fileName': file_name}
        return self._make_request('export', **params)

    def get_balance(self, address=''):
        """
        Returns the balance of an address

        Note:
            Amount needs to be divided by 100 to get decimal places.
            If balance returned is 1000 it means 10.00 TRTL

        Args:
            address (str): (optional) The address for which to return
                the balance. Must exist in this wallet.

        Returns:
            dict: available balance (int) and locked amount (int)::

            {
                'availableBalance': 1000,
                'lockedAmount': 0
            }
        """
        params = {'address': address}
        r = self._make_request('getBalance', **params)
        return r

    def get_status(self):
        return self._make_request('getStatus')

    def get_addresses(self):
        return self._make_request('getAddresses')

    def get_view_key(self):
        """
        Returns the view key

        Returns:
            str: Private view key
        """
        return self._make_request('getViewKey')

    def get_spend_keys(self, address):
        """
        Returns spend keys

        Args:
            address (str): Valid and existing in this container address

        Returns:
            dict: A dictionary with the secret and public spend keys::

            {
                'spendPublicKey': '3550a41b004520030941183b7f3e5ec075042cdde492044ea5064e4a1d99a3ba',
                'spendSecretKey': 'f66997b99f9a8444417f09b4bca710e7afe9285d581a5aa641cd4ac0b29f5d00'
            }
        """
        params = {'address': address}
        return self._make_request('getSpendKeys', **params)

    def get_unconfirmed_transaction_hashes(self, addresses=[]):
        """
        Returns the current unconfirmed transaction pool for addresses

        Args:
            addresses (list): (optional) List of addresses.
                If not set, all addresses of this wallet will be used.

        Returns:
            list: Hashes of unconfirmed transactions
        """
        params = {'addresses': addresses}
        r = self._make_request('getUnconfirmedTransactionHashes', **params)
        return r

    def create_address(self, spend_secret_key='', spend_public_key=''):
        """
        Create a new address

        Args:
            spend_secret_key (str)
            spend_public_key (str)

        Returns:
            str: the hash of the new address
        """
        params = {'spendSecretKey': spend_secret_key}
        # params = {'spendPublicKey': spend_public_key}
        return self._make_request('createAddress', **params)

    def create_address_list(self, spend_secret_keys):
        params = {'spendSecretKeys': spend_secret_keys}
        return self._make_request('createAddressList', **params)

    def delete_address(self, address):
        """
        Delete address from wallet

        Args:
            address (str): the address to delete

        Returns:
            bool: True if successful
        """
        params = {'address': address}
        self._make_request('deleteAddress', **params)
        return True

    def get_block_hashes(self, first_block_index, block_count):
        params = {'firstBlockIndex': first_block_index,
                  'blockCount': block_count}
        return self._make_request('getBlockHashes', **params)

    def get_transaction(self, transaction_hash):
        """
        Returns information about a particular transaction

        Args:
            transaction_hash (str): Hash of the requested transaction

        Returns:
            dict: information about the transaction::

            {'amount': -110,
             'blockIndex': 274123,
             'extra': '013ffd7e8481121a427a01e034cc9f4604d7b474412186ddd9fc56361dc0eafb72',
             'fee': 10,
             'isBase': False,
             'paymentId': '',
             'state': 0,
             'timestamp': 1521641265,
             'transactionHash': 'dc1221181e5745b9016fed2970bf002d14fe2ad8c90d7a55456d0eb459c7c2b8',
             'transfers': [{'address': 'TRTLuxBjcKs5Ubbopcwc9N6yV62781VdDCS4ZVFupFdWBm3UZrAabVFKwc6yLWQVV3agCBxYzGQhGJsHZokixfufgxZ7EK3d33A',
                            'amount': 100,
                            'type': 0},
                           {'address': 'TRTLuxqgEUr24bw6dWKEJnNHRWk8SfbpgfERJUX43Dys5xACTU22zTZBR32BFi8TavSNei6cU9ym6DPECaTrqQaaaFRgF3xKE73',
                            'amount': 790,
                            'type': 2},
                           {'address': 'TRTLuxqgEUr01cw61WKfJnNHRWk7SgbpgfERJUX4WDys5xACTU123TZBR32BFi8TavSNei6cU9ym6DPECaTrqQaaaFRgF3xKE73',
                            'amount': -900,
                            'type': 0}],
             'unlockTime': 0}
        """
        params = {'transactionHash': transaction_hash}
        r = self._make_request('getTransaction', **params)
        return r

    def get_transactions(self, addresses, block_hash, block_count,
                         payment_id):
        params = {'addresses': addresses,
                  'blockHash': block_hash,
                  'blockCount': block_count,
                  'paymentId': payment_id}
        return self._make_request('getTransactions', **params)

    def get_transaction_hashes(self, addresses, block_hash, block_count,
                               payment_id):
        params = {'addresses': addresses,
                  'blockHash': block_hash,
                  'blockCount': block_count,
                  'paymentId': payment_id}
        return self._make_request('getTransactionHashes', **params)

    def send_transaction(self, transfers, anonymity=3, fee=10,
                         addresses='', change_address='', extra='',
                         payment_id='', unlock_time=0):
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
            extra (bytes): extra data to include
            payment_id: can be given to receiver to identify transaction
            unlock_time (int)

        Example::

            >>> wallet.send_transaction(
                anonymity=3,
                transfers=[
                    {'address': 'TRTL...',
                     'amount': 500}],
                fee=10
            )
            {'transactionHash': '1b87a........'}
        """
        params = {'addresses': addresses,
                  'transfers': transfers,
                  'changeAddress': change_address,
                  'fee': fee,
                  'anonymity': anonymity,
                  'unlockTime': unlock_time}

        # payment_id and extra cannot be present at the same time
        # either none of them is included, or one of them
        if payment_id and extra:
            raise ValueError('payment_id and extra cannot be set together')
        elif payment_id:
            params['paymentId'] = payment_id
        elif extra:
            params['extra'] = convert_bytes_to_hex_str(extra)

        r = self._make_request('sendTransaction', **params)
        return r

    def get_delayed_transaction_hashes(self):
        """
        Returns a list of delayed transaction hashes
        """
        r = self._make_request('getDelayedTransactionHashes')
        return r

    def create_delayed_transaction(self, transfers, anonymity=3, fee=10,
                                   addresses='', change_address='',
                                   extra='', payment_id='', unlock_time=0):
        params = {'addresses': addresses,
                  'transfers': transfers,
                  'changeAddress': change_address,
                  'fee': fee,
                  'anonymity': anonymity,
                  'unlockTime': unlock_time}

        # payment_id and extra cannot be present at the same time
        # either none of them is included, or one of them
        if payment_id and extra:
            raise ValueError('payment_id and extra cannot be set together')
        elif payment_id:
            params['paymentId'] = payment_id
        elif extra:
            params['extra'] = convert_bytes_to_hex_str(extra)

        r = self._make_request('createDelayedTransaction', **params)
        return r

    def send_delayed_transaction(self, transaction_hash):
        """
        Send a delayed transaction

        Example::

            >>> wallet.send_delayed_transaction('8dea3...')

        Raises:
            ValueError: {
                'code': -32000,
                'data': {'application_code': 15},
                'message': 'Transaction transfer impossible'
            }
        """
        params = {'transactionHash': transaction_hash}
        self._make_request('sendDelayedTransaction', **params)
        return True

    def delete_delayed_transaction(self, transaction_hash):
        """
        Delete a delayed transaction

        Example:

            >>> wallet.delete_delayed_transaction('8dea3....')
        """
        params = {'transactionHash': transaction_hash}
        self._make_request('deleteDelayedTransaction', **params)
        return True

    def send_fusion_transaction(self, threshold, anonymity, addresses,
                                destination_address):
        """
        Send a fusion transaction, by taking funds from selected addresses and
        transferring them to the destination address.

        Returns:
            str: hash of the sent transaction
        """
        params = {'threshold': threshold,
                  'anonymity': anonymity,
                  'addresses': addresses,
                  'destinationAddress': destination_address}
        return self._make_request('sendFusionTransaction', **params)

    def estimate_fusion(self, threshold, addresses=[]):
        """
        Counts the number of unspent outputs of the specified addresses and
        returns how many of those outputs can be optimized.
        """
        params = {'threshold': threshold,
                  'addresses': addresses}
        return self._make_request('estimateFusion', **params)

    def get_mnemonic_seed(self, address):
        """
        Returns the mnemonic seed for the given address

        Args:
            address (str): Valid and existing in this container address

        Returns:
            str: mnemonic seed
        """
        params = {'address': address}
        return self._make_request('getMnemonicSeed', **params)

    def create_integrated_address(self, address, payment_id):
        """
        Creates a unique 236 char long address which corresponds to given
        address and paymentID

        Args:
            address (str): valid TRTL address
            payment_id (str): valid payment id

        Returns:
            str: integrated address
        """
        params = {'address': address,'paymentId': payment_id}
        return self._make_request('createIntegratedAddress', **params)

    def get_fee_info(self):
        """
        Gets the fee address and amount (if any) from the node that the
        turtle-service instance is currently connected to. This fee will be
        automatically sent to the address on every sendTransaction() and
        sendDelayedTransaction() request. Note that it does not apply to
        sendFusionTransaction().

        Returns:
            str: address
            int: amount
        """

        return self._make_request('getFeeInfo')
