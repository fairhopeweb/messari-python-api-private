"""This module is meant to contain the Polygonscan class"""

from typing import Union, List
import pandas as pd
from messari.utils import validate_input

from messari.blockexplorers import Scanner

BASE_URL='https://api.polygonscan.com/api'
class Polygonscan(Scanner):
    """This class is a wrapper around the Polygonscan API
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
    def get_eth_uncle(self, block: int, index: int):
        """Override: return None
        """
        return None

    ##### Tokens
    def get_token_circulating_supply(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Returns ERC20 Circulating Supply (For Polygon Cross Chain token Types) by ContractAddress

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

    def get_gas_oracle(self) -> None:
        """Override: return None
        """
        return None

    ##### Stats
    def get_total_matic_supply(self) -> int:
        """Returns the current amount of Matic (Wei) in circulation.

        Returns
        -------
            DataFrame
                DataFrame with current amount of matic circulating
        """
        params = {'module': 'stats',
                  'action': 'maticsupply'}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        return int(response)

    def get_last_matic_price(self) -> pd.DataFrame:
        """Returns the latest price of 1 MATIC in BTC & USD

        Returns
        -------
            DataFrame
                DataFrame with current matic price
        """
        params = {'module': 'stats',
                  'action': 'maticprice'}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        maticbtc = response['maticbtc']
        maticusd = response['maticusd']
        price_dict = {'btc': maticbtc, 'usd': maticusd}
        price_df = pd.Series(price_dict).to_frame(name='matic_price')
        return price_df
