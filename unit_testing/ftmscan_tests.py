"""Unit Tests for the FTMscan class"""

from messari.blockexplorers import FTMscan
import unittest
import os
import sys
import pandas as pd
import time
from typing import Dict

API_KEY = os.getenv('FTMSCAN_API_KEY')
if API_KEY is None:
    print('Please define FTMSCAN_API_KEY in your runtime enviornment')
    sys.exit()

class TestFTMscan(unittest.TestCase):
    """This is a unit testing class for testing the Etherscan class"""

    def test_init(self):
        """Test initializing Etherscan class"""
        fs = FTMscan(api_key=API_KEY)
        self.assertIsInstance(fs, FTMscan)

    ##### Accounts
    def test_get_account_ether_balance(self):
        """Test get_account_ether_balance"""
        fs = FTMscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        time.sleep(1)
        account_balances = fs.get_account_native_balance(accounts)
        self.assertIsInstance(account_balances, pd.DataFrame)

    def test_get_account_normal_transactions(self):
        """Test get_account_normal_transactions"""
        fs = FTMscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        time.sleep(1)
        account_normal = fs.get_account_normal_transactions(accounts)
        self.assertIsInstance(account_normal, pd.DataFrame)

    def test_get_account_internal_transactions(self):
        """Test get_account_internal_transactions"""
        fs = FTMscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        time.sleep(1)
        account_internal = fs.get_account_internal_transactions(accounts)
        self.assertIsInstance(account_internal, pd.DataFrame)

    def test_get_transaction_internal_transactions(self):
        """Test get_transaction_internal_transactions"""
        fs = FTMscan(api_key=API_KEY)
        int_txn = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'
        time.sleep(1)
        transaction_internals = fs.get_transaction_internal_transactions(int_txn)
        self.assertIsInstance(transaction_internals, pd.DataFrame)

    def test_get_block_range_internal_transactions(self):
        """Test get_block_range_internal_transactions"""
        fs = FTMscan(api_key=API_KEY)
        time.sleep(1)
        block_range_internals = fs.get_block_range_internal_transactions(10000000,10001000)
        self.assertIsInstance(block_range_internals, pd.DataFrame)

    def test_get_account_token_transfers(self):
        """Test get_account_token_transfers"""
        fs = FTMscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12']
        time.sleep(1)
        account_token_transfers = fs.get_account_token_transfers(accounts)
        self.assertIsInstance(account_token_transfers, pd.DataFrame)

    def test_get_account_nft_transfers(self):
        """Test get_account_nft_transfers"""
        fs = FTMscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12']
        time.sleep(1)
        account_nft_transfers = fs.get_account_nft_transfers(accounts)
        self.assertIsInstance(account_nft_transfers, pd.DataFrame)

    def test_get_account_blocks_mined(self):
        """Test get_account_blocks_mined"""
        fs = FTMscan(api_key=API_KEY)
        # On Fantom all blocks are mined by null address
        miners = ['0x0000000000000000000000000000000000000000']
        time.sleep(1)
        account_blocks_mined = fs.get_account_blocks_mined(miners)
        self.assertIsInstance(account_blocks_mined, pd.DataFrame)

    ##### Contracts
    def test_get_contract_abi(self):
        """Test get_contract_abi"""
        fs = FTMscan(api_key=API_KEY)
        # wakaswap Router
        contracts = ['0x7B17021FcB7Bc888641dC3bEdfEd3734fCaf2c87']
        time.sleep(1)
        abis = fs.get_contract_abi(contracts)
        self.assertIsInstance(abis, Dict)

    def test_get_contract_source_code(self):
        """Test get_contract_source_code"""
        fs = FTMscan(api_key=API_KEY)
        # wakaswap Router
        contracts = ['0x7B17021FcB7Bc888641dC3bEdfEd3734fCaf2c87']
        time.sleep(1)
        source_code = fs.get_contract_source_code(contracts)
        self.assertIsInstance(source_code, pd.DataFrame)

    ##### Transactions
    # None

    ##### Blocks
    # None

    ##### Logs
    # None

    ##### Geth/Parity Proxy
    # None

    ##### Tokens
    def test_get_token_total_supply(self):
        """Test get_token_total_supply"""
        fs = FTMscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        time.sleep(1)
        total_supply = fs.get_token_total_supply(tokens)
        self.assertIsInstance(total_supply, pd.DataFrame)

    def test_get_token_account_balance(self):
        """Test get_token_account_balance"""
        fs = FTMscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        # One account w/ the above tokens, one account w/out the above tokens
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        time.sleep(1)
        account_balance = fs.get_token_account_balance(tokens, accounts)
        self.assertIsInstance(account_balance, pd.DataFrame)

    ##### Gas Tracker
    # None

    ##### Stats
    def test_get_total_ftm_supply(self):
        """Test get_total_ftm_supply"""
        fs = FTMscan(api_key=API_KEY)
        time.sleep(1)
        total_ftm_supply = fs.get_total_ftm_supply()
        self.assertIsInstance(total_ftm_supply, int)

    def test_get_validators(self):
        """Test get_validators"""
        fs = FTMscan(api_key=API_KEY)
        time.sleep(1)
        validators = fs.get_validators()
        self.assertIsInstance(validators, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
