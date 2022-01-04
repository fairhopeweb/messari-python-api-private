"""Unit Tests for the DeepDAO class"""

import unittest
import pandas as pd
from typing import List

from messari.deepdao import DeepDAO

class TestDeepDAO(unittest.TestCase):
    """This is a unit testing class for testing the DeeDAO class"""

    def test_init(self):
        """Test initializing DeepDAO class"""
        dd = DeepDAO()
        self.assertIsInstance(dd, DeepDAO)

    def test_get_dao_list(self):
        """Test get_dao_list"""
        dd = DeepDAO()
        dao_list = dd.get_dao_list()
        self.assertIsInstance(dao_list, List)

    def test_get_member_list(self):
        """Test get_member_list"""
        dd = DeepDAO()
        member_list = dd.get_member_list()
        self.assertIsInstance(member_list, List)

    def test_get_organizations(self):
        """Test get_organizations"""
        dd = DeepDAO()
        organizations = dd.get_organizations()
        self.assertIsInstance(organizations, pd.DataFrame)

    def test_get_summary(self):
        """Test get_summary"""
        dd = DeepDAO()
        summary = dd.get_summary()
        self.assertIsInstance(summary, pd.DataFrame)

    def test_get_overview(self):
        """Test get_overview"""
        dd = DeepDAO()
        overview = dd.get_overview()
        self.assertIsInstance(overview, pd.DataFrame)

    def test_get_rankings(self):
        """Test get_rankings"""
        dd = DeepDAO()
        rankings = dd.get_rankings()
        self.assertIsInstance(rankings, pd.DataFrame)

    def test_get_tokens(self):
        """Test get_tokens"""
        dd = DeepDAO()
        tokens = dd.get_tokens()
        self.assertIsInstance(tokens, pd.DataFrame)

    def test_get_dao_info(self):
        """Test get_dao_info"""
        dd = DeepDAO()
        daos = ["Uniswap", "Compound"]
        info = dd.get_dao_info(dao_slugs=daos)
        self.assertIsInstance(info, pd.DataFrame)

    def test_get_dao_indices(self):
        """Test get_dao_indices"""
        dd = DeepDAO()
        daos=["Uniswap", "Compound", "Olympus DAO", "Aave", "Gnosis"]
        indices = dd.get_dao_indices(dao_slugs=daos)
        self.assertIsInstance(indices, pd.DataFrame)

    def test_get_dao_proposals(self):
        """Test get_dao_proposals"""
        dd = DeepDAO()
        daos = ["Uniswap", "Compound"]
        proposals = dd.get_dao_proposals(dao_slugs=daos)
        self.assertIsInstance(proposals, pd.DataFrame)


    def test_get_dao_members(self):
        """Test get_dao_members"""
        dd = DeepDAO()
        daos = ["Uniswap", "Compound"]
        members = dd.get_dao_members(dao_slugs=daos)
        self.assertIsInstance(members, pd.DataFrame)

    def test_get_dao_voter_coalitions(self):
        """Test get_voter_coalitions"""
        dd = DeepDAO()
        daos = ["Uniswap", "Compound"]
        coalitions = dd.get_dao_voter_coalitions(dao_slugs=daos)
        self.assertIsInstance(coalitions, pd.DataFrame)

    def test_get_dao_financials(self):
        """Test get_dao_financials"""
        dd = DeepDAO()
        daos = ["Uniswap", "Compound"]
        financials = dd.get_dao_financials(dao_slugs=daos)
        self.assertIsInstance(financials, pd.DataFrame)

    def test_get_top_members(self):
        """Test get_top_members"""
        dd = DeepDAO()
        people = dd.get_top_members(count=10)
        self.assertIsInstance(people, pd.DataFrame)

    def test_get_member_info(self):
        """Test get_member_info"""
        dd = DeepDAO()
        pubkeys = ["Ven Gist", "scottrepreneur"]
        members = dd.get_member_info(pubkeys=pubkeys)
        self.assertIsInstance(members, pd.DataFrame)

    def test_get_member_proposals(self):
        """Test get_member_proposals"""
        dd = DeepDAO()
        pubkeys = ["Ven Gist", "scottrepreneur"]
        member_proposals = dd.get_member_proposals(pubkeys=pubkeys)
        self.assertIsInstance(member_proposals, pd.DataFrame)

    def test_get_member_votes(self):
        """Test get_member_votes"""
        dd = DeepDAO()
        pubkeys = ["Ven Gist", "scottrepreneur"]
        member_votes = dd.get_member_votes(pubkeys=pubkeys)
        self.assertIsInstance(member_votes, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
