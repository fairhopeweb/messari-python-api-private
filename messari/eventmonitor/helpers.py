"""This module is dedicated to helpers for the EventMonitor class"""
from messari.utils import validate_input
from typing import Union, List

from web3 import Web3

def validate_checksum(hex_in: Union[str, List]) -> List:
    list_in = validate_input(hex_in)
    list_out = []
    for item in list_in:
        list_out.append(Web3.toChecksumAddress(item))
    return list_out
