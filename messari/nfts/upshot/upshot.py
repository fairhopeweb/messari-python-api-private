"""This module is meant to contain the Upshot class"""

from messari.dataloader import DataLoader
from messari.utils import validate_input, validate_int
from typing import Union, List

import pandas as pd

# assets
ASSET_URL = 'https://api.upshot.io/v1/asset'
ASSET_EVENTS_URL = 'https://api.upshot.io/v1/asset/events'

# pricing
PRICING_URL = 'https://api.upshot.io/v1/pricing'
PRICING_CURRENT_URL = 'https://api.upshot.io/v1/pricing/current'

# Refrence: https://docs.upshot.xyz/upshot-api/

class Upshot(DataLoader):
    """This class is a wrapper around the Upshot API
    """
    def __init__(self):
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)

    #### assets
    def get_asset(self,
                  contract_address: Union[str, List],
                  asset_id: Union[int, List]=None,
                  limit: int=None,
                  offset: int=0) -> pd.DataFrame:
        """retrieve an asset"""
        # set offset & limit
        parameters = {}
        if limit:
            parameters['limit'] = limit
        parameters['offset'] = offset

        # Validate inputs
        contracts = validate_input(contract_address)
        if asset_id:
            assets = validate_int(asset_id)

        df_list = []
        for contract in contracts:
            # need to use either contract or asset id, upshot api is weird
            if asset_id:
                responses = []
                # NOTE: you can do a request w/ repeated values for 'assetId' but making
                # this work within python is not easy, just looping for now but this can
                # be made better
                for asset in assets:
                    parameters['assetId'] = f'{contract}/{asset}'
                    response = self.get_response(ASSET_URL, params=parameters)['data']
                    responses.append(response['assets'][0])
                asset_df = pd.DataFrame(responses)


            else:
                parameters['contractAddress'] = contract
                response = self.get_response(ASSET_URL, params=parameters)['data']
                asset_df = pd.DataFrame(response['assets'])

            df_list.append(asset_df)
        assets_df = pd.concat(df_list, keys=contracts, axis=1)
        return assets_df

    def get_asset_events(self,
                         contract_address: Union[str, List],
                         asset_id: Union[int, List],
                         market_type: str=None,
                         event_type=None) -> pd.DataFrame:
        """retrieve the event history for a given asset

    PRIMARY or SECONDARY -- optionally filter the events based on the market in which it occurred

string
Filter events by the event type: BID, ASK, SALE, or TRANSFER
        """
        parameters = {}
        if market_type:
            parameters['marketType'] = market_type
        if event_type:
            parameters['type'] = event_type

        contracts = validate_input(contract_address)
        assets = validate_int(asset_id)

        df_list_top = []
        for contract in contracts:
            df_list = []
            for asset in assets:
                parameters['assetId'] = f'{contract}/{asset}'
                response = self.get_response(ASSET_EVENTS_URL, params=parameters)['data']
                tmp_df = pd.DataFrame(response['events'])
                df_list.append(tmp_df)

            assets_df = pd.concat(df_list, keys=assets, axis=1)
            df_list_top.append(assets_df)

        events_df = pd.concat(df_list_top, keys=contracts, axis=1)
        return events_df


    #### pricing
    def get_pricing(self,
                    contract_address: Union[str, List],
                    asset_id: Union[int, List],
                    from_time: int=None,
                    to_time: int=None,
                    confidence: str=None,
                    source: str='UPSHOT') -> pd.DataFrame:
        """Returns all the price information for a specified asset (or assets)
        based on the provided filter."""

        parameters = {}
        if from_time:
            parameters['from'] = from_time
        if to_time:
            parameters['to'] = to_time
        if confidence:
            parameters['confidence'] = confidence
        parameters['source'] = source

        contracts = validate_input(contract_address)
        assets = validate_int(asset_id)

        df_list_top = []
        for contract in contracts:
            df_list = []
            for asset in assets:
                parameters['assetId'] = f'{contract}/{asset}'
                response = self.get_response(PRICING_URL, params=parameters)['data']
                tmp_df = pd.DataFrame(response['pricings'])
                df_list.append(tmp_df)

            assets_df = pd.concat(df_list, keys=assets, axis=1)
            df_list_top.append(assets_df)

        prices_df = pd.concat(df_list_top, keys=contracts, axis=1)
        return prices_df



    def get_pricing_current(self,
                            contract_address: Union[str, List],
                            asset_id: Union[int, List],
                            source: str='UPSHOT') -> pd.DataFrame:
        """Returns an asset's most recent price information."""
        parameters = {}
        parameters['source'] = source

        contracts = validate_input(contract_address)
        assets = validate_int(asset_id)

        df_list_top = []
        for contract in contracts:
            df_list = []
            for asset in assets:
                parameters['assetId'] = f'{contract}/{asset}'
                response = self.get_response(PRICING_CURRENT_URL, params=parameters)['data']
                tmp_df = pd.DataFrame(response['pricings'])
                df_list.append(tmp_df)

            assets_df = pd.concat(df_list, keys=assets, axis=1)
            df_list_top.append(assets_df)

        prices_df = pd.concat(df_list_top, keys=contracts, axis=1)
        return prices_df

