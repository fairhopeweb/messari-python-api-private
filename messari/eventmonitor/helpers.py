"""This module is dedicated to helpers for the EventMonitor class"""

from messari.utils import validate_input
from messari.blockexplorers import Scanner
from typing import Union, List
import pandas as pd
import json
from web3 import Web3

def validate_checksum(hex_in: Union[str, List]) -> List:
    """Checks if input is list of checksum addresses.

    :param asset_input: str, list
        Single asset slug string or list of asset slugs (i.e. BTC).
    :return List of asset slugs.
    :raises ValueError if input is neither a string or list
    """
    list_in = validate_input(hex_in)
    list_out = []
    for item in list_in:
        list_out.append(Web3.toChecksumAddress(item))
    return list_out

def build_contract_events(contracts: List, explorer: Scanner) -> pd.DataFrame:
    """Return df about info of contract events
    """

    abis_dict = explorer.get_contract_abi(contracts)

    df_list = []
    for contract in contracts:

        contract_abi = json.loads(abis_dict[contract])

        # loop through abi
        event_list=[]
        for entry in contract_abi:
            # looking for events
            if entry['type'] == 'event':
                # get name & inputs
                event_name = entry['name']
                event_inputs = entry['inputs']

                # Some ugly string manipulation
                input_str='('
                for event_input in event_inputs:
                    input_str += f"{event_input['type']},"
                input_str = input_str[:-1] + ')'

                # create text to get event keccak
                event_text = event_name+input_str
                event_keccak = Web3.keccak(text=event_text).hex()

                # making df
                event_dict = {'name': event_name,
                              'text': event_text,
                              'keccak': event_keccak,
                              'inputs': event_inputs}
                event_list.append(event_dict)

        contract_event_df = pd.DataFrame(event_list)
        df_list.append(contract_event_df)

    event_df = pd.concat(df_list, keys=contracts, axis=1)
    return event_df
