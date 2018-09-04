import unittest
from _ast import Global

from kdata import const
from kdata.const import BAR_ASSET_INDEX
from kdata.fetch_kdata import *
from kdata.mongodb import *
from common.env import g


class MongodbTest(unittest.TestCase):
    def setUp(self):
        g.ENV = Global()
        print("do something before test.Prepare g.ENVironment.")

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_check_data(self):
        check_data()

    def test_get_date_max(self):
        code = "000001"
        freq = "5min"
        result = get_date_max(code, const.BAR_ASSET_INDEX, freq)
        print(result)

    def test_get_date_min(self):
        code = "000001"
        freq = "60min"
        result = get_date_min(code, BAR_ASSET_INDEX, freq)
        print(result)

    def test_fetch_kdata(self):
        df = fetch_kdata(g.ENV.code, g.ENV.asset, g.ENV.freq)
        print(df)

    def test_get_kdata(self):
        df = get_kdata('000001', '30min', const.BAR_ASSET_INDEX, )
        print(df)

    def test_get_date_next(self):
        df = get_date_next((datetime.datetime.now() - relativedelta(days=10)),
                           '000001', const.BAR_ASSET_INDEX, '30min')
        print(df)

    def test_get_trade_cal_max(self):
        print(get_trade_cal_max())

    def test_get_close_by_date(self):
        date_str = "2018-08-30 09:50:00"
        print(get_close_by_date('000001',BAR_ASSET_INDEX, datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")))
