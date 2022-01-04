
import requests
import pandas as pd
from string import Template
import sys

import argparse

from messari.defillama import DeFiLlama
from messari.utils import validate_input


dl = DeFiLlama()

CHAIN_URL = Template('https://defillama.com/_next/data/mDaYGJz3iJDOSw9H7xWVG/chain/$chain.json')



# Set up argparse
parser = argparse.ArgumentParser(description="A function built to give a detailed breakdown of a specific chain's TVL")
parser.add_argument('-c', '--chain', help='chain to recieve TVL for')
parser.add_argument('-s', '--start', help='start date used to filter results')
parser.add_argument('-e', '--end', help='end date used to filter results')
arguments = parser.parse_args()

# get chain name
if arguments.chain is not None:
    protocols = validate_input(arguments.chain)
else:
    sys.exit()

#### Get start & end date
if arguments.start is not None:
    start = arguments.start
else:
    start = None
if arguments.end is not None:
    end = arguments.end
else:
    end = None
