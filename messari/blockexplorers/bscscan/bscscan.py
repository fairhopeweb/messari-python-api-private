"""This module is meant to contain the BSCscan class"""


import pandas as pd
from typing import Union, List
from messari.blockexplorers import Scanner
from messari.utils import validate_input

BASE_URL='https://api.bscscan.com/api'
class BSCscan(Scanner):
    """This class is a wrapper around the BSCscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)

    ##### Accounts
    # NOTE: no changes

    ##### Contracts
    # NOTE: no changes

    ##### Transactions
    def get_contract_execution_status(self, transactions_in: Union[str, List]):
        """Override: return None
        """
        return None

    ##### Blocks
    # NOTE: no changes

    ##### Logs
    # NOTE: no changes

    ##### Geth/Parity Proxy
    def get_eth_uncle(self, block: int, index: int):
        """Override: return None
        """
        return None

    ##### Tokens
    def get_token_circulating_supply(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Returns BEP-20 Token Circulating Supply

        Parameters
        ----------
            tokens_in: str, List
                single token address in or list of token addresses

        Returns
        -------
            DataFrame
                DataFrame containing total supply for token(s)
        """
        tokens = validate_input(tokens_in)
        supply_dict = {}
        for token in tokens:
            params = {'module': 'stats',
                      'action': 'tokenCsupply',
                      'contractaddress': token}
            params.update(self.api_dict)
            supply = self.get_response(self.base_url, params=params)['result']
            supply_dict[token] = supply
        supply_df = pd.Series(supply_dict).to_frame(name='supply')
        return supply_df

    ##### Gas Tracker
    def get_est_confirmation(self, gas_price: int):
        """Override: return None
        """
        return None

    ##### Stats
    def get_total_bnb_supply(self) -> int:
        """Returns the current amount of bnb (Wei) in circulation.

        Returns
        -------
            DataFrame
                DataFrame with current amount of bnb circulating
        """
        params = {'module': 'stats',
                  'action': 'bnbsupply'}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        return int(response)

    def get_validators(self) -> pd.DataFrame:
        """Returns the top 21 validators for the Binance Smart Chain

        Returns
        -------
            DataFrame
                DataFrame with top 21 validators
        """
        params = {'module': 'stats',
                  'action': 'validators'}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        return pd.DataFrame(response)

    def get_last_bnb_price(self) -> pd.DataFrame:
        """Returns the latest price of 1 BNB in BTC & USD

        Returns
        -------
            DataFrame
                DataFrame with current bnb price
        """
        params = {'module': 'stats',
                  'action': 'bnbprice'}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        # yes, the respone really gives back 'ethusd' and 'btcusd'
        bnbbtc = response['ethbtc']
        bnbusd = response['ethusd']
        price_dict = {'btc': bnbbtc, 'usd': bnbusd}
        price_df = pd.Series(price_dict).to_frame(name='bnb_price')
        return price_df
