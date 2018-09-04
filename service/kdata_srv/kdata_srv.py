import datetime
import threading
import time

from common.logger import logger
from kdata import const
from kdata import *
from kdata.fetch_kdata import fetch_kdata_lazy
from kdata.mongodb import get_date_max, get_next_trade_cal
from dateutil.relativedelta import relativedelta

freq_wait_second = {
    # 5分钟
    "5min": 60 * 5,
    "15min": 60 * 5,
    "30min": 60 * 5,
    "60min": 60 * 5,
    "D": 60 * 60,
    "W": 60 * 60,
    "M": 6060,
}


class KdataThread(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self, code, asset, freq):
        threading.Thread.__init__(self, name="%s_%s_%s_%s" % (self.__class__.__name__, code, asset, freq))
        self.code = code
        self.asset = asset
        self.freq = freq
        self.kdata_date_next = None

    def run(self):  # Overwrite run() method, put what you want the thread do here
        while True:
            kdata_date_max = get_date_max(self.code, self.asset, self.freq)

            # 00:00结尾只有可能是日、周、月等周期
            if kdata_date_max.strftime('%H:%M') == '00:00':
                self.kdata_date_next = get_next_trade_cal(kdata_date_max) + relativedelta(hours=15)
            # 15:00结尾只有可能是分钟周期
            elif kdata_date_max.strftime('%H:%M') == '15:00':
                # 如果下一个k线不是今天，那么是下一个交易日
                date_str = get_next_trade_cal(kdata_date_max).strftime('%Y-%m-%d') + " 9:30"
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                self.kdata_date_next = date + \
                                       relativedelta(minutes=int(self.freq.replace('min', '')))
            elif kdata_date_max.strftime('%H:%M') == '11:30':
                # 如果下一个k线是上午最后一根，跳到下午1点
                date_str = kdata_date_max.strftime('%Y-%m-%d') + " 13:00"
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                self.kdata_date_next = date + \
                                       relativedelta(minutes=int(self.freq.replace('min', '')))
            else:
                self.kdata_date_next = kdata_date_max + \
                                       relativedelta(minutes=int(self.freq.replace('min', '')))

            logger.info("下一根K线时间是：%s ", self.kdata_date_next)
            seconds = (datetime.datetime.now() - self.kdata_date_next).total_seconds()

            if seconds > freq_wait_second[self.freq]:
                logger.info("发现新数据，无需等待，call def fetch_kdata_lazy now.", )
                result = fetch_kdata_lazy(self.code, self.asset, self.freq, end_date=self.kdata_date_next)
                if result < 1:
                    logger.error("取[%s]的k线数据失败", self.kdata_date_next.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    logger.info("取[%s]的k线数据%d条成功", self.kdata_date_next.strftime('%Y-%m-%d %H:%M:%S'), result)
            elif 0 < seconds < freq_wait_second[self.freq]:
                logger.info("发现新数据，需要等待%d秒.", seconds)
                time.sleep(seconds)
            else:
                logger.info("尚未产生新数据，睡眠直至%s", self.kdata_date_next)
                time.sleep(abs(seconds))

    def stop(self):
        self.thread_stop = True
