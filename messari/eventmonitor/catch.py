import time
import json
import asyncio
import logging
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


current_block_number = w3.eth.get_block('latest')['number']
print(f'current block is {current_block_number}')


from_block = 0
# start w/ increments of 1% bc early eth blocks are pretty empty
increment = current_block_number // 100
to_block = from_block + increment

run_filter = w3.eth.filter({'address': cETH,
                             'fromBlock': from_block,
                             'toBlock': to_block})

#13804739

all_events=[]
events_caught = []
while from_block < current_block_number:
    print(f'from {from_block} to {to_block}, inc {increment}')

    try:
        events = run_filter.get_all_entries()
        all_events.append(events)
        print(f'found {len(events)} events')

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
        run_filter = w3.eth.filter({'address': cETH,
                                    'fromBlock': from_block,
                                    'toBlock': to_block})

    except ValueError as error:
        # TODO parse this error to confirm it is the right one
        # really just assuming this error has to do w/ too much data being in return
        logging.error(error)
        increment = increment // 2
        to_block = from_block + increment

        run_filter = w3.eth.filter({'address': cETH,
                                    'fromBlock': from_block,
                                    'toBlock': to_block})


