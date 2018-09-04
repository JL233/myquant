import datetime
import unittest

from common.env import Global, g
from tdx.func import FINDLOW, BARSLAST, FINDHIGH, get_macd
from tdx.index import get_close


class TestRef(unittest.TestCase):
    def setUp(self):
        g.ENV = Global()
        g.ENV.date = datetime.datetime.now()
        print("do something before test.Prepare g.ENVironment.")

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_FINDLOW(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = 'D'
        m = FINDLOW(get_close, 0, 10, 1)
        print(m)

    def test_FINDHIGH(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = 'D'
        m = FINDHIGH(get_macd, 2, 3, 1)[1]
        print(m)

    def test_CROSS(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = 'D'
        m = BARSLAST('CROSS(get_ma10,get_ma5)')
        print(m)