import _thread
import datetime
import sys
import threading
import traceback
from threading import Lock

from pandas import DataFrame

from common.logger import logger
from common.mail import sendMail
from common.stockerror import StockError
from common.env import g
from kdata.const import end_date_suffix_map



class Strategy(object):
    def __init__(self, buy_condition, sell_cond):
        self.Empty = True
        self.LastBuy = ''
        self.buy_cond = buy_condition
        self.sell_cond = sell_cond
        self.trade_list = DataFrame(columns=['买卖', '级别'])
        self.lock = threading.Lock()



    def start(self, code, asset, freq, start_date, end_date=datetime.datetime.now()):
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date+" "+end_date_suffix_map[freq], "%Y-%m-%d %H:%M:%S")
        g.ENV.code = code
        g.ENV.asset = asset
        g.ENV.freq = freq
        g.ENV.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        g.ENV.date = g.ENV.start_date
        g.ENV.end_date=end_date
        while g.ENV.date <= g.ENV.end_date:
            logger.info("step into ：%s", g.ENV.date)
            if self.buy_cond():
                self.buy()
            if self.sell_cond():
                self.sell()
            # time.sleep(1)
            try:
                g.ENV.date_increase()
            except StockError:
                break
            except EOFError:
                logger.info("step to end: [%s] , it's over !", g.ENV.date)
                return
