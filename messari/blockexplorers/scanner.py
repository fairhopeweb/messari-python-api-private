"""This module is meant to contain the Scanner class"""

from typing import Union, List, Dict
import pandas as pd

from messari.dataloader import DataLoader
from messari.utils import validate_input, validate_int
from .helpers import int_to_hex

# Refrence: https://docs.etherscan.io/
class Scanner(DataLoader):
    """This class is a wrapper around the blockexplorer APIs
    """

    def __init__(self, base_url: str, api_key: str=None):
        self.base_url = base_url
        api_dict = {'apikey': api_key}
        DataLoader.__init__(self, api_dict=api_dict, taxonomy_dict={})

    ##### Accounts
    def get_account_native_balance(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the native token balance of a given address

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame containing accounts_in native (sol) balance
        """
        accounts = validate_input(accounts_in)
        balance_dict={}
        for account in accounts:
            params = {'module': 'account',
                      'action': 'balance',
                      'address': account,
                      'tag': 'latest'}
            params.update(self.api_dict)
            balance = self.get_response(self.base_url, params=params)['result']
            balance_dict[account] = balance
        balances_df = pd.Series(balance_dict).to_frame(name='balances')
        return balances_df

    def get_account_normal_transactions(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the list of transactions performed by an address, with optional pagination

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame containing accounts_in normal transactions
        """
        # TODO paging
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'txlist',
                      'address': account}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        account_transactions_df = pd.concat(df_list, keys=accounts, axis=1)
        return account_transactions_df

    def get_account_internal_transactions(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the list of internal transactions performed by an address

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame with internal transactions performed in given account(s)
        """
        # TODO paging
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'txlistinternal',
                      'address': account}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        account_transactions_df = pd.concat(df_list, keys=accounts, axis=1)
        return account_transactions_df

    def get_transaction_internal_transactions(self,
                                              transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the list of internal transactions performed within a transaction
        Parameters
        ----------
            transactions_in: str, List
                single transaction in or list of transactions in

        Returns
        -------
            DataFrame
                DataFrame with internal transactions performed in given transaction(s)
        """
        transactions = validate_input(transactions_in)
        df_list=[]
        for transaction in transactions:
            params = {'module': 'account',
                      'action': 'txlistinternal',
                      'txhash': transaction}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        transactions_df = pd.concat(df_list, keys=transactions, axis=1)
        return transactions_df

    def get_block_range_internal_transactions(self, start_block: int, end_block: int, page: int=0,
                                              offset: int=0, ascending:bool=True) -> pd.DataFrame:
        """Returns the list of internal transactions performed within a block range
        Parameters
        ----------
            start_block: int
                block to start search
            end_block: int
                block to end search
            page: int
                Page number starting at 0. Increment value to paginate through results
            offset: int
                Offset starting at 0. Increment value to offset paginated results
            ascending: bool
                return results ascending or descending (default True)

        Returns
        -------
            DataFrame
                DataFrame with internal transactions for a given block range
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
        response = self.get_response(self.base_url, params=params)['result']
        transactions_df = pd.DataFrame(response)
        return transactions_df

    def get_account_token_transfers(self, accounts_in: Union[str, List],
                                    tokens_in: Union[str, List]=None,
                                    start_block: int=None, end_block: int=None,
                                    page:int=0, offset:int=0,
                                    ascending:bool=True) -> pd.DataFrame:
        """Returns the list of ERC-20 tokens transferred by an address,
        with optional filtering by token contract

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in
            tokens_in: str, List
                single token address in or list of token addresses, used to filter results
            start_block: int
                block to start search
            end_block: int
                block to end search
            page: int
                Page number starting at 0. Increment value to paginate through results
            offset: int
                Offset starting at 0. Increment value to offset paginated results
            ascending: bool
                return results ascending or descending (default True)

        Returns
        -------
            DataFrame
                DataFrame with token transfers for given account(s)
        """
        sort = 'asc' if ascending else 'desc'
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'tokentx',
                      'sort': sort,
                      'page': page,
                      'offset': offset,
                      'address': account}
            if start_block:
                params.update({'startblock': str(start_block)})
            if end_block:
                params.update({'endblock': str(start_block)})
            params.update(self.api_dict)


            # iterate through optional token filters
            response=[]
            if tokens_in:
                tokens = validate_input(tokens_in)
                for token in tokens:
                    params['contractaddress'] = token
                    response += self.get_response(self.base_url, params=params)['result']
            else:
                response = self.get_response(self.base_url, params=params)['result']

            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        token_transfers_df = pd.concat(df_list, keys=accounts, axis=1)
        return token_transfers_df

    def get_account_nft_transfers(self, accounts_in: Union[str, List],
                                  nfts_in: Union[str, List]=None,
                                  start_block: int=None, end_block: int=None,
                                  page:int=0, offset:int=0, ascending:bool=True) -> pd.DataFrame:
        """Returns the list of ERC-721 ( NFT ) tokens transferred by an address,
        with optional filtering by token contract

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in
            nfts_in: str, List
                single nft in or list of nfts in, used to filter results
            start_block: int
                block to start search
            end_block: int
                block to end search
            page: int
                Page number starting at 0. Increment value to paginate through results
            offset: int
                Offset starting at 0. Increment value to offset paginated results
            ascending: bool
                return results ascending or descending (default True)

        Returns
        -------
            DataFrame
                DataFrame with NFT transfers for given account(s)
        """
        sort = 'asc' if ascending else 'desc'
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'tokennfttx',
                      'sort': sort,
                      'page': page,
                      'offset': offset,
                      'address': account}
            if start_block:
                params.update({'startblock': start_block})
            if end_block:
                params.update({'endblock': start_block})
            params.update(self.api_dict)


            # iterate through optional token filters
            response=[]
            if nfts_in:
                nfts = validate_input(nfts_in)
                for nft in nfts:
                    params['contractaddress'] = nft
                    response += self.get_response(self.base_url, params=params)['result']
            else:
                response = self.get_response(self.base_url, params=params)['result']


            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        nft_transfers_df = pd.concat(df_list, keys=accounts, axis=1)
        return nft_transfers_df

    # NOTE: this is the same as blocks validated on PoS chains
    def get_account_blocks_mined(self, accounts_in: Union[str, List], block_type:str='blocks',
                                 page:int=0, offset:int=0) -> pd.DataFrame:
        """Returns the list of blocks mined by an address

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in
            page: int
                Page number starting at 0. Increment value to paginate through results
            offset: int
                Offset starting at 0. Increment value to offset paginated results

        Returns
        -------
            DataFrame
                DataFrame with blocks mined by given account(s)
        """
        accounts = validate_input(accounts_in)
        df_list=[]
        for account in accounts:
            params = {'module': 'account',
                      'action': 'getminedblocks',
                      'blocktype': block_type,
                      'page': page,
                      'offset': offset,
                      'address': account}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        blocks_mined_df = pd.concat(df_list, keys=accounts, axis=1)
        return blocks_mined_df

    ##### Contracts
    def get_contract_abi(self, contracts_in: Union[str, List]) -> Dict:
        """Returns the Contract Application Binary Interface (ABI) of a verified smart contract

        Parameters
        ----------
            contracts_in: str, List
                single contract in or list of contracts in

        Returns
        -------
            Dict
                Dictionary with {contract: contract_abi}
        """
        contracts = validate_input(contracts_in)
        abi_dict = {}
        for contract in contracts:
            params = {'module': 'contract',
                      'action': 'getabi',
                      'address': contract}
            params.update(self.api_dict)
            abi = self.get_response(self.base_url, params=params)['result']
            abi_dict[contract] = abi
        return abi_dict

    def get_contract_source_code(self, contracts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the Solidity source code of a verified smart contract

        Parameters
        ----------
            contracts_in: str, List
                single contract in or list of contracts in

        Returns
        -------
            DataFrame
                DataFrame with contract source code
        """
        contracts = validate_input(contracts_in)
        df_list=[]
        for contract in contracts:
            params = {'module': 'contract',
                      'action': 'getsourcecode',
                      'address': contract}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        source_df = pd.concat(df_list, keys=contracts, axis=1)
        return source_df

    ##### Transactions
    def get_contract_execution_status(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the status code of a contract execution

        Parameters
        ----------
            transactions_in: str, List
                single transaction in or list of transactions in

        Returns
        -------
            DataFrame
                DataFrame with contract execution status
        """
        transactions = validate_input(transactions_in)
        transactions_dict={}
        for transaction in transactions:
            params = {'module': 'transaction',
                      'action': 'getstatus',
                      'txhah': transaction}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            transactions_dict[transaction] = response
        transactions_df = pd.Series(transactions_dict).to_frame(name='transactions')
        return transactions_df

    def get_transaction_execution_status(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the status code of a transaction execution.

        Parameters
        ----------
            transactions_in: str, List
                single transaction in or list of transactions in

        Returns
        -------
            DataFrame
                DataFrame with transaction execution status
        """
        transactions = validate_input(transactions_in)
        transactions_dict={}
        for transaction in transactions:
            params = {'module': 'transaction',
                      'action': 'gettxreceiptstatus',
                      'txhah': transaction}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            transactions_dict[transaction] = response
        transactions_df = pd.Series(transactions_dict).to_frame(name='transactions')
        return transactions_df

    ##### Blocks
    # TODO, get pro
    def get_block_reward(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Returns the block reward and 'Uncle' block rewards

        Parameters
        ----------
            blocks_in: int, List
                single block in or list of blocks in

        Returns
        -------
            DataFrame
                DataFrame with block reward(s)
        """
        blocks = validate_int(blocks_in)
        series_list = []
        for block in blocks:
            params = {'module': 'block',
                      'action': 'getblockreward',
                      'blockno': block}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            block_reward_series = pd.Series(response)
            series_list.append(block_reward_series)
        reward_df = pd.concat(series_list, keys=blocks, axis=1)
        return reward_df

    def get_block_countdown(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Returns the estimated time remaining, in seconds, until a certain block is mined

        Parameters
        ----------
            blocks_in: int, List
                single block in or list of blocks in

        Returns
        -------
            DataFrame
                DataFrame with time(s) remaining until block confirmation
        """
        blocks = validate_int(blocks_in)
        countdown_list=[]
        for block in blocks:
            params = {'module': 'block',
                      'action': 'getblockcountdown',
                      'blockno': block}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            countdown_list.append(response)
        countdown_df = pd.DataFrame(countdown_list)
        return countdown_df

    def get_block_by_timestamp(self, times_in: Union[int, List], before: bool=True) -> pd.DataFrame:
        """Returns the block number that was mined at a certain timestamp (in unix)

        Parameters
        ----------
            timess_in: int, List
                single time in or list of times in as unix timestamp(s)
            before: bool (default True)
                Return block immediately before or after given times_in

        Returns
        -------
            DataFrame
                DataFrame with block number(s) closest to times_in
        """
        closest = 'before' if before else 'after'
        times = validate_int(times_in)
        blocks_list=[]
        for time in times:
            params = {'module': 'block',
                     'action': 'getblocknobytime',
                     'timestamp': time,
                     'closest': closest}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            blocks_list.append(response)
        blocks_df = pd.DataFrame(blocks_list)
        return blocks_df

    ##### Logs
    def get_logs(self, address: str,
                 from_block: Union[int, str],
                 to_block: Union[int, str]='latest',
                 topic0: str=None, topic1: str=None,
                 topic2: str=None, topic3: str=None,
                 topic0_1_opr: str=None, topic1_2_opr: str=None,
                 topic2_3_opr: str=None, topic0_2_opr: str=None,
                 topic0_3_opr: str=None, topic1_3_opr: str=None) -> pd.DataFrame:
        """This function is a wrapper around the Etherscan API which is a wrapper
        around the native eth_getLogs. Please check out their documentation for a
        more in depth explanation: https://docs.etherscan.io/api-endpoints/logs"""

        params = {'module': 'logs',
                  'action': 'getlogs',
                  'toBlock': to_block,
                  'fromBlock': from_block,
                  'address': address}
        params.update(self.api_dict)

        # topics
        if topic0:
            params['topic0'] = topic0
        if topic1:
            params['topic1'] = topic1
        if topic2:
            params['topic2'] = topic2
        if topic3:
            params['topic3'] = topic3

        # operators
        valid = ['and', 'or']
        if topic0_1_opr in valid:
            params['topic0_1_opr'] = topic0_1_opr
        if topic1_2_opr in valid:
            params['topic1_2_opr'] = topic1_2_opr
        if topic2_3_opr in valid:
            params['topic2_3_opr'] = topic2_3_opr
        if topic0_2_opr in valid:
            params['topic0_2_opr'] = topic0_2_opr
        if topic0_3_opr in valid:
            params['topic0_3_opr'] = topic0_3_opr
        if topic1_3_opr in valid:
            params['topic1_3_opr'] = topic1_3_opr

        logs = self.get_response(self.base_url, params=params)['result']
        logs_df = pd.DataFrame(logs)
        return logs_df

    ##### Geth/Parity Proxy
    def get_eth_block_number(self) -> int:
        """Returns the number of most recent block

        Returns
        -------
            int
                Number of the most recent block
        """
        params = {'module': 'proxy',
                  'action': 'eth_blockNumber'}
        params.update(self.api_dict)
        block_num_hex = self.get_response(self.base_url, params=params)['result']
        block_num = int(block_num_hex, 16)
        return block_num

    def get_eth_block(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Returns information about a block by block number

        Parameters
        ----------
            blocks_in: int, List
                single block in or list of blocks in

        Returns
        -------
            DataFrame
                DataFrame containing information about block(s)
        """
        blocks = validate_int(blocks_in)
        blocks_hex = int_to_hex(blocks)

        series_list = []
        for block in blocks_hex:
            params = {'module': 'proxy',
                      'action': 'eth_getBlockByNumber',
                      'tag': block,
                      'boolean': 'true'}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            block_series = pd.Series(response)
            series_list.append(block_series)
        series_df = pd.concat(series_list, keys=blocks, axis=1)
        return series_df

    def get_eth_uncle(self, block: int, index: int) -> Dict:
        """Returns information about an uncle by block number and index

        Parameters
        ----------
            block: int
                single block in
            index: int
                single index in

        Returns
        -------
            Dict
                Information about an uncle by block number and index
        """
        block_hex = int_to_hex(block)[0]
        index_hex = int_to_hex(index)[0]

        params = {'module': 'proxy',
                  'action': 'eth_getUncleByBlockNumberAndIndex',
                  'tag': block_hex,
                  'index': index_hex}
        #print(params)
        params.update(self.api_dict)

        response = self.get_response(self.base_url, params=params)['result']
        return response

    def get_eth_block_transaction_count(self, blocks_in: Union[int, List]) -> pd.DataFrame:
        """Returns the number of transactions in a block

        Parameters
        ----------
            blocks_in: int, List
                single block in or list of blocks in

        Returns
        -------
            DataFrame
                DataFrame containing transaction count(s) for the given block(s)
        """
        blocks = validate_int(blocks_in)
        blocks_hex = int_to_hex(blocks)
        count_dict={}
        for block in blocks_hex:
            params = {'module': 'proxy',
                      'action': 'eth_getBlockTransactionCountByNumber',
                      'tag': block}
            params.update(self.api_dict)
            count = self.get_response(self.base_url, params=params)['result']
            count_int = int(count, 16)
            count_dict[block] = count_int
        count_df = pd.Series(count_dict).to_frame(name='transaction_count')
        return count_df

    def get_eth_transaction_by_hash(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the information about a transaction requested by transaction hash

        Parameters
        ----------
            transactions_in: str, List
                single contract in or list of transactions in

        Returns
        -------
            DataFrame
                DataFrame containing transaction details
        """
        transactions = validate_input(transactions_in)
        series_list=[]
        for transaction in transactions:
            params = {'module': 'proxy',
                      'action': 'eth_getTransactionByHash',
                      'txhash': transaction}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            tmp_series = pd.Series(response)
            series_list.append(tmp_series)
        transactions_df = pd.concat(series_list, keys=transactions, axis=1)
        return transactions_df

    def get_eth_transaction_by_block_index(self, block: int, index: int) -> pd.DataFrame:
        """Returns information about a transaction by block number and transaction index position

        Parameters
        ----------
            blocks: int
                single block in

        Returns
        -------
            DataFrame
                DataFrame containing transaction details
        """
        block_hex = int_to_hex(block)[0]
        index_hex = int_to_hex(index)[0]

        params = {'module': 'proxy',
                  'action': 'eth_getTransactionByBlockNumberAndIndex',
                  'tag': block_hex,
                  'index': index_hex}
        params.update(self.api_dict)

        response = self.get_response(self.base_url, params=params)['result']
        txn_df = pd.Series(response).to_frame(name='transaction_info')
        return txn_df

    def get_eth_account_transaction_count(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the number of transactions performed by an address

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame containing transaction count(s) for the given account(s)
        """
        accounts = validate_input(accounts_in)
        count_dict={}
        for account in accounts:
            params = {'module': 'proxy',
                      'action': 'eth_getTransactionCount',
                      'address': account,
                      'tag': 'latest'}
            params.update(self.api_dict)
            count = self.get_response(self.base_url, params=params)['result']
            count_int = int(count, 16)
            count_dict[account] = count_int
        count_df = pd.Series(count_dict).to_frame(name='transaction_count')
        return count_df

    def get_eth_transaction_receipt(self, transactions_in: Union[str, List]) -> pd.DataFrame:
        """Returns the receipt of a transaction by transaction hash

        Parameters
        ----------
            transactions_in: str, List
                single contract in or list of transactions in

        Returns
        -------
            DataFrame
                DataFrame with transaction receipts
        """
        transactions = validate_input(transactions_in)
        df_list=[]
        for transaction in transactions:
            params = {'module': 'proxy',
                      'action': 'eth_getTransactionReceipt',
                      'txhash': transaction}
            params.update(self.api_dict)
            response = self.get_response(self.base_url, params=params)['result']
            tmp_df = pd.DataFrame(response)
            df_list.append(tmp_df)
        transactions_df = pd.concat(df_list, keys=transactions, axis=1)
        return transactions_df

    def get_eth_gas_price(self) -> int:
        """Returns the current price per gas in wei

        Returns
        -------
            int
                Current price per gas in wei
        """
        params = {'module': 'proxy',
                  'action': 'eth_gasPrice'}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        gas_price = int(response, 16)
        return gas_price

    ##### Tokens
    def get_token_total_supply(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Returns the current amount of an ERC-20 token in circulation

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
                      'action': 'tokensupply',
                      'contractaddress': token}
            params.update(self.api_dict)
            supply = self.get_response(self.base_url, params=params)['result']
            supply_dict[token] = supply
        supply_df = pd.Series(supply_dict).to_frame(name='supply')
        return supply_df

    def get_token_account_balance(self, tokens_in: Union[str, List],
                                  accounts_in: Union[str, List]) -> pd.DataFrame:
        """Returns the current balance of an ERC-20 token of an address

        Parameters
        ----------
            tokens_in: str, List
                single token address in or list of token addresses
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame containing token balance(s) for given account(s)
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
                balance = self.get_response(self.base_url, params=params)['result']
                token_dict[token] = balance
            token_series = pd.Series(token_dict)
            series_list.append(token_series)
        balances_df = pd.concat(series_list, keys=accounts, axis=1)
        return balances_df

    ##### Gas Tracker
    def get_est_confirmation(self, gas_price: int) -> int:
        """Returns the estimated time, in seconds,
        for a transaction to be confirmed on the blockchain
        gas price in wei

        Parameters
        ----------
            gas_price: int
                Gas price (in Wei) used for transaction

        Returns
        -------
            int
                The estimated time (in seconds) for a transaction to be confirmed
        """
        params = {'module': 'gastracker',
                  'action': 'gasestimate',
                  'gasprice': gas_price}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        return int(response)

    def get_gas_oracle(self) -> pd.DataFrame:
        """Returns the current Safe, Proposed and Fast gas prices

        Returns
        -------
            DataFrame
                DataFrame containing the current Safe, Proposed and Fast gas prices
        """
        params = {'module': 'gastracker',
                  'action': 'gasoracle'}
        params.update(self.api_dict)
        response = self.get_response(self.base_url, params=params)['result']
        oracle_df = pd.Series(response).to_frame(name='gas_oracle')
        return oracle_df
