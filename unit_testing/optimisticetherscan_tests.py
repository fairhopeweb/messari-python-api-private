"""Unit Tests for the OptimisticEtherscan class"""

from messari.blockexplorers import OptimisticEtherscan
import unittest
import os
import sys
import pandas as pd
import time
from typing import Dict

API_KEY = os.getenv('OPTIMISTICETHERSCAN_API_KEY')
if API_KEY is None:
    print('Please define OPTIMISITCETHERSCAN_API_KEY in your runtime enviornment')
    sys.exit()

class TestOptimisticEtherscan(unittest.TestCase):
    """This is a unit testing class for testing the OptimisticEtherscan class"""

    def test_init(self):
        """Test initializing OptimisticEtherscan class"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        self.assertIsInstance(oes, OptimisticEtherscan)

    ##### Accounts
    def test_get_account_ether_balance(self):
        """Test get_account_ether_balance"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balances = oes.get_account_native_balance(accounts)
        time.sleep(1)
        self.assertIsInstance(account_balances, pd.DataFrame)

    def test_get_account_normal_transactions(self):
        """Test get_account_normal_transactions"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_normal = oes.get_account_normal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_normal, pd.DataFrame)

    def test_get_account_internal_transactions(self):
        """Test get_account_internal_transactions"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_internal = oes.get_account_internal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_internal, pd.DataFrame)

    def test_get_transaction_internal_transactions(self):
        """Test get_transaction_internal_transactions"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        int_txn = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'
        transaction_internals = oes.get_transaction_internal_transactions(int_txn)
        time.sleep(1)
        self.assertIsInstance(transaction_internals, pd.DataFrame)

    def test_get_block_range_internal_transactions(self):
        """Test get_block_range_internal_transactions"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        block_range_internals = oes.get_block_range_internal_transactions(10000000,10001000)
        time.sleep(1)
        self.assertIsInstance(block_range_internals, pd.DataFrame)

    def test_get_account_token_transfers(self):
        """Test get_account_token_transfers"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_token_transfers = oes.get_account_token_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_token_transfers, pd.DataFrame)

    def test_get_account_nft_transfers(self):
        """Test get_account_nft_transfers"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_nft_transfers = oes.get_account_nft_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_nft_transfers, pd.DataFrame)

    def test_get_account_blocks_mined(self):
        """Test get_account_blocks_mined"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        # Ethermine pubkey, F2Pool Old pubkey
        miners = ['0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8',
                  '0x829BD824B016326A401d083B33D092293333A830']
        account_blocks_mined = oes.get_account_blocks_mined(miners)
        time.sleep(1)
        self.assertIsInstance(account_blocks_mined, pd.DataFrame)

    def test_get_account_l1_deposits(self):
        """Test get_account_l1_deposits"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_l1_deposits = oes.get_account_l1_deposits(accounts)
        time.sleep(1)
        self.assertIsInstance(account_l1_deposits, pd.DataFrame)

    def test_get_account_l2_withdrawals(self):
        """Test get_account_l2_withdrawals"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_l2_withdrawals = oes.get_account_l2_withdrawals(accounts)
        time.sleep(1)
        self.assertIsInstance(account_l2_withdrawals, pd.DataFrame)

    ##### Contracts
    def test_get_contract_abi(self):
        """Test get_contract_abi"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        abis = oes.get_contract_abi(contracts)
        time.sleep(1)
        self.assertIsInstance(abis, Dict)

    def test_get_contract_source_code(self):
        """Test get_contract_source_code"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        source_code = oes.get_contract_source_code(contracts)
        time.sleep(1)
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
        oes = OptimisticEtherscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        total_supply = oes.get_token_total_supply(tokens)
        time.sleep(1)
        self.assertIsInstance(total_supply, pd.DataFrame)

    def test_get_token_account_balance(self):
        """Test get_token_account_balance"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        # One account w/ the above tokens, one account w/out the above tokens
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balance = oes.get_token_account_balance(tokens, accounts)
        time.sleep(1)
        self.assertIsInstance(account_balance, pd.DataFrame)

    ##### Gas Tracker
    # None

    ##### Stats
    def test_get_total_eth_supply(self):
        """Test get_total_eth_supply"""
        oes = OptimisticEtherscan(api_key=API_KEY)
        total_eth_supply = oes.get_total_eth_supply()
        time.sleep(1)
        self.assertIsInstance(total_eth_supply, int)

if __name__ == '__main__':
    unittest.main()
