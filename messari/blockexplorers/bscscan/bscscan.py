"""This module is meant to contain the BSCscan class"""


from messari.blockexplorers import Scanner

BASE_URL='https://api.bscscan.io/api'
class BSCscan(Scanner):
    """This class is a wrapper around the BSCscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)
