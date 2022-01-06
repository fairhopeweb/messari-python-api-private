"""Unit Tests for the NFTPriceFloor class"""

import unittest
import pandas as pd

from messari.nfts import NFTPriceFloor

class TestNFTPriceFloor(unittest.TestCase):
    """This is a unit testing class for testing the NFTPriceFloor class"""

    def test_init(self):
        """Test initializing NFTPriceFloor class"""
        floor = NFTPriceFloor()
        self.assertIsInstance(floor, NFTPriceFloor)

    def test_get_nfts(self):
        """Test get_nfts"""
        floor = NFTPriceFloor()
        tmp_df = floor.get_nfts()
        self.assertIsInstance(tmp_df, pd.DataFrame)

    def test_get_floor(self):
        """Test get_floor"""
        collections = ['boredApesYC', 'coolCats', 'cryptoPunks']
        floor = NFTPriceFloor()
        tmp_df = floor.get_floor(collections)
        self.assertIsInstance(tmp_df, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
