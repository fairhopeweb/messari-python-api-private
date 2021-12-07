"""This module is meant to contain the Etherscan class"""

from typing import Union, List, Dict
import datetime
import pandas as pd

from messari.dataloader import DataLoader
from messari.utils import validate_input, validate_datetime, validate_int
from messari.blockexplorers import Scanner

# Refrence: https://docs.etherscan.io/


#dict.update(dict)


BASE_URL='https://api.etherscan.io/api'
class Etherscan(Scanner):
    """This class is a wrapper around the Etherscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)
