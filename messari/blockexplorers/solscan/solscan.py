"""This module is meant to contain the Solscan class"""

from messari.dataloader import DataLoader
from messari.utils import validate_input
from string import Template
from typing import Union, List, Dict
from .helpers import unpack_dataframe_of_dicts
import pandas as pd

#### Block
BLOCK_LAST_URL = 'https://public-api.solscan.io/block/last'
BLOCK_TRANSACTIONS_URL = 'https://public-api.solscan.io/block/transactions'
BLOCK_BLOCK_URL = Template('https://public-api.solscan.io/block/$block')
#### Transaction
TRANSACTION_LAST_URL = 'https://public-api.solscan.io/transaction/last'
TRANSACTION_SIGNATURE_URL = Template('https://public-api.solscan.io/transaction/$signature')
#### Account
ACCOUNT_TOKENS_URL = 'https://public-api.solscan.io/account/tokens'
ACCOUNT_TRANSACTIONS_URL = 'https://public-api.solscan.io/account/transactions'
ACCOUNT_STAKE_URL = 'https://public-api.solscan.io/account/stakeAccounts'
ACCOUNT_SPL_TXNS_URL = 'https://public-api.solscan.io/account/splTransfers'
ACCOUNT_SOL_TXNS_URL = 'https://public-api.solscan.io/account/solTransfers'
ACCOUNT_EXPORT_TXNS_URL = 'https://public-api.solscan.io/account/exportTransactions'
ACCOUNT_ACCOUNT_URL = Template('https://public-api.solscan.io/account/$account')
#### Token
TOKEN_HOLDERS_URL = 'https://public-api.solscan.io/token/holders'
TOKEN_META_URL = 'https://public-api.solscan.io/token/meta'
TOKEN_LIST_URL = 'https://public-api.solscan.io/token/list'
#### Market
MARKET_INFO_URL = Template('https://public-api.solscan.io/market/token/$tokenAddress')
#### Chain Information
CHAIN_INFO_URL = 'https://public-api.solscan.io/chaininfo'

#TODO max this clean/ not hardcoded? look into how this works
HEADERS={'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'} # pylint: disable=line-too-long

class Solscan(DataLoader):
    """This class is a wrapper around the Solscan API
    """

    def __init__(self):
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)

    #################
    # Block endpoints
    def get_last_blocks(self, num_blocks=1) -> pd.DataFrame:
        """returns info for last blocks (default is 1, limit is 20)

        Parameters
        ----------
            num_blocks: int (default is 1)
                number of blocks to return, max is 20

        Returns
        -------
            DataFrame
                DataFrame with block information
        """

        # Max value is 20 or API bricks
        limit=num_blocks if num_blocks < 21 else 20
        params = {'limit': limit}

        last_blocks = self.get_response(BLOCK_LAST_URL,
                                        params=params,
                                        headers=HEADERS)
        last_blocks_df = pd.DataFrame(last_blocks)
        last_blocks_df.set_index('currentSlot', inplace=True)
        last_blocks_df = unpack_dataframe_of_dicts(last_blocks_df)

        # TODO, extract data from 'result'

        return last_blocks_df

    def get_block_last_transactions(self, blocks_in: Union[str, List],
                               offset=0, num_transactions=10) -> pd.DataFrame:
        """get last num_transactions of given block numbers

        Parameters
        ----------
            blocks_in: str, List
                single block in or list of blocks in
            num_transactions: int (default is 10)
                number of transactions to return

        Returns
        -------
            DataFrame
                dataframe with transaction details
        """
        blocks = validate_input(blocks_in)

        df_list = []
        for block in blocks:
            params = {'block': block,
                      'offset': offset,
                      'limit': num_transactions}
            txns = self.get_response(BLOCK_TRANSACTIONS_URL,
                                         params=params,
                                         headers=HEADERS)
            txns_df = pd.DataFrame(txns)
            df_list.append(txns_df)
        fin_df = pd.concat(df_list, keys=blocks, axis=1)
        fin_df = unpack_dataframe_of_dicts(fin_df)

        return fin_df

    def get_block(self, blocks_in: Union[str, List]) -> pd.DataFrame:
        """Return information of given block(s)

        Parameters
        ----------
            blocks_in: str, List
                single block in or list of blocks in

        Returns
        -------
            DataFrame
                DataFrame with block information
        """
        blocks = validate_input(blocks_in)

        df_list = []
        for block in blocks:
            endpoint_url = BLOCK_BLOCK_URL.substitute(block=block)
            response = self.get_response(endpoint_url,
                                         headers=HEADERS)
            df = pd.DataFrame(response)
            df.drop('currentSlot', axis=1)
            df_list.append(df)
        fin_df = pd.concat(df_list, keys=blocks, axis=1)
        fin_df = fin_df.xs('result', axis=1, level=1)
        return fin_df


    #######################
    # Transaction endpoints
    def get_last_transactions(self, num_transactions=10) -> pd.DataFrame:
        """Return last num_transactions transactions

        Parameters
        ----------
            num_transactions: int (default is 10)
                number of transactions to return, limit is 20

        Returns
        -------
            DataFrame
                dataframe with transaction details
        """
        # 20
        limit=num_transactions if num_transactions < 21 else 20
        params = {'limit': limit}
        response = self.get_response(TRANSACTION_LAST_URL,
                                    params=params,
                                    headers=HEADERS)
        df = pd.DataFrame(response)
        fin_df = unpack_dataframe_of_dicts(df)
        return fin_df


    def get_transaction(self, signatures_in: Union[str, List]) -> pd.DataFrame:
        """Return information of given transaction signature(s)

        Parameters
        ----------
            signatures_in: str, List
                single signature in or list of signatures in

        Returns
        -------
            DataFrame
                DataFrame with transaction details
        """
        signatures = validate_input(signatures_in)

        series_list = []
        for signature in signatures:
            endpoint_url = TRANSACTION_SIGNATURE_URL.substitute(signature=signature)
            response = self.get_response(endpoint_url,
                                        headers=HEADERS)
            #print(response)
            series = pd.Series(response)
            series_list.append(series)
        fin_df = pd.concat(series_list, keys=signatures, axis=1)
        return fin_df

    ###################
    # Account endpoints
    def get_account_tokens(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Return token balances of the given account(s)

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame with token balances of given accounts
        """
        accounts = validate_input(accounts_in)

        df_list=[]
        for account in accounts:
            params={'account':account}
            response = self.get_response(ACCOUNT_TOKENS_URL,
                                         params=params,
                                         headers=HEADERS)
            df = pd.DataFrame(response)
            df_list.append(df)
        fin_df = pd.concat(df_list, keys=accounts, axis=1)
        return fin_df

    def get_account_transactions(self, accounts_in: Union[str,List]) -> pd.DataFrame:
        """Return DataFrame of transactions of the given account(s)

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame with transactions of given accounts
        """
        accounts = validate_input(accounts_in)

        df_list=[]
        for account in accounts:
            params={'account':account}
            response = self.get_response(ACCOUNT_TRANSACTIONS_URL,
                                         params=params,
                                         headers=HEADERS)
            df = pd.DataFrame(response)
            df_list.append(df)
        fin_df = pd.concat(df_list, keys=accounts, axis=1)
        return fin_df

    def get_account_stake(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Get staking accounts of the given account(s)

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in

        Returns
        -------
            DataFrame
                DataFrame with staking accounts of given accounts
        """
        accounts = validate_input(accounts_in)

        df_list=[]
        for account in accounts:
            params={'account':account}
            response = self.get_response(ACCOUNT_STAKE_URL,
                                         params=params,
                                         headers=HEADERS)
            df = pd.DataFrame(response)
            df_list.append(df)
        fin_df = pd.concat(df_list, keys=accounts, axis=1)
        return fin_df

    def get_account_spl_transactions(self, accounts_in: Union[str, List],
                                     from_time: int=None,
                                     to_time: int=None,
                                     offset: int=0,
                                     limit: int=10) -> pd.DataFrame:
        """Return SPL transfers for given account(s)

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in
            from_time: int
                unix time to start transaction history
            to_time: int
                unix time to end transaction history
            offset: int
                Offset starting at 0. Increment value to offset paginated results
            limit: int
                Limit of assets to return. Default is 10

        Returns
        -------
            DataFrame
                DataFrame with SPL transfers for given account(s)
        """
        accounts = validate_input(accounts_in)

        df_list=[]
        for account in accounts:
            params={'account':account,
                    'toTime': to_time,
                    'fromTime': from_time,
                    'offset': offset,
                    'limit': limit}
            response = self.get_response(ACCOUNT_SPL_TXNS_URL,
                                         params=params,
                                         headers=HEADERS)
            df = pd.DataFrame(response)
            df.drop('total', axis=1)
            df_list.append(df)
        fin_df = pd.concat(df_list, keys=accounts, axis=1)
        fin_df = unpack_dataframe_of_dicts(fin_df)
        return fin_df

    def get_account_sol_transactions(self, accounts_in: Union[str, List],
                                     from_time: int=None,
                                     to_time: int=None,
                                     offset: int=0,
                                     limit: int=10) -> pd.DataFrame:
        """Return SOL transfers for given account(s)

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in
            from_time: int
                unix time to start transaction history
            to_time: int
                unix time to end transaction history
            offset: int
                Offset starting at 0. Increment value to offset paginated results
            limit: int
                Limit of assets to return. Default is 10

        Returns
        -------
            DataFrame
                DataFrame with SOL transfers for given account(s)
        """
        accounts = validate_input(accounts_in)

        df_list=[]
        for account in accounts:
            params={'account':account,
                    'toTime': to_time,
                    'fromTime': from_time,
                    'offset': offset,
                    'limit': limit}
            response = self.get_response(ACCOUNT_SOL_TXNS_URL,
                                         params=params,
                                         headers=HEADERS)
            df = pd.DataFrame(response)
            df_list.append(df)
        fin_df = pd.concat(df_list, keys=accounts, axis=1)
        fin_df = unpack_dataframe_of_dicts(fin_df)
        return fin_df

    def get_account_export_transactions(self, accounts_in: Union[str, List],
                                        type_in: str, from_time: int, to_time: int) -> List[str]:
        """Export transactions to CSV style string

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in
            type_in: str
                what type of transactions to export:
                    - tokenchange
                    - soltransfer
                    - all
            from_time: int
                unix time to start transaction history
            to_time: int
                unix time to end transaction history

        Returns
        -------
            List[str]
                list of strings to make csv document
        """
        accounts = validate_input(accounts_in)
        csv_list=[]
        for account in accounts:
            params={'account': account,
                    'type': type_in,
                    'fromTime': from_time,
                    'toTime': to_time}
            # NOTE: need to do this to not return json
            response = self.session.get(ACCOUNT_EXPORT_TXNS_URL, params=params, headers=HEADERS)
            csv = response.content.decode('utf-8')
            csv_list.append(csv)
        return csv_list

    def get_account(self, accounts_in: Union[str, List]) -> pd.DataFrame:
        """Return overall account(s) information, including program account,
        NFT metadata information

        Parameters
        ----------
            accounts_in: str, List
                single account in or list of accounts in
        Returns
        -------
            DataFrame
                DataFrame with account info
        """
        accounts = validate_input(accounts_in)
        series_list = []
        for account in accounts:
            endpoint_url = ACCOUNT_ACCOUNT_URL.substitute(account=account)
            response = self.get_response(endpoint_url,
                                         headers=HEADERS)
            series = pd.Series(response)
            series_list.append(series)
        fin_df = pd.concat(series_list, keys=accounts, axis=1)
        return fin_df

    #################
    # Token endpoints
    def get_token_holders(self, tokens_in: Union[str, List],
                          limit: int=10, offset: int=0) -> pd.DataFrame:
        """Return top token holders for given token(s)

        Parameters
        ----------
            tokens_in: str, List
                single token address in or list of token addresses, used to filter results
            offset: int
                Offset starting at 0. Increment value to offset paginated results
            limit: int
                Limit of assets to return. Default is 10

        Returns
        -------
            DataFrame
                DataFrame with top token holders
        """
        tokens = validate_input(tokens_in)

        df_list = []
        for token in tokens:
            params={'tokenAddress': token,
                    'limit': limit,
                    'offset': offset}
            response = self.get_response(TOKEN_HOLDERS_URL,
                                         params=params,
                                         headers=HEADERS)
            df = pd.DataFrame(response)
            df.drop('total', axis=1)
            df_list.append(df)
        fin_df = pd.concat(df_list, keys=tokens, axis=1)
        fin_df = unpack_dataframe_of_dicts(fin_df)
        return fin_df

    def get_token_meta(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Return metadata of given token(s)

        Parameters
        ----------
            tokens_in: str, List
                single token address in or list of token addresses, used to filter results

        Returns
        -------
            DataFrame
                DataFrame with token metadata
        """
        tokens = validate_input(tokens_in)

        series_list = []
        for token in tokens:
            params={'tokenAddress': token}
            response = self.get_response(TOKEN_META_URL,
                                         params=params,
                                         headers=HEADERS)
            series = pd.Series(response)
            series_list.append(series)
        fin_df = pd.concat(series_list, keys=tokens, axis=1)
        return fin_df

    def get_token_list(self, sort_by: str='market_cap', ascending: bool=True,
                       limit: int=10, offset: int=0) -> pd.DataFrame:
        """Returns DataFrame of tokens

        Parameters
        ----------
            sort_by: str (default 'market_cap')
                how to sort results, options are:
                    - market_cap
                    - volume
                    - holder
                    - price
                    - price_change_24h
                    - price_change_7d
                    - price_change_14d
                    - price_change_30d
                    - price_change_60d
                    - price_change_200d
                    - price_change_1y
            offset: int
                Offset starting at 0. Increment value to offset paginated results
            limit: int
                Limit of assets to return. Default is 10
            ascending: bool
                return results ascending or descending (default True)

        Returns
        -------
            DataFrame
                DataFrame with tokens
        """
        direction = 'asc' if ascending else 'desc'
        params={'sortBy': sort_by,
                'direction': direction,
                'limit': limit,
                'offset': offset}
        response = self.get_response(TOKEN_LIST_URL,
                                     params=params,
                                     headers=HEADERS)
        token_list_df = pd.DataFrame(response['data'])
        return token_list_df

    ##################
    # Market endpoints
    def get_market_info(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Get market information of the given token

        Parameters
        ----------
            tokens_in: str, List
                single token address in or list of token addresses

        Returns
        -------
            DataFrame
                DataFrame containing market info for token(s)
        """
        tokens = validate_input(tokens_in)

        market_info_list = []
        for token in tokens:
            endpoint_url = MARKET_INFO_URL.substitute(tokenAddress=token)
            market_info = self.get_response(endpoint_url,
                                            headers=HEADERS)
            market_info_series = pd.Series(market_info)
            market_info_list.append(market_info_series)
        market_info_df = pd.concat(market_info_list, keys=tokens, axis=1)
        return market_info_df


    #############################
    # Chain Information endpoints
    def get_chain_info(self) -> Dict:
        """Return Blockchain overall information

        Returns
        -------
            Dict
                Information about Solana blockchain
        """
        chain_info = self.get_response(CHAIN_INFO_URL,
                                       headers=HEADERS)
        chain_info_df = pd.Series(chain_info).to_frame(name='chain_info')
        return chain_info_df
