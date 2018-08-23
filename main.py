import tushare as ts
import datetime
from dateutil.relativedelta import relativedelta

import strategy
from stock_lib import utils
import time

def test_ztb():
    # utils.get_stock_basics()
    all_stocks = ts.get_stock_basics()
    for index, row in all_stocks.iterrows():  # 获取每行的index、row
        # print(index)  # 第一列，股票代码
        # index:是否为指数：默认为False,设定为True时认为code为指数代码
        # start:开始日期format：YYYY-MM-DD 为空时取当前日期
        kdata = ts.get_k_data(index, index=False, start=T_pre, end=T)
        try:
            if utils.is_ztb(kdata.iloc[-2], kdata.iloc[-1]):
                if not kdata.iloc[-1]['close'] == kdata.iloc[-1]['open']:
                    print(index)
        except IndexError:
            # print(index+'k线数据不足')
            pass


def run_strategy_2shadow():
    all_stocks = ts.get_stock_basics()
    for index, row in all_stocks.iterrows():  # 获取每行的index、row
        # print(index)  # 第一列，股票代码
        # index:是否为指数：默认为False,设定为True时认为code为指数代码
        # start:开始日期format：YYYY-MM-DD 为空时取当前日期
        kdata = ts.get_k_data(index, index=False, start=T_pre, end=T)
        if index=='002819':
            print('')
        try:
            if utils.is_shadow_down(kdata.iloc[-1]) and utils.is_shadow_down(kdata.iloc[-2]):
                print(index)
        except IndexError:
            # print(index+'k线数据不足')
            pass

def run_strategy_ztb_2day():
    all_stocks = utils.get_stock_basics()
    print("获取股票总数：" + str(len(all_stocks.index)))
    for index, row in all_stocks.iterrows():  # 获取每行的index、row

        if strategy.ztb_2day(index, T):
            print(index)

            # est_shadow()
            # kdata = ts.get_k_data('002419', index=False, start=T_pre, end=T)
            # print(utils.is_shadow_down(kdata.iloc[-1]))


def run_money_in_double():
    all_stocks = utils.get_stock_basics()
    print("获取股票总数：" + str(len(all_stocks.index)))
    for index, row in all_stocks.iterrows():  # 获取每行的index、row
        if strategy.money_in_double(index, T):
            print(index)
            time.sleep(1)
def run_money_in_double():
    all_stocks = utils.get_stock_basics()
    print("获取股票总数：" + str(len(all_stocks.index)))
    for index, row in all_stocks.iterrows():  # 获取每行的index、row
        if strategy.money_in_double(index, T):
            print(index)
            time.sleep(1)
def run_strategy_common(f,wait=0):
    all_stocks = utils.get_stock_basics()
    print("获取股票总数：" + str(len(all_stocks.index)))
    for index, row in all_stocks.iterrows():  # 获取每行的index、row
        time.sleep(wait)
        if f(index, T):
            print(index)
T='2017-05-04'
T_date= datetime.datetime.strptime(T, "%Y-%m-%d")
T_pre_date=T_date - relativedelta(days=10)
T_pre=T_pre_date.strftime("%Y-%m-%d")

if __name__ == '__main__':
    #mas=utils.getMa("600846")
    print(utils.MA(5))