import random
import time


def uuid_generator(fixed_hex, as_string=True):
    """
    0x AAAA BBBB BBBB BBBB CCCC
    A - random
    B - timestamp
    c - fixed hex
    """

    fill = lambda s, l: f"{s:0>{l}}"

    fixed = int(fixed_hex, 16) if isinstance(fixed_hex, str) else fixed_hex
    random_hex = hex(random.getrandbits(16))[2:]
    timestamp_hex = hex(int(time.time() * 1000))[2:]
    fixed = hex(fixed)[2:]
    r = fill(random_hex, 4)+fill(timestamp_hex, 12)+fill(fixed, 4)
    if not as_string:
        r = int(r, 16)
    return r
