import logging

import requests
import json


class TurtleCoinD:
    """
    Integrates with RPC interface of ./TurtleCoind

    Note: You have to start with blockexplorer enabled:

        ./TurtleCoind --enable_blockexplorer
    """

    def __init__(self, host='127.0.0.1', port=11898):
        self.url = f'http://{host}:{port}/json_rpc'
        self.headers = {'content-type': 'application/json'}

    def _make_request(self, method, **kwargs):
        payload = {
            "jsonrpc": "2.0",
            "id": 'test',
            "method": method,
            "params": kwargs
        }
        logging.debug(json.dumps(payload, indent=4))
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        return response

    def getcurrencyid(self):
        return self._make_request('getcurrencyid')

    def getlastblockheader(self):
        return self._make_request('getlastblockheader')

    def f_transaction_json(self, tx_hash):
        params = {'hash': tx_hash}
        return self._make_request('f_transaction_json', **params)

    def f_blocks_list_json(self, height):
        params = {'height': height}
        return self._make_request('f_blocks_list_json', **params)

    def f_block_json(self, block_hash):
        params = {'hash': block_hash}
        return self._make_request('f_block_json', **params)

    def f_on_transactions_pool_json(self):
        return self._make_request('f_on_transactions_pool_json')

    # def getblockcount
    #{"error":{"code":-32603,"message":"JsonValue type is not ARRAY or OBJECT"},"id":"test","jsonrpc":"2.0"}
