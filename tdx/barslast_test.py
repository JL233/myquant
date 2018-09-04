import unittest

from tdx.g.ENV import set_current
from tdx.barslast import barslast


class Barslast_Test(unittest.TestCase):
    def test_barslast_cross_macd(self):
        set_current("000001",'5')
        str="get_macd()>0 and tdx_ref('get_macd()<0',1)"
        result=barslast(str)
        print(result)