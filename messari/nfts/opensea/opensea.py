
"""This module is meant to contain the OpenSea class"""

from messari.dataloader import DataLoader
from messari.utils import validate_input

from string import Template
from typing import Union, List
import pandas as pd


# Reference: https://docs.opensea.io/reference/api-overview
# TODO, api key as header

ASSET_URL = Template('https://api.opensea.io/api/v1/asset/$contract/$id/')
CONTRACT_URL = Template('https://api.opensea.io/api/v1/asset_contract/$contract')
COLLECTION_URL = Template('https://api.opensea.io/api/v1/collection/$collection')

HEADERS = {'Accept': 'application/json'}

class OpenSea(DataLoader):
    """This class is a wrapper around the OpenSea API
    """
    def __init__(self, api_key=None):
        api_dict = None
        if api_key:
            api_dict = {'X-API-KEY': api_key}
        DataLoader.__init__(self, api_dict=api_dict, taxonomy_dict=None)

    def get_asset(self, contracts_in: Union[str, List], assets_in: Union[str, List], account: str=None) -> pd.DataFrame:
        """Used to fetch more in-depth information about an individual asset"""
        params = {}
        if account:
            params['account_address'] = account

        # check api-key to update headers
        if self.api_dict:
            headers = HEADERS | self.api_dict
        else:
            headers = HEADERS

        contracts = validate_input(contracts_in)
        assets = validate_input(assets_in)
        df_list=[]
        for contract in contracts:
            series_list=[]
            for asset in assets:
                endpoint_url = ASSET_URL.substitute(contract=contract, id=asset)
                response = self.get_response(endpoint_url, params=params, headers=headers)

                tmp_series=pd.Series(response)
                series_list.append(tmp_series)
            tmp_df=pd.concat(series_list, keys=assets, axis=1)
            df_list.append(tmp_df)
        assets_df=pd.concat(df_list, keys=contracts, axis=1)
        return assets_df

    def get_contract(self, contracts_in: Union[str, List]) -> pd.DataFrame:
        """Used to fetch more in-depth information about an contract asset"""
        # check api-key to update headers
        if self.api_dict:
            headers = HEADERS | self.api_dict
        else:
            headers = HEADERS

        contracts = validate_input(contracts_in)

        df_list=[]
        for contract in contracts:
            endpoint_url = CONTRACT_URL.substitute(contract=contract)
            response = self.get_response(endpoint_url, headers=headers)
            tmp_df = pd.DataFrame(response)

            df_list.append(tmp_df)
        contracts_df = pd.concat(df_list, keys=contracts, axis=1)
        return contracts_df

    def get_collection(self, collections_in: Union[str, List]) -> pd.DataFrame:
        """Used for retrieving more in-depth information about individual collections,
        including real time statistics like floor price"""
        # check api-key to update headers
        if self.api_dict:
            headers = HEADERS | self.api_dict
        else:
            headers = HEADERS

        collections = validate_input(collections_in)

        df_list=[]
        for collection in collections:
            endpoint_url = COLLECTION_URL.substitute(collection=collection)
            response = self.get_response(endpoint_url, headers=headers)
            tmp_df = pd.DataFrame(response)

            df_list.append(tmp_df)
        collections_df = pd.concat(df_list, keys=collections, axis=1)
        return collections_df

    def get_events(self) -> pd.DataFrame:
        """provides a list of events that occur on the assets that OpenSea tracks"""
        # check api-key to update headers
        if self.api_dict:
            headers = HEADERS | self.api_dict
        else:
            headers = HEADERS
        return

    def get_bundle(self) -> pd.DataFrame:
        """Bundles are groups of items for sale on OpenSea.
        You can buy them all at once in one transaction,
        and you can create them without any transactions or gas,
        as long as you've already approved the assets inside."""
        # check api-key to update headers
        if self.api_dict:
            headers = HEADERS | self.api_dict
        else:
            headers = HEADERS
        return

    def get_collection_stats(self) -> pd.DataFrame:
        """fetch stats for a specific collection, including realtime floor price statistics"""
        # check api-key to update headers
        if self.api_dict:
            headers = HEADERS | self.api_dict
        else:
            headers = HEADERS
        return

    def get_orders(self) -> pd.DataFrame:
        """fetch orders from the OpenSea system"""
        # check api-key to update headers
        if self.api_dict:
            headers = HEADERS | self.api_dict
        else:
            headers = HEADERS
        return
