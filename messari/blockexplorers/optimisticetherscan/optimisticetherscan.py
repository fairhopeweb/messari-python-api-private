"""This module is meant to contain the OptimisticEtherscan class"""


from messari.blockexplorers import Scanner

BASE_URL='https://api-optimistic.etherscan.io/api'
class OptimisticEtherscan(Scanner):
    """This class is a wrapper around the OptimisticEtherscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)
