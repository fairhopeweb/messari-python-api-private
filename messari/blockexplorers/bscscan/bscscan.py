"""This module is meant to contain the BSCscan class"""


import pandas as pd
from typing import Union, List
from messari.blockexplorers import Scanner
from messari.utils import validate_input, validate_datetime

BASE_URL='https://api.bscscan.io/api'
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
    def get_contract_execution_status(self, transactions_in: Union[str, List]) -> None:
        """Override: return None
        """
        return None

    ##### Blocks
    # NOTE: no changes

    ##### Logs
    # NOTE: no changes

    ##### Geth/Parity Proxy
    # NOTE: no changes

    ##### Tokens
    def get_token_circulating_supply(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Returns BEP-20 Token Circulating Supply
        """
        tokens = validate_input(tokens_in)
        supply_dict = {}
        for token in tokens:
            params = {'module': 'stats',
                      'action': 'tokenCsupply',
                      'contractaddress': token}
            params.update(self.api_dict)
            supply = self.get_response(self.BASE_URL, params=params)['result']
            supply_dict[token] = supply
        supply_df = pd.Series(supply_dict).to_frame(name='supply')
        return supply_df

    ##### Gas Tracker
    def get_est_confirmation(self, gas_price: int) -> None:
        """Override: return None
        """
        return None

    ##### Stats
    def get_total_bnb_supply(self) -> int:
        """Returns the current amount of bnb (Wei) in circulation.
        """
        params = {'module': 'stats',
                  'action': 'bnbsupply'}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        return response

    def get_validators(self) -> pd.DataFrame:
        """Returns the top 21 validators for the Binance Smart Chain
        """
        params = {'module': 'stats',
                  'action': 'validators'}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        return pd.DataFrame(response)

    def get_last_bnb_price(self) -> pd.DataFrame:
        """Returns the latest price of 1 BNB in BTC & USD
        """
        params = {'module': 'stats',
                  'action': 'bnbprice'}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        # yes, the respone really gives back 'ethusd' and 'btcusd'
        bnbbtc = response['ethbtc']
        bnbusd = response['ethusd']
        price_dict = {'btc': bnbbtc, 'usd': bnbusd}
        price_df = pd.Series(price_dict).to_frame(name='bnb_price')
        return price_df
