"""Unit Tests for the Solscan class"""

from messari.blockexplorers import Solscan
import unittest
import pandas as pd
from typing import List


class TestSolscan(unittest.TestCase):
    """This is a unit testing class for testing the Solscan class"""

    def test_init(self):
        """Test initializing Solscan class"""
        ss = Solscan()
        self.assertIsInstance(ss, Solscan)

    def test_get_last_blocks(self):
        """Test get_last_blocks"""
        ss = Solscan()
        last_blocks = ss.get_last_blocks(num_blocks=10)
        self.assertIsInstance(last_blocks, pd.DataFrame)

    def test_get_block_last_transactions(self):
        """Test get_block_last_transactions"""
        ss = Solscan()
        blocks = ['109452586', '109452587']
        block_last_transactions = ss.get_block_last_transactions(blocks, num_transactions=7)
        self.assertIsInstance(block_last_transactions, pd.DataFrame)

    def test_get_block(self):
        """Test get_block"""
        ss = Solscan()
        blocks = ['109452586', '109452587']
        blocks_info = ss.get_block(blocks)
        self.assertIsInstance(blocks_info, pd.DataFrame)


    def test_get_last_transactions(self):
        """Test get_last_transaction"""
        ss = Solscan()
        last_transactions = ss.get_last_transactions(num_transactions=20)
        self.assertIsInstance(last_transactions, pd.DataFrame)


    def test_get_transaction(self):
        """Test get_transaction"""
        ss = Solscan()
        transactions=['T4ipYTjKUqHQpfuA8ZM5E4iJag9kX9nGhjbY974oq2ucyYRL6eWhqTjtmk3cqfqTSu8Qdce33vzKQd7bWEX3H21', # pylint: disable=line-too-long
                      '5hJhu4RYQLZF3zBwTUzu6vbvt6kX71uoFTTdx6NurkESEeQsjTJNut6FzSjgBqGe8j9V4dDo2VFssbRGiwbachom'] # pylint: disable=line-too-long
        transactions_info = ss.get_transaction(transactions)
        self.assertIsInstance(transactions_info, pd.DataFrame)

    def test_get_account_tokens(self):
        """Test get_account_tokens"""
        ss = Solscan()
        accounts = ['Fhhq7AtgMsWge7oBMMWkqaF4boMLJ6Utcmc2X1oEsqJQ',
                    '7MwQuB8vsCosYiqY4NCBDiECgsv5aFDYP3Zd5zBT6oaS']
        account_tokens = ss.get_account_tokens(accounts)
        self.assertIsInstance(account_tokens, pd.DataFrame)

    def test_get_account_transactions(self):
        """Test get_account_transactions"""
        ss = Solscan()
        accounts = ['5FCSMognWSsNGjmYK9D387Zz79catdwEakdNtGf2UAJS']
        account_transactions = ss.get_account_transactions(accounts)
        self.assertIsInstance(account_transactions, pd.DataFrame)

    def test_get_account_stake(self):
        """Test get_account_stake"""
        ss = Solscan()
        accounts = ['6qdpJdp6L8cCSEECt4vSUbDtRH6oe7MrMY3s1iBSJHie']
        stake_accounts = ss.get_account_stake(accounts)
        self.assertIsInstance(stake_accounts, pd.DataFrame)

    def test_get_account_spl_transactions(self):
        """Test get_account_spl_transactions"""
        ss = Solscan()
        accounts = ['Fhhq7AtgMsWge7oBMMWkqaF4boMLJ6Utcmc2X1oEsqJQ',
                    '7MwQuB8vsCosYiqY4NCBDiECgsv5aFDYP3Zd5zBT6oaS']
        account_spl_transactions = ss.get_account_spl_transactions(accounts)
        self.assertIsInstance(account_spl_transactions, pd.DataFrame)

    def test_get_account_sol_transactions(self):
        """Test get_account_sol_transactions"""
        ss = Solscan()
        accounts = ['Fhhq7AtgMsWge7oBMMWkqaF4boMLJ6Utcmc2X1oEsqJQ',
                    '7MwQuB8vsCosYiqY4NCBDiECgsv5aFDYP3Zd5zBT6oaS']
        account_sol_transactions = ss.get_account_sol_transactions(accounts)
        self.assertIsInstance(account_sol_transactions, pd.DataFrame)

    def test_get_account_export_transactions(self):
        """Test get_account_export_transactions"""
        ss = Solscan()
        accounts = ['Fhhq7AtgMsWge7oBMMWkqaF4boMLJ6Utcmc2X1oEsqJQ',
                    '7MwQuB8vsCosYiqY4NCBDiECgsv5aFDYP3Zd5zBT6oaS']
        account_export_transactions = ss.get_account_export_transactions(accounts,
                                                                         type_in='all',
                                                                         from_time=0,
                                                                         to_time=1634918610)
        self.assertIsInstance(account_export_transactions, List)
        self.assertIsInstance(account_export_transactions[0], str)

    def test_get_account(self):
        """Test get_account"""
        ss = Solscan()
        accounts = ['Fhhq7AtgMsWge7oBMMWkqaF4boMLJ6Utcmc2X1oEsqJQ',
                    'hz4sZFVC1MccN3WaSZ8YjHcZLewLw2JL7t1RfaRa4Pe']
        accounts = ss.get_account(accounts)
        self.assertIsInstance(accounts, pd.DataFrame)

    def test_get_token_holders(self):
        """Test get_token_holders"""
        ss = Solscan()
        tokens = ['Saber2gLauYim4Mvftnrasomsv6NvAuncvMEZwcLpD1']
        token_holders = ss.get_token_holders(tokens, limit=50)
        self.assertIsInstance(token_holders, pd.DataFrame)

    def test_get_token_meta(self):
        """Test get_token_meta"""
        ss = Solscan()
        tokens = ['Saber2gLauYim4Mvftnrasomsv6NvAuncvMEZwcLpD1']
        token_meta = ss.get_token_meta(tokens)
        self.assertIsInstance(token_meta, pd.DataFrame)

    def test_get_token_list(self):
        """Test get_token_list"""
        ss = Solscan()
        token_list = ss.get_token_list(limit=50)
        self.assertIsInstance(token_list, pd.DataFrame)

    def test_get_market_info(self):
        """Test get_market_info"""
        ss = Solscan()
        tokens = ['Saber2gLauYim4Mvftnrasomsv6NvAuncvMEZwcLpD1',
                  '2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk']
        market_info = ss.get_market_info(tokens)
        self.assertIsInstance(market_info, pd.DataFrame)

    def test_get_chain_info(self):
        """Test get_chain_info"""
        ss = Solscan()
        chain_info = ss.get_chain_info()
        self.assertIsInstance(chain_info, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
