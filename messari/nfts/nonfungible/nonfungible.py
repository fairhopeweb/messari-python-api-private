"""This module is meant to contain the NonFungible class"""

from messari.dataloader import DataLoader
from messari.utils import validate_input, validate_int
from typing import Union, List
from string import Template

import pandas as pd

COLLECTION_HISTORY_URL = Template('https://nonfungible.com/api/v4/market/history/$collection?filter=%5B%7B%22id%22%3A%22blockTimestamp%22%2C%22value%22%3A%5B%222021-12-28T16%3A09%3A42.206Z%22%5D%7D%5D&sort=%5B%7B%22id%22%3A%22usdPrice%22%2C%22desc%22%3Atrue%7D%5D')
COLLECTION_STATS_URL = Template('https://nonfungible.com/api/v4/market/statistic/project/$collection/7/count-sale,count-salesprimary,count-salessecondary,sum-usd,avg-usd,sum-usdprimary,sum-usdsecondary,sum-feeusd,unique-wallets,unique-buyer,unique-seller/latest,daily')
COLLECTION_SUMMARY_URL = Template('https://nonfungible.com/api/v4/market/summary/$collection')


class NonFungible(DataLoader):
    """This class is a wrapper around the NonFungible API
    """
    def __init__(self):
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)

    def get_collection_history(self, collections_in: Union[str, List], length:int=10) -> pd.DataFrame:
        """get collection history

        Parameters
        ----------
            collections_in: str, List
                single collection name in or list of collection names,
                use '' to get all collections
            length: int
                optional length of history to return, default is 30

        Returns
        -------
            DataFrame
                DataFrame with collection history
        """
        params = {'length': length}

        collections = validate_input(collections_in)

        df_list=[]
        for collection in collections:
            endpoint_url = COLLECTION_HISTORY_URL.substitute(collection=collection)
            response = self.get_response(endpoint_url, params=params)
            tmp_df = pd.DataFrame(response['data']['sales'][0]['sales'])
            df_list.append(tmp_df)
        collections_df = pd.concat(df_list, keys=collections, axis=1)
        return collections_df

    def get_collection_stats(self, collections_in: Union[str, List], length: int=30) -> pd.DataFrame:
        """get stats about collection

        Parameters
        ----------
            collections_in: str, List
                single collection name in or list of collection names 
            length: int
                optional length of stats to return, default is 30

        Returns
        -------
            DataFrame
                DataFrame with collection statistics
        """
        # TODO get 'global' to work
        params = {'length': length}

        collections = validate_input(collections_in)

        series_list=[]
        for collection in collections:
            endpoint_url = COLLECTION_STATS_URL.substitute(collection=collection)
            response = self.get_response(endpoint_url, params=params)
            tmp_df = pd.DataFrame(response['data'])
            keys = tmp_df['key'].tolist()
            data = tmp_df['data'].tolist()
            series_dict = dict(zip(keys,data))
            tmp_series = pd.Series(series_dict)
            series_list.append(tmp_series)
        collections_df = pd.concat(series_list, keys=collections, axis=1)
        return collections_df

    def get_collection_summary(self, collections_in: Union[str, List]) -> pd.DataFrame:
        """Retrieve quick collection summary

        Parameters
        ----------
            collections_in: str, List
                single collection name in or list of collection names 

        Returns
        -------
            DataFrame
                DataFrame with collection summary
        """

        collections = validate_input(collections_in)
        series_list=[]
        for collection in collections:
            endpoint_url = COLLECTION_SUMMARY_URL.substitute(collection=collection)
            response = self.get_response(endpoint_url)
            response_dict = response['data']['totals'][0]
            response_dict.update(response_dict['totals']['alltime']) #upack
            response_dict.pop('totals')
            tmp_series = pd.Series(response_dict)

            series_list.append(tmp_series)
        collections_df = pd.concat(series_list, keys=collections, axis=1)
        return collections_df

