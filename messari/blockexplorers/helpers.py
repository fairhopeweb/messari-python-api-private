"""This module is dedicated to helpers for the Scanners class"""

from typing import List, Union
from messari.utils import validate_int

def int_to_hex(ints_in: Union[int, List]) -> List[str]:
    """Converts a lits of integers to a list of hex strings '0x'
    """
    ints = validate_int(ints_in)
    hex_out = []
    for int_in in ints:
        hex_out.append(hex(int_in))
    return hex_out
