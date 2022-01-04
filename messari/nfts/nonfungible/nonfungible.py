"""This module is meant to contain the NonFungible class"""

from messari.dataloader import DataLoader
from messari.utils import validate_input, validate_int
from typing import Union, List

import pandas as pd


class NonFungible(DataLoader):
    """This class is a wrapper around the NonFungible API
    """
    def __init__(self):
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)
