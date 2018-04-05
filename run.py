# This script is for debugging/development
# It initializes Wallatd and TurtleCoinD with debug logging enabled

import logging

from turtlecoin import Walletd, TurtleCoind

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

wallet = Walletd(password='test')
#daemon = TurtleCoind()
import ipdb; ipdb.set_trace()

#wallet.get_balance()
