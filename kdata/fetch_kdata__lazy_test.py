import unittest

from kdata.fetch_kdata import *
from common.env import g, Global


class FetchKdataTest(unittest.TestCase):
    def setUp(self):
        g.ENV = Global()
        print("do something before test.Prepare g.ENVironment.")

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_fetch_kdata_lazy_day(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = '5min'
        df = fetch_kdata_lazy(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_5min(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = '5min'
        df = fetch_kdata_lazy(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_15min(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = '15min'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_30min(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = '30min'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_60min(self):
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        g.ENV.freq = '60min'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)
