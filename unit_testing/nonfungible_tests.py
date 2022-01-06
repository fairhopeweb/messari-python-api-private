"""Unit Tests for the NonFungible class"""

import unittest
import pandas as pd

from messari.nfts import NonFungible

class TestNonFungible(unittest.TestCase):
    """This is a unit testing class for testing the NonFungible class"""

    def test_init(self):
        """Test initializing NonFungible class"""
        nf = NonFungible()
        self.assertIsInstance(nf, NonFungible)

    def test_get_collection_history(self):
        """Test get_collection_history"""
        nf = NonFungible()
        collections = ['cryptopunks', 'doodles']
        tmp_df = nf.get_collection_history(collections_in=collections, length=3)
        self.assertIsInstance(tmp_df, pd.DataFrame)

    def test_get_collection_stats(self):
        """Test get_collection_stats"""
        nf = NonFungible()
        collections = ['cryptopunks', 'doodles']
        tmp_df = nf.get_collection_stats(collections_in=collections)
        self.assertIsInstance(tmp_df, pd.DataFrame)

    def test_get_collection_summary(self):
        """Test get_collection_summary"""
        nf = NonFungible()
        collections = ['cryptopunks', 'doodles']
        tmp_df = nf.get_collection_summary(collections_in=collections)
        self.assertIsInstance(tmp_df, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
