"""This module is meant to contain the FTMscan class"""


from messari.blockexplorers import Scanner

BASE_URL='https://api.ftmscan.io/api'
class FTMscan(Scanner):
    """This class is a wrapper around the FTMscan API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)
