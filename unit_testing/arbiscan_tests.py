"""Unit Tests for the Etherscan class"""

from messari.blockexplorers import Arbiscan
import unittest
import os
import sys
import pandas as pd
import time
from typing import Dict

API_KEY = os.getenv('ETHERSCAN_API_KEY')
if API_KEY is None:
    print('Please define ETHERSCAN_API_KEY in your runtime enviornment')
    sys.exit()

class TestArbiscan(unittest.TestCase):
    """This is a unit testing class for testing the Etherscan class"""

    def test_init(self):
        """Test initializing Etherscan class"""
        arbiscan = Arbiscan(api_key=API_KEY)
        self.assertIsInstance(arbiscan, Arbiscan)

    ##### Accounts
    def test_get_account_ether_balance(self):
        """Test get_account_ether_balance"""
        arbiscan = Arbiscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balances = arbiscan.get_account_native_balance(accounts)
        time.sleep(1)
        self.assertIsInstance(account_balances, pd.DataFrame)

    def test_get_account_normal_transactions(self):
        """Test get_account_normal_transactions"""
        arbiscan = Arbiscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_normal = arbiscan.get_account_normal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_normal, pd.DataFrame)

    def test_get_account_internal_transactions(self):
        """Test get_account_internal_transactions"""
        arbiscan = Arbiscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_internal = arbiscan.get_account_internal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_internal, pd.DataFrame)

    def test_get_transaction_internal_transactions(self):
        """Test get_transaction_internal_transactions"""
        arbiscan = Arbiscan(api_key=API_KEY)
        int_txn = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'
        transaction_internals = arbiscan.get_transaction_internal_transactions(int_txn)
        time.sleep(1)
        self.assertIsInstance(transaction_internals, pd.DataFrame)

    def test_get_block_range_internal_transactions(self):
        """Test get_block_range_internal_transactions"""
        arbiscan = Arbiscan(api_key=API_KEY)
        block_range_internals = arbiscan.get_block_range_internal_transactions(10000000,10001000)
        time.sleep(1)
        self.assertIsInstance(block_range_internals, pd.DataFrame)

    def test_get_account_token_transfers(self):
        """Test get_account_token_transfers"""
        arbiscan = Arbiscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_token_transfers = arbiscan.get_account_token_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_token_transfers, pd.DataFrame)

    def test_get_account_nft_transfers(self):
        """Test get_account_nft_transfers"""
        arbiscan = Arbiscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_nft_transfers = arbiscan.get_account_nft_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_nft_transfers, pd.DataFrame)

    def test_get_account_blocks_mined(self):
        """Test get_account_blocks_mined"""
        arbiscan = Arbiscan(api_key=API_KEY)
        # Ethermine pubkey, F2Pool Old pubkey
        miners = ['0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8',
                  '0x829BD824B016326A401d083B33D092293333A830']
        account_blocks_mined = arbiscan.get_account_blocks_mined(miners)
        time.sleep(1)
        self.assertIsInstance(account_blocks_mined, pd.DataFrame)

    ##### Contracts
    def test_get_contract_abi(self):
        """Test get_contract_abi"""
        arbiscan = Arbiscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        abis = arbiscan.get_contract_abi(contracts)
        time.sleep(1)
        self.assertIsInstance(abis, Dict)

    def test_get_contract_source_code(self):
        """Test get_contract_source_code"""
        arbiscan = Arbiscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        source_code = arbiscan.get_contract_source_code(contracts)
        time.sleep(1)
        self.assertIsInstance(source_code, pd.DataFrame)

    ##### Transactions
    def test_get_transaction_execution_status(self):
        """Test get_transaction_execution_status"""
        arbiscan = Arbiscan(api_key=API_KEY)
        txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6',
                '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc',
                '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
        transaction_execution_status = arbiscan.get_transaction_execution_status(txns)
        time.sleep(1)
        self.assertIsInstance(transaction_execution_status, pd.DataFrame)

    ##### Blocks
    def test_get_block_by_timestamp(self):
        """Test get_block_by_timestamp"""
        arbiscan = Arbiscan(api_key=API_KEY)
        timestamp = 1638767557
        block_at_time = arbiscan.get_block_by_timestamp(timestamp)
        time.sleep(1)
        self.assertIsInstance(block_at_time, pd.DataFrame)

    ##### Logs
    def test_get_logs(self):
        """Test get_logs"""
        arbiscan = Arbiscan(api_key=API_KEY)
        address = '0x33990122638b9132ca29c723bdf037f1a891a70c'
        from_block = 379224
        to_block = 'latest'
        topic0 = '0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545'
        logs = arbiscan.get_logs(address, from_block, to_block=to_block, topic0=topic0)
        time.sleep(1)
        self.assertIsInstance(logs, pd.DataFrame)

    ##### Geth/Parity Proxy
    # NONE

    ##### Tokens
    def test_get_token_total_supply(self):
        """Test get_token_total_supply"""
        arbiscan = Arbiscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        total_supply = arbiscan.get_token_total_supply(tokens)
        time.sleep(1)
        self.assertIsInstance(total_supply, pd.DataFrame)

    def test_get_token_account_balance(self):
        """Test get_token_account_balance"""
        arbiscan = Arbiscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        # One account w/ the above tokens, one account w/out the above tokens
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balance = arbiscan.get_token_account_balance(tokens, accounts)
        time.sleep(1)
        self.assertIsInstance(account_balance, pd.DataFrame)

    def test_get_token_circulating_supply(self):
        """Test get_token_circulating_supply"""
        arbiscan = Arbiscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        total_supply = arbiscan.get_token_circulating_supply(tokens)
        time.sleep(1)
        self.assertIsInstance(total_supply, pd.DataFrame)

    ##### Gas Tracker
    # NONE

    ##### Stats
    # NONE

if __name__ == '__main__':
    unittest.main()
