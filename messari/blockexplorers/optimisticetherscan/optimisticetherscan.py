"""This module is meant to contain the OptimisticEtherscan class"""

from typing import Union, List, Dict
import pandas as pd

from messari.blockexplorers import Scanner
from messari.utils import validate_input, validate_datetime, validate_int

BASE_URL='https://api-optimistic.etherscan.io/api'
# Reference: https://optimistic.etherscan.io/apis
class OptimisticEtherscan(Scanner):
    """This class is a wrapper around the OptimisticEtherscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)

    ##### Accounts
    def get_account_l1_deposits(self, accounts_in: Union[str, List], ascending:bool=True) -> pd.DataFrame:
        accounts = validate_input(accounts_in)
        sort = 'asc' if ascending else 'desc'
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'getdeposittx',
                      'address': account,
                      'sortorder': sort}
            params.update(self.api_dict)
            response = self.get_response(self.BASE_URL, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        deposits_df = pd.concat(df_list, keys=accounts, axis=1)
        return deposits_df

    def get_account_l2_withdrawals(self, accounts_in: Union[str, List], ascending:bool=True) -> pd.DataFrame:
        accounts = validate_input(accounts_in)
        # NOTE: sort may not be an argument
        sort = 'asc' if ascending else 'desc'
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'getwithdrawaltx',
                      'address': account,
                      'sortorder': sort}
            params.update(self.api_dict)
            response = self.get_response(self.BASE_URL, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        deposits_df = pd.concat(df_list, keys=accounts, axis=1)
        return deposits_df

    #TODO: missing a lot?

    ##### Contracts
    # NOTE: no changes

    ##### Transactions
    def get_contract_execution_status(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Override: return None
        """
        return None

    def get_transaction_execution_status(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Override: return None
        """
        return None

    ##### Blocks
    def get_block_reward(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Override: return None
        """
        return None

    def get_block_countdown(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Override: return None
        """
        return None

    def get_block_by_timestamp(self, times_in: Union[int, List], before: bool=True) -> pd.DataFrame:
        """Override: return None
        """
        return None

    ##### Logs
    def get_logs(self, address: str, from_block: Union[int, str], to_block: Union[int, str]='latest',
                 topic0: str=None, topic1: str=None, topic2: str=None, topic3: str=None,
                 topic0_1_opr: str=None, topic1_2_opr: str=None, topic2_3_opr: str=None,
                 topic0_2_opr: str=None, topic0_3_opr: str=None, topic1_3_opr: str=None) -> pd.DataFrame:
        """Override: return None
        """
        return None

    ##### Geth/Parity Proxy
    def get_eth_block_number(self) -> int:
        """Override: return None
        """
        return None

    def get_eth_block(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Override: return None
        """
        return None

    def get_eth_uncle(self, block: int, index: int):
        """Override: return None
        """
        return None

    def get_eth_block_transaction_count(self, blocks_in: Union[int, List]):
        """Override: return None
        """
        return None

    def get_eth_transaction_by_hash(self, transactions_in: Union[str, List]):
        """Override: return None
        """
        return None

    def get_eth_transaction_by_block_index(self, block: int, index: int):
        """Override: return None
        """
        return None

    def get_eth_account_transaction_count(self, accounts_in: Union[str, List]):
        """Override: return None
        """
        return None

    def get_eth_transaction_receipt(self, transactions_in: Union[str, List]):
        """Override: return None
        """
        return None

    def get_eth_gas_price(self) -> int:
        """Override: return None
        """
        return None

    ##### Tokens
    # NOTE: no changes

    ##### Gas Tracker
    def get_est_confirmation(self, gas_price: int) -> int:
        """Override: return None
        """
        return None

    def get_gas_oracle(self) -> pd.DataFrame:
        """Override: return None
        """
        return None

    ##### Stats
    def get_total_matic_supply(self) -> int:
        """Returns the current amount of ETH (Wei) in circulation on optimism
        """
        params = {'module': 'stats',
                  'action': 'optimismsupply'}
        params.update(self.api_dict)
        response = self.get_response(self.BASE_URL, params=params)['result']
        return response
