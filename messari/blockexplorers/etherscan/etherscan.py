"""This module is meant to contain the Etherscan class"""

from typing import Union, List
import datetime
import pandas as pd

from messari.utils import validate_input, validate_datetime
from messari.blockexplorers import Scanner

# Refrence: https://docs.etherscan.io/

BASE_URL='https://api.etherscan.io/api'
class Etherscan(Scanner):
    """This class is a wrapper around the Etherscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)

    ##### Accounts
    # NOTE: no changes

    ##### Transactions
    # NOTE: no changes

    ##### Blocks
    # NOTE: no changes

    ##### Geth/Parity Proxy
    # NOTE: no changes

    ##### Tokens
    # NOTE: no changes

    ##### Gas Tracker
    # NOTE: no changes

    ##### Stats
    def get_total_eth_supply(self) -> int:
        """Returns the current amount of Ether in circulation.
        """
        params = {'module': 'stats',
                  'action': 'ethsupply'}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        return response

    def get_total_eth2_supply(self) -> pd.DataFrame:
        """Returns the current amount of Ether in circulation,
        ETH2 Staking rewards and EIP1559 burnt fees statistics
        """
        params = {'module': 'stats',
                  'action': 'ethsupply2'}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        price_df = pd.Series(response).to_frame(name='eth2_supply')
        return price_df

    def get_last_eth_price(self) -> pd.DataFrame:
        """Returns the latest price of 1 ETH in BTC & USD
        """
        params = {'module': 'stats',
                  'action': 'ethprice'}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        ethbtc = response['ethbtc']
        ethusd = response['ethusd']
        price_dict = {'btc': ethbtc, 'usd': ethusd}
        price_df = pd.Series(price_dict).to_frame(name='eth_price')
        return price_df

    def get_nodes_size(self, start_date: Union[str, datetime.datetime],
                       end_date: Union[str, datetime.datetime],
                       client_type: str='geth', sync_mode: str='archive',
                       ascending: bool=True) -> pd.DataFrame:
        """Returns the size of the Ethereum blockchain, in bytes, over a date range
        """
        start = validate_datetime(start_date)
        end = validate_datetime(end_date)
        sort = 'asc' if ascending else 'desc'
        params = {'module': 'stats',
                  'action': 'chainsize',
                  'startdate': start,
                  'enddate': end,
                  'clienttype': client_type,
                  'syncmode': sync_mode,
                  'sort': sort}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        size_df = pd.DataFrame(response)
        return size_df

    def get_total_nodes_count(self) -> int:
        """Returns the total number of discoverable Ethereum nodes
        """
        params = {'module': 'stats',
                  'action': 'nodecount'}
        params.update(self.api_dict)
        nodes_count = self.get_response(self.BASE_URL, params=params)['result']['TotalNodeCount']
        return nodes_count
