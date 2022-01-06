"""Unit Tests for the Etherscan class"""

from messari.blockexplorers import Etherscan
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

class TestEtherscan(unittest.TestCase):
    """This is a unit testing class for testing the Etherscan class"""

    def test_init(self):
        """Test initializing Etherscan class"""
        es = Etherscan(api_key=API_KEY)
        self.assertIsInstance(es, Etherscan)

    ##### Accounts
    def test_get_account_ether_balance(self):
        """Test get_account_ether_balance"""
        es = Etherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balances = es.get_account_native_balance(accounts)
        time.sleep(1)
        self.assertIsInstance(account_balances, pd.DataFrame)

    def test_get_account_normal_transactions(self):
        """Test get_account_normal_transactions"""
        es = Etherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_normal = es.get_account_normal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_normal, pd.DataFrame)

    def test_get_account_internal_transactions(self):
        """Test get_account_internal_transactions"""
        es = Etherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_internal = es.get_account_internal_transactions(accounts)
        time.sleep(1)
        self.assertIsInstance(account_internal, pd.DataFrame)

    def test_get_transaction_internal_transactions(self):
        """Test get_transaction_internal_transactions"""
        es = Etherscan(api_key=API_KEY)
        int_txn = '0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170'
        transaction_internals = es.get_transaction_internal_transactions(int_txn)
        time.sleep(1)
        self.assertIsInstance(transaction_internals, pd.DataFrame)

    def test_get_block_range_internal_transactions(self):
        """Test get_block_range_internal_transactions"""
        es = Etherscan(api_key=API_KEY)
        block_range_internals = es.get_block_range_internal_transactions(10000000,10001000)
        time.sleep(1)
        self.assertIsInstance(block_range_internals, pd.DataFrame)

    def test_get_account_token_transfers(self):
        """Test get_account_token_transfers"""
        es = Etherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_token_transfers = es.get_account_token_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_token_transfers, pd.DataFrame)

    def test_get_account_nft_transfers(self):
        """Test get_account_nft_transfers"""
        es = Etherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_nft_transfers = es.get_account_nft_transfers(accounts)
        time.sleep(1)
        self.assertIsInstance(account_nft_transfers, pd.DataFrame)

    def test_get_account_blocks_mined(self):
        """Test get_account_blocks_mined"""
        es = Etherscan(api_key=API_KEY)
        # Ethermine pubkey, F2Pool Old pubkey
        miners = ['0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8',
                  '0x829BD824B016326A401d083B33D092293333A830']
        account_blocks_mined = es.get_account_blocks_mined(miners)
        time.sleep(1)
        self.assertIsInstance(account_blocks_mined, pd.DataFrame)

    ##### Contracts
    def test_get_contract_abi(self):
        """Test get_contract_abi"""
        es = Etherscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        abis = es.get_contract_abi(contracts)
        time.sleep(1)
        self.assertIsInstance(abis, Dict)

    def test_get_contract_source_code(self):
        """Test get_contract_source_code"""
        es = Etherscan(api_key=API_KEY)
        # Sushiswap Router, Ygov Contract
        contracts = ['0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
                     '0x0001FB050Fe7312791bF6475b96569D83F695C9f']
        source_code = es.get_contract_source_code(contracts)
        time.sleep(1)
        self.assertIsInstance(source_code, pd.DataFrame)

    ##### Transactions
    def test_get_contract_execution_status(self):
        """Test get_contract_execution_status"""
        es = Etherscan(api_key=API_KEY)
        txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6',
                '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc',
                '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
        contract_execution_status = es.get_contract_execution_status(txns)
        time.sleep(1)
        self.assertIsInstance(contract_execution_status, pd.DataFrame)

    def test_get_transaction_execution_status(self):
        """Test get_transaction_execution_status"""
        es = Etherscan(api_key=API_KEY)
        txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6',
                '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc',
                '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
        transaction_execution_status = es.get_transaction_execution_status(txns)
        time.sleep(1)
        self.assertIsInstance(transaction_execution_status, pd.DataFrame)

    ##### Blocks
    def test_get_block_reward(self):
        """Test get_block_reward"""
        es = Etherscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        block_rewards = es.get_block_reward(blocks)
        time.sleep(1)
        self.assertIsInstance(block_rewards, pd.DataFrame)

    def test_get_block_countdown(self):
        """Test get_block_countdown"""
        es = Etherscan(api_key=API_KEY)
        far_out_block = 50000000
        block_countdown = es.get_block_countdown(far_out_block)
        time.sleep(1)
        self.assertIsInstance(block_countdown, pd.DataFrame)

    def test_get_block_by_timestamp(self):
        """Test get_block_by_timestamp"""
        es = Etherscan(api_key=API_KEY)
        timestamp = 1638767557
        block_at_time = es.get_block_by_timestamp(timestamp)
        time.sleep(1)
        self.assertIsInstance(block_at_time, pd.DataFrame)

    ##### Logs
    def test_get_logs(self):
        """Test get_logs"""
        es = Etherscan(api_key=API_KEY)
        address = '0x33990122638b9132ca29c723bdf037f1a891a70c'
        from_block = 379224
        to_block = 'latest'
        topic0 = '0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545'
        logs = es.get_logs(address, from_block, to_block=to_block, topic0=topic0)
        time.sleep(1)
        self.assertIsInstance(logs, pd.DataFrame)

    ##### Geth/Parity Proxy
    def test_get_eth_block_number(self):
        """Test get_eth_block_number"""
        es = Etherscan(api_key=API_KEY)
        block_number = es.get_eth_block_number()
        time.sleep(1)
        self.assertIsInstance(block_number, int)

    def test_get_eth_block(self):
        """Test get_eth_block"""
        es = Etherscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        eth_blocks = es.get_eth_block(blocks)
        time.sleep(1)
        self.assertIsInstance(eth_blocks, pd.DataFrame)

    def test_get_eth_uncle(self):
        """Test get_eth_uncle"""
        es = Etherscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        blocks = [12989046]
        index = 0
        uncle = es.get_eth_uncle(blocks[0], index)
        time.sleep(1)
        #print('TODO')
        #print(uncle)
        self.assertIsInstance(uncle, Dict)

    def test_get_eth_block_transaction_count(self):
        """Test get_eth_block_transaction_count"""
        es = Etherscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        block_transaction_count = es.get_eth_block_transaction_count(blocks)
        time.sleep(1)
        self.assertIsInstance(block_transaction_count, pd.DataFrame)

    def test_get_eth_transaction_by_hash(self):
        """Test get_eth_transaction_by_hash"""
        es = Etherscan(api_key=API_KEY)
        txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6',
                '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc',
                '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
        txns_by_hash = es.get_eth_transaction_by_hash(txns)
        time.sleep(1)
        self.assertIsInstance(txns_by_hash, pd.DataFrame)

    def test_get_eth_transaction_by_block_index(self):
        """Test get_eth_transaction_by_block_index"""
        es = Etherscan(api_key=API_KEY)
        blocks = [13188647, 13088500]
        index = 0
        txn_info = es.get_eth_transaction_by_block_index(blocks[0], index)
        time.sleep(1)
        self.assertIsInstance(txn_info, pd.DataFrame)

    def test_get_eth_account_transaction_count(self):
        """Test get_eth_account_transaction_count"""
        es = Etherscan(api_key=API_KEY)
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        transaction_count = es.get_eth_account_transaction_count(accounts)
        time.sleep(1)
        self.assertIsInstance(transaction_count, pd.DataFrame)

    def test_get_eth_transaction_receipt(self):
        """Test get_eth_transaction_receipt"""
        es = Etherscan(api_key=API_KEY)
        txns = ['0x29f2df8ce6a0e2a93bddacdfcceb9fd847630dcd1d25ad1ec3402cc449fa1eb6',
                '0x0bd7f9af4f8ddb18a321ab0120a2389046b39feb67561d17378e0d4dc062decc',
                '0x1815a03dd8a1ce7da5a7a4304fa5fae1a8f4f3c20787e341eea230614e49ff61']
        receipts = es.get_eth_transaction_receipt(txns)
        time.sleep(1)
        self.assertIsInstance(receipts, pd.DataFrame)

    def test_get_eth_gas_price(self):
        """Test get_eth_gas_price"""
        es = Etherscan(api_key=API_KEY)
        gas_price = es.get_eth_gas_price()
        time.sleep(1)
        self.assertIsInstance(gas_price, int)

    ##### Tokens
    def test_get_token_total_supply(self):
        """Test get_token_total_supply"""
        es = Etherscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        total_supply = es.get_token_total_supply(tokens)
        time.sleep(1)
        self.assertIsInstance(total_supply, pd.DataFrame)

    def test_get_token_account_balance(self):
        """Test get_token_account_balance"""
        es = Etherscan(api_key=API_KEY)
        #pickle, xSushi
        tokens = ['0x429881672B9AE42b8EbA0E26cD9C73711b891Ca5',
                  '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272']
        # One account w/ the above tokens, one account w/out the above tokens
        accounts = ['0xBa19BdFF99065d9ABF3dF8CE942390B97fd71B12',
                    '0x503e4bfe8299D486701BC7bc7F2Ea94f50035daC']
        account_balance = es.get_token_account_balance(tokens, accounts)
        time.sleep(1)
        self.assertIsInstance(account_balance, pd.DataFrame)

    ##### Gas Tracker
    def test_get_est_confirmation(self):
        """Test get_est_confirmation"""
        es = Etherscan(api_key=API_KEY)
        gas_price_wei=2000000000
        est_confirmation = es.get_est_confirmation(gas_price_wei)
        time.sleep(1)
        self.assertIsInstance(est_confirmation, int)

    def test_get_gas_oracle(self):
        """Test get_gas_oracle"""
        es = Etherscan(api_key=API_KEY)
        gas_oracle = es.get_gas_oracle()
        time.sleep(1)
        self.assertIsInstance(gas_oracle, pd.DataFrame)

    ##### Stats
    def test_get_total_eth_supply(self):
        """Test get_total_eth_supply"""
        es = Etherscan(api_key=API_KEY)
        total_eth_supply = es.get_total_eth_supply()
        time.sleep(1)
        self.assertIsInstance(total_eth_supply, int)

    def test_get_total_eth2_supply(self):
        """Test get_total_eth2_supply"""
        es = Etherscan(api_key=API_KEY)
        total_eth2_supply = es.get_total_eth2_supply()
        time.sleep(1)
        self.assertIsInstance(total_eth2_supply, pd.DataFrame)

    def test_get_last_eth_price(self):
        """Test get_last_eth_price"""
        es = Etherscan(api_key=API_KEY)
        last_eth_price = es.get_last_eth_price()
        time.sleep(1)
        self.assertIsInstance(last_eth_price, pd.DataFrame)

    def test_get_nodes_size(self):
        """Test get_nodes_size"""
        es = Etherscan(api_key=API_KEY)
        start_date='2021-01-01'
        end_date='2021-01-05'
        nodes_size = es.get_nodes_size(start_date=start_date, end_date=end_date)
        time.sleep(1)
        self.assertIsInstance(nodes_size, pd.DataFrame)

    def test_get_total_nodes_count(self):
        """Test get_total_nodes_count"""
        es = Etherscan(api_key=API_KEY)
        total_nodes_count = es.get_total_nodes_count()
        time.sleep(1)
        self.assertIsInstance(total_nodes_count, int)

if __name__ == '__main__':
    unittest.main()
