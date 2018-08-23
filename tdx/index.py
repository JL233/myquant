
import talib
import mongodb as db
from env import ENV

from tdx.tdx_decorator import check


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
        return self.macd>other.macd
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.macd + other
        return self.macd + other.macd

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


# 返回结果是：
# 1、获取以ENV.date为结束时间的所有数据，按时间先后顺序排列
# 2、 将1中的数据尾部丢弃ENV.ref个数据
@check
def get_macd():
    k_data = db.get_k_data(ENV.code, freq=ENV.freq, index=True)
    k_data = k_data[:len(k_data) - ENV.ref]
    # if k_data.is:
    #     print("get_k_data返回為空",ENV.freq,ENV.code,ENV.date)
    #     return
    dif, dea, macd = talib.MACD(k_data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    disftance_list = []
    for i in range(0, len(macd)):
        tmp = MACD(macd.iloc[i] * 2, dif.iloc[i], dea.iloc[i])
        disftance_list.append(tmp)
    # result=MACD_OBJ(macd.tolist()[-1-interval]*2,dif.tolist()[-1-interval],dea.tolist()[-1-interval])
    return disftance_list[-1]


@check
def get_close():
    k_data = db.get_k_data(ENV.code, freq=ENV.freq, index=True)
    k_data = k_data[:len(k_data) - ENV.ref]
    return list(k_data['close'])[-1]
@check
def get_high():
    k_data = db.get_k_data(ENV.code, freq=ENV.freq, index=True)
    k_data = k_data[:len(k_data) - ENV.ref]
    return list(k_data['high'])[-1]
@check
def get_low():
    k_data = db.get_k_data(ENV.code, freq=ENV.freq, index=True)
    k_data = k_data[:len(k_data) - ENV.ref]
    return list(k_data['low'])[-1]