# Messari API
Messari provides a free API for crypto prices, market data metrics, on-chain metrics, and qualitative information (asset profiles).

This documentation will provide the basic steps to start using messari’s python library.

This repo is the private repo for internal use at Messari.
Features in the library may or may not be 100% ready for release to the public but they can be useful internally.

For any bugs, feature//integration requests, or asssistance reach out to:
Roberto Talamas or Michael Kremer on slack.

## Remote Install
To install the messari package remotely run this inside of any unix terminal:

```
$> pip install git+https://github.com/messari/messari-python-api-private.git
```


## Local Install
To install the messari package from the source:
```
$> git clone https://github.com/messari/messari-python-api-private.git
$> cd messari-python-api-private
messari-python-api-private$> python -m pip install -r requirements.txt
messari-python-api-private$> python setup.py install
```

## Quickstart
For a quick demo, you can try the following:
```
$> python
>>> from messari.timeseries import get_metric_timeseries
>>> assets = ['btc', 'eth']
>>> metric = 'price'
>>> start = '2020-06-01'
>>> end = '2021-01-01'
>>> timeseries_df = get_metric_timeseries(asset_slugs=assets, asset_metric=metric, start=start, end=end)
>>> print(timeseries_df)
```

## Docs
To open the offical docs go [here](https://objective-lalande-8ec88b.netlify.app/).

Examples can be found in [this](https://github.com/messari/messari-python-api/blob/master/examples/Messari%20API%20Tutorial.ipynb) Jupyter Notebook. 
