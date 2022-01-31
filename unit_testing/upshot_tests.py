"""Unit Tests for the Upshot class"""

import unittest
import time
import pandas as pd

from messari.nfts import Upshot

class TestUpshot(unittest.TestCase):
    """This is a unit testing class for testing the Upshot class"""

    def test_init(self):
        """Test initializing Upshot class"""
        up = Upshot()
        self.assertIsInstance(up, Upshot)

    def test_get_asset(self):
        """Test get_asset"""
        contract = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
        asset_id = ['11', '1']
        up = Upshot()
        time.sleep(10)
        tmp_df = up.get_asset(contract_address=contract, asset_id=asset_id)
        self.assertIsInstance(tmp_df, pd.DataFrame)

    def test_get_asset_events(self):
        """Test get_asset_events"""
        contract = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
        asset_id = ['11', '1']
        up = Upshot()
        time.sleep(10)
        tmp_df = up.get_asset_events(contract_address=contract, asset_id=asset_id)
        self.assertIsInstance(tmp_df, pd.DataFrame)

    def test_get_pricing(self):
        """Test get_pricing"""
        contract = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
        asset_id = ['11', '1']
        up = Upshot()
        time.sleep(10)
        tmp_df = up.get_pricing(contract_address=contract, asset_id=asset_id)
        self.assertIsInstance(tmp_df, pd.DataFrame)

    def test_get_pricing_current(self):
        """Test get_pricing_current"""
        contract = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
        asset_id = ['11', '1']
        up = Upshot()
        time.sleep(10)
        tmp_df = up.get_pricing(contract_address=contract, asset_id=asset_id)
        self.assertIsInstance(tmp_df, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
