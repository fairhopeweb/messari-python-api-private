"""This module is meant to contain the arbiscan class"""


from messari.blockexplorers import Scanner

BASE_URL='https://api.arbiscan.io/api'
class Arbiscan(Scanner):
    """This class is a wrapper around the arbiscan API
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
    def get_block_reward(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Override: return None
        """
        return None

    def get_block_countdown(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Override: return None
        """
        return None

    ##### Logs
    # NOTE: no changes

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
    def get_token_circulating_supply(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Get ERC20-Token Circulating Supply (Applicable for Arbitrum Cross Chain token Types) by ContractAddress
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

    def get_gas_oracle(self) -> None:
        """Override: return None
        """
        return None

    ##### Stats
    # NOTE: no changes
