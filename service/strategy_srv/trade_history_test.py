import datetime
import unittest

from pandas import DataFrame

from service.strategy_srv.trade_history import trade


class TestThread(unittest.TestCase):
    def setUp(self):
        self.result_df = DataFrame(columns=['买卖', '级别', "信号"])
        f = "%Y-%m-%d %H:%M:%S"
        date1 = datetime.datetime.strptime("2018-08-20 09:45:00", f)
        self.result_df.loc[date1] = ["buy", "5min", "bottom_bc"]
        self.result_df.loc[datetime.datetime.strptime("2018-08-20 09:45:00", f)] = ["buy", "15min", "bottom_bc"]
        self.result_df.append()
    def test_trade(self):
        trade(self.result_df)
