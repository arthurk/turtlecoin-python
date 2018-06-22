import logging

import requests
import json


class TurtleCoind:
    """
    Integrates with JSON-RPC interface of `TurtleCoind`.
    """

    def __init__(self, host='127.0.0.1', port=11898, password=''):
        self.url = f'http://{host}:{port}/json_rpc'
        self.headers = {'content-type': 'application/json'}
        self.password = password

    def _make_request(self, method, **kwargs):
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': kwargs,
            'password': self.password
        }
        logging.debug(json.dumps(payload, indent=4))
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response['result']

    def get_block_count(self):
        """
        Returns current chain height.

        Returns:
            dict::

            {'count': 286373, 'status': 'OK'}
        """
        return self._make_request('getblockcount')
    
    def get_block_hash(self, block_hash):
        payload = {
            'jsonrpc': '2.0',
            'method': 'on_getblockhash',
            'params': [block_hash],
            'password': self.password
        }
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response['result']

    def get_block_template(self, reserve_size, wallet_address):
        """
        Returns blocktemplate with an empty "hole" for nonce.

        Args:
            reserve_size (int): 123
            wallet_address (str): a valid wallet address

        Returns:
            dict: the block template::

            {
                'blocktemplate_blob': '0300f29a5cddd1a88f9b95...',
                'difficulty': 273666101,
                'height': 286393,
                'reserved_offset': 412,
                'status': 'OK'
            }
        """
        params = {'reserve_size': reserve_size,
                  'wallet_address': wallet_address}
        return self._make_request('getblocktemplate', **params)
    
    def submit_block(self, block_blob):
        payload = {
            'jsonrpc': '2.0',
            'method': 'submitblock',
            'params': [block_blob],
            'password': self.password
        }
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response['result']

    def get_last_block_header(self):
        """
        Returns last block header.

        Returns:
            dict: information about the last block header::

            {
                'block_header': {
                    'depth': 0,
                    'difficulty': 226559499,
                    'hash': '34aa8777302f4856e360fef49a0a7b6c78cc8eff999c0c716bad234837917986',
                    'height': 286397,
                    'major_version': 3,
                    'minor_version': 0,
                    'nonce': 18205,
                    'orphan_status': False,
                    'prev_hash': '522f53dae525f0a66064377c41bc1f78c6eb4eea2b3e7630efccd395bb17f43f',
                    'reward': 2954906,
                    'timestamp': 1521732086
                },
                'status': 'OK'
            }
        """
        return self._make_request('getlastblockheader')

    def get_block_header_by_hash(self, hash):
        """
        Returns last block header by given hash.

        Args:
            hash (str): a valid block hash

        Returns:
            dict: See getlastblockheader
        """
        params = {'hash': hash}
        return self._make_request('getblockheaderbyhash', **params)

    def get_block_header_by_height(self, height):
        """
        Returns last block header by given hash.

        Args:
            hash (int): a valid block height

        Returns:
            dict: See getlastblockheader
        """
        params = {'height': height}
        return self._make_request('getblockheaderbyheight', **params)

    def get_currency_id(self):
        """
        Returns unique currency identifier.

        Returns:
            dict::

            {'currency_id_blob': '7fb97df81221dd1366051b2...'}
        """
        return self._make_request('getcurrencyid')

    def get_blocks(self, height):
        params = {'height': height}
        return self._make_request('f_blocks_list_json', **params)

    def get_block(self, block_hash):
        params = {'hash': block_hash}
        return self._make_request('f_block_json', **params)
    
    def get_transaction(self, transaction_hash):
        params = {'hash' : transaction_hash}
        return self._make_request('f_transaction_json', **params)

    def get_transaction_pool(self):
        return self._make_request('f_on_transactions_pool_json')
