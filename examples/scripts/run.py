
import requests
import pandas as pd
import json
from string import Template

from messari.defillama import DeFiLlama
dl = DeFiLlama()

CHAIN_URL = Template('https://defillama.com/_next/data/mDaYGJz3iJDOSw9H7xWVG/chain/$chain.json')

###### specify chain and number of top N protocols on chain
chain = 'Solana'
N = 3

endpoint_url = CHAIN_URL.substitute(chain=chain)


###### ohhhh boy this is goooood
# this gets a tvl breakdown by protocol on specific chain
# data is localized to chain
page_props = requests.get(endpoint_url).json()['pageProps']
protocols_df = pd.DataFrame(page_props['filteredProtocols'])
protocols_df.sort_values('tvl', ascending=False, inplace=True)

###### now get top N names -- convert to slugs
top_N = protocols_df.iloc[0:N]

protocols_df = dl.get_protocols()
names = protocols_df.loc['name'].tolist()
slugs = protocols_df.loc['slug'].tolist()
name_to_slugs = dict(zip(names, slugs))

top_N_names = top_N['name'].tolist()

slugs = [name_to_slugs[name] for name in top_N_names]


#protocol_tvls_df = dl.get_protocol_tvl_timeseries(top_N_names)
protocol_tvls_df = dl.get_protocol_tvl_timeseries(slugs)
final = protocol_tvls_df.xs(chain, axis=1, level=1)
print(final)
