import unittest

from kdata.fetch_kdata import fetch_kdata, fetch_trade_cal
from common.env import g, Global


# 在数据库还没创建的时候执行一次，以后就不要执行了
class FetchKdataTest(unittest.TestCase):
    def setUp(self):
        print("do something before test.Prepare g.ENVironment.")
        g.ENV = Global()
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'

    def tearDown(self):
        print("do something after test.Clean up.")

    # 从足够久的时间开始获取k线数据，直至最新
    def test_fetch_kdata_D(self):
        g.ENV.freq = 'D'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_5min(self):
        g.ENV.freq = '5min'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_15min(self):
        g.ENV.freq = '15min'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_30min(self):
        g.ENV.freq = '30min'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_kdata_60min(self):
        g.ENV.freq = '60min'
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_fetch_trade_cal(self):
        result = fetch_trade_cal()
        print(result)
