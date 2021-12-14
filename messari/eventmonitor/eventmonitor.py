import time
import threading
import json
import asyncio
from typing import Union, List, Dict
import pandas as pd

from web3 import Web3
from web3.logs import DISCARD
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/679f03cb2c4a4853b6aa19e44600dfc9'))

from messari.blockexplorers import Etherscan
from messari.utils import validate_input
API_KEY='DWC3QGAEHNFQQM55Z1AYTXUTZ1GPBK51JQ'
ES = Etherscan(api_key=API_KEY)

cETH = Web3.toChecksumAddress('0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5')
cDAI = Web3.toChecksumAddress('0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643')
cUSDC = Web3.toChecksumAddress('0x39aa39c021dfbae8fac545936693ac917d5e7563')
DAI= Web3.toChecksumAddress('0x6B175474E89094C44Da98b954EedeAC495271d0F')
contracts = [cETH, cDAI, cUSDC, DAI]


#################

class EventMonitor:
    """Class to monitor contract events
    """

    def __init__(self, contracts_in: Union[str, List]):
        self.contracts = self.validate_checksum(contracts_in)
        self.event_df = self.get_contract_events(self.contracts)
        self.event_filters = [w3.eth.filter({'address': contract}) for contract in self.contracts]
        self.abis_dict = ES.get_contract_abi(contracts)

        self.run = pd.DataFrame()

        # set flags to false
        self.monitoring_flag = False
        self.syncing_flag = False

    # TODO, make this a helper
    def validate_checksum(self, hex_in: Union[str, List]) -> List:
        list_in = validate_input(hex_in)
        list_out = []
        for item in list_in:
            list_out.append(Web3.toChecksumAddress(item))
        return list_out

    def get_contract_events(self, contracts_in: Union[str, List]) -> pd.DataFrame:
        """Return df about info of contract events
        """

        contracts = validate_input(contracts_in)
        ABIs_dict = ES.get_contract_abi(contracts)

        df_list = []
        for contract in contracts:

            contract_ABI = json.loads(ABIs_dict[contract])

            # loop through abi
            event_list=[]
            for entry in contract_ABI:
                # looking for events
                if entry['type'] == 'event':
                    # get name & inputs
                    event_name = entry['name']
                    event_inputs = entry['inputs']

                    # Some ugly string manipulation
                    input_str='('
                    for event_input in event_inputs:
                        input_str += f"{event_input['type']},"
                    input_str = input_str[:-1] + ')'

                    # create text to get event keccak
                    event_text = event_name+input_str
                    event_keccak = Web3.keccak(text=event_text).hex()

                    # making df
                    event_dict = {'name': event_name,
                                  'text': event_text,
                                  'keccak': event_keccak,
                                  'inputs': event_inputs}
                    event_list.append(event_dict)

            contract_event_df = pd.DataFrame(event_list)
            df_list.append(contract_event_df)

        event_df = pd.concat(df_list, keys=contracts, axis=1)
        return event_df

    def handle_event(self, event) -> pd.DataFrame:
        event_address = event['address']
        event_topics = [topic.hex() for topic in event['topics']]
        event_keccak = event_topics[0]

        sub_event_df = self.event_df[event_address]
        entry = sub_event_df.loc[sub_event_df['keccak'] == event_keccak]
        event_name = entry['name'].item()

        contract_abi = self.abis_dict[event_address]
        contract = w3.eth.contract(address=event_address, abi=contract_abi)

        txn = event['transactionHash']
        txn_rec = w3.eth.get_transaction_receipt(txn)

        # event_name is a member function of the contract contrusted w/ the
        # contract abi when initializing the contract. the weird __dict__ syntax
        # is the way to access this function
        logs = contract.events.__dict__[event_name]().processReceipt(txn_rec, errors=DISCARD)
        # logs is a tuple
        d_list = []
        for log in logs:
            event_dict = {'args': dict(log['args']),
                          'event': log['event'],
                          'transaction': log['transactionHash'].hex(),
                          'log_index': log['logIndex'],
                          'transaction_index': log['transactionIndex'],
                          'address': log['address'],
                          'block_number': log['blockNumber'],
                          'block': log['blockHash'].hex()}
            d_list.append(event_dict)
        event_df = pd.DataFrame(d_list)
        return event_df

    def monitor(self):
        events_df = pd.DataFrame()
        while self.monitoring_flag:
            for event_filter in self.event_filters:
                for event in event_filter.get_new_entries():
                    event_df = self.handle_event(event)
                    events_df = pd.concat([events_df, event_df])
                    self.run = pd.concat([self.run, event_df])
            time.sleep(2)
        print('done monitoring')
        return

    def start_monitor(self) -> threading.Thread:
        self.monitoring_flag = True
        monitor_thread = threading.Thread(target=self.monitor, args=())
        monitor_thread.start()
        return monitor_thread

    def stop_monitor(self):
        self.monitoring_flag = False

    def get_history(self):
        for event_filter in self.event_filters:
            print("getting all")
            events = event_filter.get_all_entries()
            print(events)
            print("done")

WAIT_TIME = 2
em = EventMonitor(contracts)
#em.get_history()
monitor_thread = em.start_monitor()
