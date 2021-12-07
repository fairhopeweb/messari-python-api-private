"""This module is meant to contain the SnowTrace class"""


from messari.blockexplorers import Scanner

BASE_URL='https://api.snowtrace.io/api'
class SnowTrace(Scanner):
    """This class is a wrapper around the SnowTrace API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)
