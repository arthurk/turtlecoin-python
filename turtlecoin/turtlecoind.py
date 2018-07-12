import logging

import requests
import json


class TurtleCoind:
    """
    Integrates with JSON-RPC interface of `TurtleCoind`.
    """

    def __init__(self, host='127.0.0.1', port=11898):
        self.url = f'http://{host}:{port}'
        self.headers = {'content-type': 'application/json'}

    def _make_request(self, method, **kwargs):
        post_url = self.url +'/json_rpc'
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': kwargs,
        }
        logging.debug(json.dumps(payload, indent=4))
        response = requests.post(post_url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response

    def _make_get_request(self, method):
        get_url = self.url + '/' + method
        print(get_url)
        response = requests.get(get_url)
        return response.json()

    def get_height(self):
        """
        Returns current chain height

        Returns:
            dict::

                {
                    'height': 613945,
                    'network_height': 613945,
                    'status': 'OK'
                }
        """
        return self._make_get_request('getheight')

    def get_info(self):
        """
        Returns information of network and connection

        Returns:
            dict::
                {
                    'alt_blocks_count': 7,
                    'difficulty': 162204943,
                    'grey_peerlist_size': 736,
                    'hashrate': 5406831,
                    'height': 613945,
                    'incoming_connections_count': 0,
                    'last_known_block_index': 613942,
                    'major_version': 4,
                    'minor_version': 0,
                    'network_height': 613945,
                    'outgoing_connections_count': 8,
                    'start_time': 1531374018,
                    'status': 'OK',
                    'supported_height': 620000,
                    'synced': True,
                    'testnet': False,
                    'tx_count': 719763,
                    'tx_pool_size': 0,
                    'upgrade_heights': [
                        187000,
                        350000,
                        440000,
                        620000,
                        ...
                    ],
                    'version': '0.6.4',
                    'white_peerlist_size': 52
                }
        """
        return self._make_get_request('getinfo')

    def get_transactions(self):
        """
        Returns array of missed transactions

        Returns:
            dict::
                {
                    'missed_tx': [],
                    'status': 'OK',
                    'txs_as_hex': []
                }
        """
        return self._make_get_request('gettransactions')

    def get_peers(self):
        """
        Returns array of peers connected to the daemon

        Returns:
            dict::
                {
                    'peers': [
                        142.44.212.51:11897,
                        45.55.33.219:11897.
                        ...
                    ],
                    'status': 'OK
                }
        """
        return self._make_get_request('getpeers')

    def get_fee_info(self):
        """
        Returns information on fee set by remote node

        Returns:
            dict::
                {
                    'address': '',
                    'amount': 0,
                    'status': "Node's fee address is not set"
                }
        """
        return self._make_get_request('feeinfo')

    def get_block_count(self):
        """
        Returns current chain height.

        Returns:
            dict::

            {
                "jsonrpc":"2.0",
                "result":{
                    "count":560915,
                    "status":"OK"
                }
            }
        """
        return self._make_request('getblockcount')
    
    def get_block_hash(self, block_hash):
        """
        Returns block hash for a given height off by one
        
        Args:
            height : 123456
            
        Returns:
            dict:: result
            
            {
                "jsonrpc": "2.0",
                "result": "4bd7dd9649a006660e113efe49691e0739d9838d044774f18732111b145347c8"
            }
        """
        payload = {
            'jsonrpc': '2.0',
            'method': 'on_getblockhash',
            'params': [block_hash]
        }
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response

    def get_block_template(self, reserve_size, wallet_address):
        """
        Returns blocktemplate with an empty "hole" for nonce.

        Args:
            reserve_size (int): 123
            wallet_address (str): a valid wallet address

        Returns:
            dict: the block template::

            {
                "blocktemplate_blob": "0300f29a5cddd1a88f9b95...",
                "difficulty": 273666101,
                "height": 286393,
                "reserved_offset": 412,
                "status": "OK"
            }
        """
        params = {'reserve_size': reserve_size,
                  'wallet_address': wallet_address}
        return self._make_request('getblocktemplate', **params)
    
    def submit_block(self, block_blob):
        """
        Submits a block
        
        Args:
            block_blob (str) : a valid block blob ...
        
        Returns:
            dict::
            
            {
                "jsonrpc": "2.0"
                "result": {
                    "status": "OK"
                }
            }
        """
        payload = {
            'jsonrpc': '2.0',
            'method': 'submitblock',
            'params': [block_blob]
        }
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers=self.headers).json()
        if 'error' in response:
            raise ValueError(response['error'])
        return response

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
        """
        Returns information on the last 30 blocks before height (inclusive)
        
        Args:
            height: the height of the blockchain to start at
            
        Returns:
            dict::
            
            {
                "jsonrpc": "2.0",
                "result": {
                    'blocks':[
                        {
                            "cumul_size": 22041,
                            "difficulty": 285124963,
                            "hash": "62f0058453292af5e1aa070f8526f7642ab6974c6af2c17088c21b31679c813d",
                            "height": 500000,
                            "timestamp": 1527834137,
                            "tx_count": 4
                        },
                        .....,
                        .....,
                    ],
                    "status": "OK"
                }
            }
        """
        params = {'height': height}
        return self._make_request('f_blocks_list_json', **params)

    def get_block(self, block_hash):
        """
        Returns information on a single block
        
        Args:
            block_hash: Block hash of the block you wish to retrieve
            
        Returns:
            dict::
            
            {
                "block": {
                    "alreadyGeneratedCoins": "1484230931125",
                    "alreadyGeneratedTransactions": 974921,
                    "baseReward": 2935998,
                    "blockSize": 48846,
                    "depth": 0,
                    "difficulty": 358164537,
                    "effectiveSizeMedian": 100000,
                    "hash": "f11580d74134ac34673c74f8da458080aacbe1eccea05b197e9d10bde05139f5",
                    "height": 501854,
                    "major_version": 4,
                    "minor_version": 0,
                    "nonce": 214748383,
                    "orphan_status": false,
                    "penalty": 0,
                    "prev_hash": "674046ea53a8673c630bd34655c4723199e69fdcfd518503f4c714e16a7121b5",
                    "reward": 2936608,
                    "sizeMedian": 231,
                    "timestamp": 1527891820,
                    "totalFeeAmount": 610,
                    "transactions": [
                        {
                            "amount_out": 2936608,
                            "fee": 0,
                            "hash": "61b29d7a3fe931928388f14cffb5e705a68db219e1df6b4e15aee39d1c2a16e8",
                            "size": 266
                        },
                        .....,
                        .....,
                    ],
                    "transactionsCumulativeSize": 48535
                },
                "status": "OK"
            }
        """
        params = {'hash': block_hash}
        return self._make_request('f_block_json', **params)
    
    def get_transaction(self, transaction_hash):
        """
        Gets information on the single transaction
        
        Args:
            transaction_hash: (str) The transaction hash
            
        Returns:
            dict::
            
            {
                "block": {
                    "cumul_size": 22041,
                    "difficulty": 103205633,
                    "hash": "62f0058453292af5e1aa070f8526f7642ab6974c6af2c17088c21b31679c813d",
                    "height": 500000,
                    "timestamp": 1527834137,
                    "tx_count": 4
                },
                "status": "OK",
                "tx": {
                    "extra": "019e430ecdd501714900c71cb45fd49b4fa77ebd4a68d967cc2419ccd4e72378e3020800000000956710b6",
                    "unlock_time": 500040,
                    "version": 1,
                    "vin": [
                        {
                            "type": "ff",
                            "value": {
                                "height": 500000
                            }
                        }
                    ],
                    "vout": [
                        {
                            "amount": 80,
                            "target": {
                                "data": {
                                    "key": "5ce69a87940df7ae8443261ff610861d2e4207a7556ef1aa35878c0a5e7e382d"
                                },
                            "type": "02"
                            }
                        },
                        .....,
                        .....,
                    ]
                },
                "txDetails": {
                    "amount_out": 2936280,
                    "fee": 0,
                    "hash": "702ad5bd04b9eff14b080d508f69a320da1909e989d6c163c18f80ae7a5ab832",
                    "mixin": 0,
                    "paymentId": "",
                    "size": 266
                }
            }
        """
        params = {'hash' : transaction_hash}
        return self._make_request('f_transaction_json', **params)

    def get_transaction_pool(self):
        """
        Gets the list of transaction hashs in the mempool.
        
        Returns:
            dict::
            
            {
                "jsonrpc": "2.0"
                "transactions": [
                    {
                        "amount_out": 1660000,
                        "fee": 0,
                        "hash": "721ae50994d5446d5683ca79d6fa97dce321a39e88e1df70ae433dc67573841b",
                        "size": 13046
                    },
                    .....,
                    .....,
                ]
            }
        """
        return self._make_request('f_on_transactions_pool_json')
