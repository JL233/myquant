import unittest

from env import set_current
from tdx.index import get_close
from tdx.ref import REF


class TestRef(unittest.TestCase):
    def test_ref(self):
        set_current(freq_new='5')
        close = REF(get_close, 2)
        print(close)
        close=REF("get_close()", 2)
        print(close)
