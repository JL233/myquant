import datetime
import unittest

from common.env import Global, g
from tdx.func import FINDLOW, get_ma5
from tdx.index import get_close


class TestIndex(unittest.TestCase):
    def setUp(self):
        g.ENV = Global()
        g.ENV.date = datetime.datetime.now()
        print("do something before test.Prepare g.ENVironment.")

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_get_ma(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = 'D'
        m = get_ma5()
        print(m)
