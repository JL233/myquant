import datetime
import threading
import time

from dateutil.relativedelta import relativedelta

from common.logger import logger

from _threading_local import local
from kdata import mongodb


class Global:
    def __init__(self):
        self.code = ''
        self.freq = 'D'
        self.date = None
        self.ref = 0
        self.asset = ''
        # 格式是datetime
        self.start_date = None
        # 格式是datetime
        self.end_date = None
        self.kdata = None

    def date_increase(self):
        # 从数据库取下一根k线
        next_dt = mongodb.get_date_next(self.date, self.code, self.asset, self.freq)
        if next_dt is None:
            logger.info("run out of kdata")
        while next_dt is None:
            if g.ENV.date >= g.ENV.end_date:
                raise EOFError
            # 过5分钟再去取
            time.sleep(300)
            next_dt = mongodb.get_date_next(self.date, self.code, self.asset, self.freq)
        self.date = next_dt

    def __str__(self):
        return "当前代码：%s, 当前周期:%s, " \
               "当前时间:%s " % (self.code, self.freq, self.date)


g = threading.local()


# todo 形参默认值引用全局变量引用不到
def set_current(code_new='', freq_new='', date_new='', asset=''):
    if code_new != "":
        g.ENV.code = code_new
    if freq_new != "":
        g.ENV.freq = freq_new
    if date_new != "":
        g.ENV.date = date_new
    g.ENV.asset = asset
    print("set_current", g.ENV.code, g.ENV.freq, g.ENV.date, g.ENV.asset)


def ser_ref(ref):
    g.ENV.ref = ref
