"""This module is meant to contain the Etherscan class"""

from typing import Union, List, Dict
import datetime
import pandas as pd

from messari.dataloader import DataLoader
from messari.utils import validate_input, validate_datetime

# Refrence: https://docs.etherscan.io/

BASE_URL='https://api.etherscan.io/api'

#dict.update(dict)


class Etherscan(DataLoader):
    """This class is a wrapper around the Etherscan API
    """

    def __init__(self, api_key: str=None):
        # TODO, api key
        # TODO, use ENS as pseudo taxonomy
        api_dict = {'apikey': api_key}
        DataLoader.__init__(self, api_dict=api_dict, taxonomy_dict={}) # TODO, figure out

    ##### Accounts
    # TODO
    def get_account_ether_balance(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the Ether balance of a given address
        """
        accounts = validate_input(accounts_in)
        balance_dict={}
        for account in accounts:
            params = {'module': 'account',
                      'action': 'balance',
                      'address': account,
                      'tag': 'latest'}
            params.update(self.api_dict)
            balance = self.get_response(BASE_URL, params=params)['result']
            balance_dict[account] = balance
        balances_df = pd.Series(balance_dict).to_frame(name='balances')
        return balances_df

    def get_account_normal_transactions(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the list of transactions performed by an address, with optional pagination
        """
        # TODO paging
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts: 
            params = {'module': 'account',
                      'action': 'txlist',
                      'address': account}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        account_transactions_df = pd.concat(df_list, keys=accounts, axis=1)
        return account_transactions_df

    def get_account_internal_transactions(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the list of internal transactions performed by an address, with optional pagination
        """
        # TODO paging
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts: 
            params = {'module': 'account',
                      'action': 'txlistinternal',
                      'address': account}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        account_transactions_df = pd.concat(df_list, keys=accounts, axis=1)
        return account_transactions_df

    def get_transaction_internal_transactions(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the list of internal transactions performed within a transaction
        """
        transactions = validate_input(transactions_in)
        df_list=[]
        for transactoin in transactions:
            params = {'module': 'account',
                      'action': 'txlistinternal',
                      'txhash': transactions}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        transactions_df = pd.concat(df_list, keys=accounts, axis=1)
        return transactions_df

    def get_block_range_internal_transactions(self, start_block: int, end_block: int, page: int=0, offset: int=0, ascending:bool=True) -> pd.DataFrame:
        """Returns the list of internal transactions performed within a block range, with optional pagination
        """
        # TODO check paging
        sort = 'asc' if ascending else 'desc'
        params = {'module': 'account',
                  'action': 'txlistinternal',
                  'startblock': start_block,
                  'endblock': end_block,
                  'page': page,
                  'offset': offset,
                  'sort': sort}
        params.update(self.api_dict)
        response = self.get_response(BASE_URL, params=params)['result']
        transactions_df = pd.DataFrame(response)
        return transactions_df

    def get_account_token_transfers(self, accounts_in: Union[str, List], tokens_in: Union[str, List]=None, start_block: int=None, end_block: int=None, page:int=0, offset:int=0, ascending:bool=True) -> pd.DataFrame:
        # TODO optional contract filtering
        # TODO block filtering
        """Returns the list of ERC-20 tokens transferred by an address, with optional filtering by token contract
        """
        sort = 'asc' if ascending else 'desc'
        accounts = validate_input(accounts_in)
        if tokens_in:
            tokens = validate_input(tokens_in)
        else:
            tokens=None
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'tokentx',
                      'address': account}
            if start_block:
                params.update({'startblock': start_block})
            if end_block:
                params.update({'endblock': start_block})
            params.update(self.api_dict)


            # iterate through optional token filters
            response=[]
            if tokens:
                for token in tokens:
                    response += self.get_response(BASE_URL, params=params)['result']
            else:
                response = self.get_response(BASE_URL, params=params)['result']


            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        token_transfers_df = pd.concat(df_list, keys=accounts, axis=1)
        return token_transfers_df

    def get_account_nft_transfers(self) -> pd.DataFrame:
        # TODO more args
        """Returns the list of ERC-721 ( NFT ) tokens transferred by an address, with optional filtering by token contract
        """
        # TODO, gonna be the exact same as get_account_token_transfers
        return

    def get_account_blocks_mined(self, accounts_in: Union[str, List], block_type:str='blocks', page:int=0, offset:int=0) -> pd.DataFrame:
        # TODO more args
        """Returns the list of blocks mined by an address
        """
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'getminedblocks',
                      'page': page,
                      'offset': offset,
                      'address': account}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        blocks_mined_df = pd.concat(df_list, keys=accounts, axis=1)
        return blocks_mined_df

    ##### Contracts
    def get_contract_abi(self, contracts_in: Union[str, List]) -> Dict:
        """Returns the Contract Application Binary Interface (ABI) of a verified smart contract
        """
        contracts = validate_input(contracts_in)
        abi_dict = {}
        for contract in contracts:
            params = {'module': 'contract',
                      'action': 'getabi',
                      'address': account}
            params.update(self.api_dict)
            abi = self.get_response(BASE_URL, params=params)['result']
            abi_dict[contract] = abi
        return abi_dict

    def get_contract_source_code(self, contracts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the Solidity source code of a verified smart contract
        """
        contracts = validate_input(contracts_in)
        df_list=[]
        for contract in contracts:
            params = {'module': 'contract',
                      'action': 'getsourcecode',
                      'address': account}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        source_df = pd.concat(df_list, keys=contracts, axis=1)
        return source_df

    ##### Transactions
    def get_contract_execution_status(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the status code of a contract execution
        """
        transactions = validate_input(transactions_in)
        transactions_dict={}
        for transaction in transactions:
            params = {'module': 'transaction',
                      'action': 'getstatus',
                      'txhah': transaction}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            transactions_dict[transaction] = response
        transactions_df = pd.Series(transactions_dict).to_frame(name='transactions')
        return transactions_df

    def get_transaction_execution_status(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the status code of a transaction execution.
        """
        transactions = validate_input(transactions_in)
        transactions_dict={}
        for transaction in transactions:
            params = {'module': 'transaction',
                      'action': 'gettxreceiptstatus',
                      'txhah': transaction}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            transactions_dict[transaction] = response
        transactions_df = pd.Series(transactions_dict).to_frame(name='transactions')
        return transactions_df

    ##### Blocks
    # TODO, get pro
    def get_block_reward(self, blocks_in: Union[str, List]) -> pd.DataFrame:
        """Returns the block reward and 'Uncle' block rewards
        """
        blocks = validate_input(blocks_in)
        for block in blocks:
            params = {'module': 'block',
                      'action': 'getblockreward',
                      'blockno': block}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
        return "TODO"

    def get_block_countdown(self, blocks_in: Union[str, List]) -> pd.DataFrame:
        """Returns the estimated time remaining, in seconds, until a certain block is mined
        """
        blocks = validate_input(blocks_in)
        countdown_list=[]
        for block in blocks:
            params = {'module': 'block',
                      'action': 'getblockcountdown',
                      'blockno': block}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)['result']
            countdown_list.append(response)
        countdown_df = pd.DataFrame(countdown_list)
        return countdown_df

    def get_block_by_timestamp(self, times_in: Union[str, List], before: bool=True) -> pd.DataFrame:
        """Returns the block number that was mined at a certain timestamp (in unix)
        """
        closest = 'before' if before else 'after'
        times = validate_input(times_in)
        blocks_list=[]
        for time in times:
            params = {'module': 'block',
                     'action': 'getblocknobytime',
                     'timestamp': time,
                     'closest': closest}
            params.update(self.api_dict)
            response = self.get_response(BASE_URL, params=params)
            blocks_list.append(response)
        blocks_df = pd.DataFrame(blocks_list)
        return blocks_df

    ##### Logs
    # TODO, learn this

    ##### Geth/Parity Proxy
    def get_eth_block_number(self) -> int:
        """Returns the number of most recent block
        """
        return 0

    def get_eth_block(self, blocks_in) -> pd.DataFrame:
        """Returns information about a block by block number
        """
        return "TODO GETH"
    # TODO more

    ##### Tokens
    # TODO pro
    def get_token_total_supply(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Returns the current amount of an ERC-20 token in circulation
        """
        tokens = validate_input(tokens_in)
        supply_dict = {}
        for token in tokens:
            params = {'module': 'stats',
                      'action': 'tokensupply',
                      'contractaddress': token}
            params.update(self.api_dict)
            supply = self.get_response(BASE_URL, params=params)['result']
            supply_dict[token] = supply
        supply_df = pd.Series(supply_dict).to_frame(name='supply')
        return supply_df

    def get_token_account_balance(self, tokens_in: Union[str, List], accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the current balance of an ERC-20 token of an address
        """
        tokens = validate_input(tokens_in)
        accounts = validate_input(accounts_in)
        series_list = []
        for account in accounts:
            token_dict = {}
            for token in tokens:
                params = {'module': 'account',
                          'action': 'tokenbalance',
                          'contractaddress': token,
                          'address': account,
                          'tag': 'latest'}
                params.update(self.api_dict)
                balance = self.get_response(BASE_URL, params=params)['result']
                token_dict[token] = balance
            token_series = pd.Series(token_dict)
            series_list.append(token_series)
        balances_df = pd.concat(series_list, keys=accounts, axis=1)
        return balances_df

    ##### Gas Tracker
    # TODO pro
    def get_est_confirmation(self, gas_price: int) -> int:
        """Returns the estimated time, in seconds, for a transaction to be confirmed on the blockchain
        gas price in wei
        """
        params = {'module': 'gastracker',
                  'action': 'gasestimate',
                  'gasprice': gas_price}
        params.update(self.api_dict)
        response = self.get_response(BASE_URL, params=params)['result']
        return response

    def get_gas_oracle(self) -> pd.DataFrame:
        """Returns the current Safe, Proposed and Fast gas prices
        """
        params = {'module': 'gastracker',
                  'action': 'gasoracle'}
        params.update(self.api_dict)
        response = self.get_response(BASE_URL, params=params)['result']
        oracle_df = pd.Series(response).to_frame(name='gas_oracle')
        return oracle_df

    ##### Stats
    def get_total_eth_supply(self) -> int:
        """Returns the current amount of Ether in circulation.
        """
        params = {'module': 'stats',
                  'action': 'ethsupply'}
        params.update(self.api_dict)
        response = self.get_response(BASE_URL, params=params)['result']
        return response

    def get_total_eth2_supply(self) -> pd.DataFrame:
        """Returns the current amount of Ether in circulation,
        ETH2 Staking rewards and EIP1559 burnt fees statistics
        """
        params = {'module': 'stats',
                  'action': 'ethsupply2'}
        params.update(self.api_dict)
        response = self.get_response(BASE_URL, params=params)['result']
        price_df = pd.Series(response).to_frame(name='eth2_supply')
        return price_df

    def get_last_eth_price(self) -> pd.DataFrame:
        """Returns the latest price of 1 ETH in BTC & USD
        """
        params = {'module': 'stats',
                  'action': 'ethprice'}
        params.update(self.api_dict)
        response = self.get_response(BASE_URL, params=params)['result']
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
        response = self.get_response(BASE_URL, params=params)['result']
        size_df = pd.DateFrame(response)
        return size_df

    def get_total_nodes_count(self) -> int:
        """Returns the total number of discoverable Ethereum nodes
        """
        params = {'module': 'stats',
                  'action': 'nodecount'}
        params.update(self.api_dict)
        nodes_count = self.get_response(BASE_URL, params=params)['result']['TotalNodeCount']
        return nodes_count

import time

## Setup
API_KEY='DWC3QGAEHNFQQM55Z1AYTXUTZ1GPBK51JQ'
es = Etherscan(api_key=API_KEY)
accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12', '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F', '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6', '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc', '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
blocks = ['13188647', '13088500']
tokens = ['0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', '0xc18360217d8f7ab5e7c516566761ea12ce7f9d72']

##### Accounts
#account_balances = es.get_account_ether_balance(accounts)
#print(account_balances)
#print('3 second sleep')
#time.sleep(3)

#account_normal = es.get_account_normal_transactions(accounts)
#print(account_normal)
#print('3 second sleep')
#time.sleep(3)

#account_internal = es.get_account_internal_transactions(accounts)
#print(account_internal)
#print('3 second sleep')
#time.sleep(3)

#int_txn = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'
#transaction_internals = es.get_transaction_internal_transactions(int_txn)
#print(transaction_internals)
#print('3 second sleep')
#time.sleep(3)

#block_range_internals = es.get_block_range_internal_transactions(10000000,10001000)
#print(block_range_internals)
#print('3 second sleep')
#time.sleep(3)

account_token_transfers = es.get_account_token_transfers(accounts)
print(account_token_transfers)
print('3 second sleep')
time.sleep(3)

account_nft_transfers = es.get_account_nft_transfers(accounts)
print(account_nft_transfers)
print('3 second sleep')
time.sleep(3)

# Ethermine pubkey, F2Pool Old pubkey
miners = ['0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8', '0x829BD824B016326A401d083B33D092293333A830']
account_blocks_mined = es.get_account_blocks_mined(miners)
print(account_blocks_mined)
print('3 second sleep')
time.sleep(3)

##### Contracts
abis = es.get_contract_abi(contracts)
print(abis)
print('3 second sleep')
time.sleep(3)

source_code = es.get_contract_source_code(contracts)
print(source_code)
print('3 second sleep')
time.sleep(3)

##### Transactions
contract_execution_status = es.get_contract_execution_status(txns)
print(contract_execution_status)
print('3 second sleep')
time.sleep(3)

transaction_execution_status = es.get_transaction_execution_status(txns)
print(transaction_execution_status)
print('3 second sleep')
time.sleep(3)

##### Blocks
block_rewards = es.get_block_reward(blocks)
print(block_rewards)
print('3 second sleep')
time.sleep(3)

block_countdown = es.get_block_countdown('50000000')
print(block_countdown)
print('3 second sleep')
time.sleep(3)

block_at_time = es.get_block_by_timestamp('1638767557')
print(block_at_time)
print('3 second sleep')
time.sleep(3)

##### Logs
# TODO

##### Geth/Parity Proxy
# TODO

##### Tokens
total_supply = es.get_token_total_supply(tokens)
print(total_supply)
print('3 second sleep')
time.sleep(3)

#pickle, xSushi
t2 = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5', '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
account_balance = es.get_token_account_balance(t2, accounts)
print(account_balance)
print('3 second sleep')
time.sleep(3)

##### Gas Tracker
est_confirmation = es.get_est_confirmation(2000000000)
print(est_confirmation)
print('3 second sleep')
time.sleep(3)

gas_oracle = es.get_gas_oracle()
print(gas_oracle)
print('3 second sleep')
time.sleep(3)

##### Stats
total_eth_supply = es.get_total_eth_supply()
print(total_eth_supply)
print('3 second sleep')
time.sleep(3)

total_eth2_supply = es.get_total_eth2_supply()
print(total_eth2_supply)
print('3 second sleep')
time.sleep(3)

last_eth_price = es.get_last_eth_price()
print(last_eth_price)
print('3 second sleep')
time.sleep(3)

nodes_size = es.get_nodes_size(start_date='2021-01-01', end_date='2021-06-01')
print(nodes_size)
print('3 second sleep')
time.sleep(3)

total_nodes_count = es.get_total_nodes_count()
print(total_nodes_count)
print('3 second sleep')
time.sleep(3)
