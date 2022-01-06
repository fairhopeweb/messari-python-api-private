"""Unit Tests for the BSCscan class"""

from messari.blockexplorers import BSCscan
import unittest
import os
import sys
import pandas as pd
import time
from typing import Dict

API_KEY = os.getenv('BSCSCAN_API_KEY')
if API_KEY is None:
    print('Please define BSCSCAN_API_KEY in your runtime enviornment')
    sys.exit()

class TestBSCscan(unittest.TestCase):
    """This is a unit testing class for testing the BSCscan class"""

    def test_init(self):
        """Test initializing BSCscan class"""
        bs = BSCscan(api_key=API_KEY)
        self.assertIsInstance(bs, BSCscan)

    ##### Accounts
    def test_get_account_ether_balance(self):
        """Test get_account_ether_balance"""
        bs = BSCscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balances = bs.get_account_native_balance(accounts)
        time.sleep(1)
        self.assertIsInstance(account_balances, pd.DataFrame)

    def test_get_account_normal_transactions(self):
        """Test get_account_normal_transactions"""
        bs = BSCscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_normal = bs.get_account_normal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_normal, pd.DataFrame)

    def test_get_account_internal_transactions(self):
        """Test get_account_internal_transactions"""
        bs = BSCscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_internal = bs.get_account_internal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_internal, pd.DataFrame)

    def test_get_transaction_internal_transactions(self):
        """Test get_transaction_internal_transactions"""
        bs = BSCscan(api_key=API_KEY)
        int_txn = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'
        transaction_internals = bs.get_transaction_internal_transactions(int_txn)
        time.sleep(1)
        self.assertIsInstance(transaction_internals, pd.DataFrame)

    def test_get_block_range_internal_transactions(self):
        """Test get_block_range_internal_transactions"""
        bs = BSCscan(api_key=API_KEY)
        block_range_internals = bs.get_block_range_internal_transactions(10000000,10001000)
        time.sleep(1)
        self.assertIsInstance(block_range_internals, pd.DataFrame)

    def test_get_account_token_transfers(self):
        """Test get_account_token_transfers"""
        bs = BSCscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_token_transfers = bs.get_account_token_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_token_transfers, pd.DataFrame)

    def test_get_account_nft_transfers(self):
        """Test get_account_nft_transfers"""
        bs = BSCscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_nft_transfers = bs.get_account_nft_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_nft_transfers, pd.DataFrame)

    def test_get_account_blocks_mined(self):
        """Test get_account_blocks_mined"""
        bs = BSCscan(api_key=API_KEY)
        # Ethermine pubkey, F2Pool Old pubkey
        miners = ['0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8',
                  '0x829BD824B016326A401d083B33D092293333A830']
        account_blocks_mined = bs.get_account_blocks_mined(miners)
        time.sleep(1)
        self.assertIsInstance(account_blocks_mined, pd.DataFrame)

    ##### Contracts
    def test_get_contract_abi(self):
        """Test get_contract_abi"""
        bs = BSCscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        abis = bs.get_contract_abi(contracts)
        time.sleep(1)
        self.assertIsInstance(abis, Dict)

    def test_get_contract_source_code(self):
        """Test get_contract_source_code"""
        bs = BSCscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        source_code = bs.get_contract_source_code(contracts)
        time.sleep(1)
        self.assertIsInstance(source_code, pd.DataFrame)

    ##### Transactions
    def test_get_transaction_execution_status(self):
        """Test get_transaction_execution_status"""
        bs = BSCscan(api_key=API_KEY)
        txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6',
                '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc',
                '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
        transaction_execution_status = bs.get_transaction_execution_status(txns)
        time.sleep(1)
        self.assertIsInstance(transaction_execution_status, pd.DataFrame)

    ##### Blocks
    def test_get_block_reward(self):
        """Test get_block_reward"""
        bs = BSCscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        block_rewards = bs.get_block_reward(blocks)
        time.sleep(1)
        self.assertIsInstance(block_rewards, pd.DataFrame)

    def test_get_block_countdown(self):
        """Test get_block_countdown"""
        bs = BSCscan(api_key=API_KEY)
        far_out_block = 50000000
        block_countdown = bs.get_block_countdown(far_out_block)
        time.sleep(1)
        self.assertIsInstance(block_countdown, pd.DataFrame)

    def test_get_block_by_timestamp(self):
        """Test get_block_by_timestamp"""
        bs = BSCscan(api_key=API_KEY)
        timestamp = 1638767557
        block_at_time = bs.get_block_by_timestamp(timestamp)
        time.sleep(1)
        self.assertIsInstance(block_at_time, pd.DataFrame)

    ##### Logs
    def test_get_logs(self):
        """Test get_logs"""
        bs = BSCscan(api_key=API_KEY)
        address = '0x33990122638b9132ca29c723bdf037f1a891a70c'
        from_block = 379224
        to_block = 'latest'
        topic0 = '0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545'
        logs = bs.get_logs(address, from_block, to_block=to_block, topic0=topic0)
        time.sleep(1)
        self.assertIsInstance(logs, pd.DataFrame)

    ##### Geth/Parity Proxy
    def test_get_eth_block_number(self):
        """Test get_eth_block_number"""
        bs = BSCscan(api_key=API_KEY)
        block_number = bs.get_eth_block_number()
        time.sleep(1)
        self.assertIsInstance(block_number, int)

    def test_get_eth_block(self):
        """Test get_eth_block"""
        bs = BSCscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        eth_blocks = bs.get_eth_block(blocks)
        time.sleep(1)
        self.assertIsInstance(eth_blocks, pd.DataFrame)

    def test_get_eth_block_transaction_count(self):
        """Test get_eth_block_transaction_count"""
        bs = BSCscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        block_transaction_count = bs.get_eth_block_transaction_count(blocks)
        time.sleep(1)
        self.assertIsInstance(block_transaction_count, pd.DataFrame)

    def test_get_eth_transaction_by_hash(self):
        """Test get_eth_transaction_by_hash"""
        bs = BSCscan(api_key=API_KEY)
        txns = ['0x287cd684bdaf6f6778b779f6dba359a625aede6e515af24979aa5f69b7c2224a']
        txns_by_hash = bs.get_eth_transaction_by_hash(txns)
        time.sleep(1)
        self.assertIsInstance(txns_by_hash, pd.DataFrame)

    def test_get_eth_transaction_by_block_index(self):
        """Test get_eth_transaction_by_block_index"""
        bs = BSCscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        index = 0
        txn_info = bs.get_eth_transaction_by_block_index(blocks[0], index)
        time.sleep(1)
        self.assertIsInstance(txn_info, pd.DataFrame)

    def test_get_eth_account_transaction_count(self):
        """Test get_eth_account_transaction_count"""
        bs = BSCscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        transaction_count = bs.get_eth_account_transaction_count(accounts)
        time.sleep(1)
        self.assertIsInstance(transaction_count, pd.DataFrame)

    def test_get_eth_transaction_receipt(self):
        """Test get_eth_transaction_receipt"""
        bs = BSCscan(api_key=API_KEY)
        txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6',
                '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc',
                '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
        receipts = bs.get_eth_transaction_receipt(txns)
        time.sleep(1)
        self.assertIsInstance(receipts, pd.DataFrame)

    def test_get_eth_gas_price(self):
        """Test get_eth_gas_price"""
        bs = BSCscan(api_key=API_KEY)
        gas_price = bs.get_eth_gas_price()
        time.sleep(1)
        self.assertIsInstance(gas_price, int)

    ##### Tokens
    def test_get_token_total_supply(self):
        """Test get_token_total_supply"""
        bs = BSCscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        total_supply = bs.get_token_total_supply(tokens)
        time.sleep(1)
        self.assertIsInstance(total_supply, pd.DataFrame)

    def test_get_token_account_balance(self):
        """Test get_token_account_balance"""
        bs = BSCscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        # One account w/ the above tokens, one account w/out the above tokens
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balance = bs.get_token_account_balance(tokens, accounts)
        time.sleep(1)
        self.assertIsInstance(account_balance, pd.DataFrame)

    def test_get_token_circulating_supply(self):
        """Test get_token_circulating_supply"""
        bs = BSCscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        total_supply = bs.get_token_circulating_supply(tokens)
        time.sleep(1)
        self.assertIsInstance(total_supply, pd.DataFrame)


    ##### Gas Tracker
    def test_get_gas_oracle(self):
        """Test get_gas_oracle"""
        bs = BSCscan(api_key=API_KEY)
        gas_oracle = bs.get_gas_oracle()
        time.sleep(1)
        self.assertIsInstance(gas_oracle, pd.DataFrame)

    ##### Stats
    def test_get_total_bnb_supply(self):
        """Test get_total_bnb_supply"""
        bs = BSCscan(api_key=API_KEY)
        total_bnb_supply = bs.get_total_bnb_supply()
        time.sleep(1)
        self.assertIsInstance(total_bnb_supply, int)

    def test_get_validators(self):
        """Test get_validators"""
        bs = BSCscan(api_key=API_KEY)
        validators = bs.get_validators()
        self.assertIsInstance(validators, pd.DataFrame)

    def test_get_last_bnb_price(self):
        """Test get_last_eth_price"""
        bs = BSCscan(api_key=API_KEY)
        last_bnb_price = bs.get_last_bnb_price()
        time.sleep(1)
        self.assertIsInstance(last_bnb_price, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
