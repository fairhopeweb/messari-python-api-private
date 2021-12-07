"""This module is meant to contain the arbiscan class"""


from messari.blockexplorers import Scanner

BASE_URL='https://api.arbiscan.io/api'
class Arbiscan(Scanner):
    """This class is a wrapper around the arbiscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)
