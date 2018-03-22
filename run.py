# This script is for debugging/development

import logging

from turtlecoin import TurtleCoinWallet, TurtleCoinD

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

wallet = TurtleCoinWallet(password='test')
daemon = TurtleCoinD()

import ipdb; ipdb.set_trace()
