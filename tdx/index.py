import functools

import talib
from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from common.logger import logger
from kdata import mongodb as db
from kdata.const import freq_value_map
from common.env import g

from tdx.tdx_decorator import check, index_round


class MACD(object):
    def __init__(self, macd, dif, dea):
        self.macd = round(macd, 2)
        self.dif = round(dif, 2)
        self.dea = round(dea, 2)

    def __lt__(self, other):
        if isinstance(other, (int, float)):
            return self.macd < other
        return self.macd < other.macd

    def __gt__(self, other):
        if isinstance(other, (int, float)):
            return self.macd > other
        return self.macd > other.macd

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.macd + other
        return self.macd + other.macd

    def __radd__(self, other):
        if other == 0:
            return self.macd
        else:
            return self.__add__(other)

    def __str__(self):
        return "macd: %s    dif:%s  dea:%s" % (self.macd, self.dif, self.dea)


def get_dif():
    macd = get_macd()
    return macd.dif


def get_dif():
    macd = get_macd()
    return macd.dea


def __set_macd__():
    # 注意：talib.MACD传入的k线的日期必须是从小到大排列
    dif, dea, macd = talib.MACD(g.ENV.kdata['close'][::-1], fastperiod=12, slowperiod=26, signalperiod=9)
    disftance_list = []
    for i in range(0, len(macd)):
        tmp = MACD(macd.iloc[i] * 2, dif.iloc[i], dea.iloc[i])
        disftance_list.append(tmp)
    disftance_list.reverse()
    g.ENV.kdata['macd'] = disftance_list


def __set_ma__(col_name, x):
    # 注意：talib.MACD传入的k线的日期必须是从小到大排列
    ma_series = talib.SMA(g.ENV.kdata[col_name][::-1], x)
    g.ENV.kdata['ma' + str(x)] = ma_series


@check
def __get_kdata__():
    if g.ENV.kdata is None:
        logger.info("g.ENV.kdata is None，init kdata")
        freq = g.ENV.freq
        start = g.ENV.date - relativedelta(days=(365 * 3 / freq_value_map['D']) * freq_value_map[freq])
        end = g.ENV.end_date
        g.ENV.kdata = db.get_kdata(g.ENV.code, freq=freq, asset=g.ENV.asset, start=start, end=end)
        __set_macd__()
        __set_ma__('close', 5)
        __set_ma__('close', 10)
        __set_ma__('close', 20)
        __set_ma__('close', 60)
        __set_ma__('close', 120)

    # 先根据当前时间g.ENV.date筛选日期
    kdata = g.ENV.kdata[(g.ENV.kdata.日期 <= g.ENV.date.strftime('%Y-%m-%d %H:%M:%S'))]
    # 先根据当前时间g.ENV.ref截取
    kdata = kdata[g.ENV.ref:]
    return kdata


def __get_index__(column):
    k_data = __get_kdata__()
    # 因为kdata是按时间从大到小排列的
    # 返回第一个，即当前时间、REF决定的top1
    return list(k_data[column])[0]


# 偏函数
get_close = functools.partial(__get_index__, column='close')
get_high = functools.partial(__get_index__, column='high')
get_low = functools.partial(__get_index__, column='low')
get_open = functools.partial(__get_index__, column='open')
get_ma5 = functools.partial(__get_index__, column='ma5')
get_ma10 = functools.partial(__get_index__, column='ma10')
get_ma20 = functools.partial(__get_index__, column='ma20')
get_ma60 = functools.partial(__get_index__, column='ma60')
get_ma120 = functools.partial(__get_index__, column='ma120')
get_macd = functools.partial(__get_index__, column='macd')
