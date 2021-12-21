"""This module is meant to contain the EventMonitor class"""

import time
import logging
import queue
import threading
import json
from typing import Union, List, Dict
import pandas as pd

from web3 import Web3
from web3.logs import DISCARD

from messari.blockexplorers import Scanner
from .helpers import validate_checksum

#################
class EventMonitor:
    """Class to monitor contract events
    """

    def __init__(self, contracts_in: Union[str, List], explorer: Scanner, rpc_url: str):

        # More web3 setup
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.explorer = explorer

        # Web3 set up, can be super streamlined
        self.contracts = validate_checksum(contracts_in)
        self.contracts_df = self.get_contract_events()
        self.event_filters = [self.w3.eth.filter({'address': contract}) for contract in self.contracts]
        self.abis_dict = self.explorer.get_contract_abi(self.contracts)

        # For progress
        self.sync_status = ''

        # For shared data
        # TODO, fixing typing bc linting tool
        self.event_queue: queue.Queue = queue.Queue()
        self.events_list: List[Dict] = []
        # list of tuples for uniquely identifiying events that have been processed or not
        self.event_tuples: List[tuple] = []
        self.events_df = pd.DataFrame()

        # set flags to kill threads
        self.monitor_flag = False
        self.sync_flag = False
        self.handler_flag = False

        # threads
        self.monitor_thread = threading.Thread(target=self.monitor, args=())
        self.sync_thread = threading.Thread(target=self.sync, args=())
        self.handler_thread = threading.Thread(target=self.event_handler, args=())

    ##########################
    # HELPERS
    ##########################
    def get_events_df(self) -> pd.DataFrame:
        """Return all events as a DataFrame
        """
        events_df = pd.DataFrame(self.events_list)

        # create multiIndex (block#, log#)
        tuples_list = [(row['block_number'], row['log_index']) for index, row in events_df.iterrows()]
        event_index = pd.MultiIndex.from_tuples(tuples_list, names=['block_number', 'log_index'])

        # set & sort new index
        events_df.index = event_index
        events_df.sort_index(level=[0,1], inplace=True)

        return events_df

    def get_events_list(self) -> List:
        """Return all events as a List
        """
        return self.events_list

    def get_queue_size(self) -> int:
        """Return size of event queue
        """
        return self.event_queue.qsize()

    # TODO refactor this
    def get_contract_events(self) -> pd.DataFrame:
        """Return df about info of contract events
        """

        ABIs_dict = self.explorer.get_contract_abi(self.contracts)

        df_list = []
        for contract in self.contracts:

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

        event_df = pd.concat(df_list, keys=self.contracts, axis=1)
        return event_df

    ##########################
    # HANDLING
    ##########################
    def start_event_handler(self):
        """Start handler thread, do nothing if already started
        """
        self.handler_flag = True
        if self.handler_thread.is_alive():
            return
        self.handler_thread = threading.Thread(target=self.event_handler, args=())
        self.handler_thread.start()
        return

    def stop_event_handler(self):
        """Send flag to handler to end loop & thread
        """
        self.handler_flag = False

    def get_event_handler_status(self) -> str:
        """Return status of event handler thread
        """
        if self.handler_thread.is_alive():
            if self.handler_flag:
                return 'RUNNING'
            else:
                return 'STOPPING'
        else:
            if self.handler_flag:
                return 'CRASH'
            else:
                return 'DEAD'

    def event_handler(self):
        """Grab events from queue and pass to handler
        """
        # while monitoring, syncing, or queue not empty
        while self.handler_flag:
            while not self.event_queue.empty():
                event = self.event_queue.get()
                self.handle_event(event)
            time.sleep(2)

    def handle_event(self, event) -> pd.DataFrame:
        """Process event when it happens
        """
        # Look for repeats, txn hash & log index uniquely identify any event
        event_tuple = (event['transactionHash'], event['logIndex'])
        if event_tuple in self.event_tuples:
            # TODO, indicate this is working
            return


        # TODO, shouldn't need try-except error catching
        try:
            event_address = event['address']
            event_topics = [topic.hex() for topic in event['topics']]
            event_keccak = event_topics[0]

            sub_event_df = self.contracts_df[event_address]
            entry = sub_event_df.loc[sub_event_df['keccak'] == event_keccak]
            event_name = entry['name'].item()

            contract_abi = self.abis_dict[event_address]
            contract = self.w3.eth.contract(address=event_address, abi=contract_abi)

            txn = event['transactionHash']
            txn_rec = self.w3.eth.get_transaction_receipt(txn)

            # event_name is a member function of the contract contrusted w/ the
            # contract abi when initializing the contract. the weird __dict__ syntax
            # is the way to access this function
            logs = contract.events.__dict__[event_name]().processReceipt(txn_rec, errors=DISCARD)

            # logs is a tuple
            for log in logs:
                event_dict = {'args': dict(log['args']),
                              'event': log['event'],
                              'transaction': log['transactionHash'].hex(),
                              'log_index': log['logIndex'],
                              'transaction_index': log['transactionIndex'],
                              'address': log['address'],
                              'block_number': log['blockNumber'],
                              'block': log['blockHash'].hex()}
                self.events_list.append(event_dict)
                self.event_tuples.append(event_tuple)
        except:
            logging.error('event handler error')

        return


    ##########################
    # MONITORING
    ##########################
    def monitor(self):
        """Monitor for events & add to queue
        """
        while self.monitor_flag:
            for event_filter in self.event_filters:
                for event in event_filter.get_new_entries():
                    self.event_queue.put(event)
                    #self.handle_event(event)
            time.sleep(2)

    def start_monitor(self):
        """Start monitor thread, do nothing if already started
        """
        self.monitor_flag = True
        self.start_event_handler()
        if self.monitor_thread.is_alive():
            return

        self.monitor_thread = threading.Thread(target=self.monitor, args=())
        self.monitor_thread.start()
        return

    def stop_monitor(self):
        """Send flag to monitor to end loop & thread
        """
        self.monitor_flag = False

    def get_monitor_status(self) -> str:
        """Return status of event monitor thread
        """
        if self.monitor_thread.is_alive():
            if self.monitor_flag:
                return 'RUNNING'
            else:
                return 'STOPPING'
        else:
            if self.monitor_flag:
                return 'CRASH'
            else:
                return 'DEAD'

    ##########################
    # SYNCING
    ##########################
    # TODO fix defaults
    def start_sync(self, start: int = 0, end: Union[int, str] = 'latest'):
        """Start sync thread, do nothing if already started
        """
        self.sync_flag = True
        self.start_event_handler()
        if self.sync_thread.is_alive():
            return

        start_block = int(start)
        end_block = self.w3.eth.get_block('latest')['number'] if end == 'latest' else end

        self.sync_thread = threading.Thread(target=self.sync, args=(start_block, end_block))
        self.sync_thread.start()

    def stop_sync(self):
        """Send flag to monitor to end loop & thread
        """
        self.sync_flag = False

    def watch_sync(self):
        """Live watching & printing of the sync status. Be warned this is a blocking function
        """
        # Loop to monitor sync progress
        while self.sync_flag:
            print(self.sync_status)
            time.sleep(10)

    def get_sync_status(self) -> str:
        """Return status of sync thread
        """
        if self.sync_thread.is_alive():
            if self.sync_flag:
                return 'RUNNING'
            else:
                return 'STOPPING'
        else:
            if self.sync_flag:
                return 'CRASH'
            else:
                return 'DEAD'

    def sync(self, start_block: int, end_block: int):
        contract_total = len(self.contracts)
        contract_count = 1

        for contract in self.contracts:

            from_block = start_block
            # start w/ increments of 1% bc early eth blocks are pretty empty
            increment = (end_block - from_block) // 100
            to_block = from_block + increment

            run_filter = self.w3.eth.filter({'address': contract,
                                             'fromBlock': from_block,
                                             'toBlock': to_block})
            all_events = []
            events_caught = []
            while from_block < end_block and self.sync_flag:
                self.sync_status = f'Contract: {contract_count}/{contract_total}, Range: ({from_block} - {to_block}), Goal: {end_block}, Increment: {increment}'

                try:
                    events = run_filter.get_all_entries()
                    all_events.append(events)
                    for event in events:
                        # Add to queue
                        self.event_queue.put(event)

                    # Optimize increasing the increment
                    if len(events_caught) >= 10:
                        # pop new len(events) into list
                        events_caught.pop(0)
                        events_caught.append(len(events))

                        # get average
                        avg_caught = sum(events_caught)//10

                        diff = 5000 - avg_caught
                        diff_percent = diff/5000

                        # should work for +/- optimizing for 5000?
                        increment = int(increment * (1 + diff_percent))
                    else:
                        events_caught.append(len(events))
                        increment = increment

                    from_block = to_block + 1
                    to_block = from_block + increment
                    run_filter = self.w3.eth.filter({'address': contract,
                                                'fromBlock': from_block,
                                                'toBlock': to_block})

                except ValueError as error:
                    # TODO parse this error to confirm it is the right one
                    # really just assuming this error has to do w/ too much data being in return
                    #logging.error(error)
                    increment = increment // 2
                    to_block = from_block + increment

                    run_filter = self.w3.eth.filter({'address': contract,
                                                     'fromBlock': from_block,
                                                     'toBlock': to_block})
            contract_count+=1

        # self-stop sync w/ flag
        self.sync_flag = False
