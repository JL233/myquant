import unittest

from env import set_current
from tdx.index import get_macd_df, get_macd
from tdx.sum import tdxSum





class Sum_Test(unittest.TestCase):
    def testSumMacd(self):
        set_current("000001", '5')
        result = tdxSum(get_macd, 3)
        print(result)
    def testRefSumMacd(self):
        set_current("000001", '5')
        result = tdxRef(tdxSum(get_macd(), 3),1)
        print(result)

