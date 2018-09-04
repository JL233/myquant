import _thread
import concurrent
import datetime
import threading
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from pandas import DataFrame

from common.logger import logger
from common.mail import sendMail
from common.stockerror import StockError
from condition import bottom_bc, top_bc
from kdata.const import end_date_suffix_map
from common.env import Global, g
from service.strategy_srv.comm_excutor import executor, Need_Notify
from tdx import index

buy_cond = bottom_bc.bottom_bc
sell_cond = top_bc.top_bc


def bc_run(code, asset, freq, start_date_str,
           end_date_str):  # Overwrite run() method, put what you want the thread do here
    future_result_list = []

    g.ENV = Global()
    if isinstance(end_date_str, str):
        end_date = datetime.datetime.strptime(end_date_str + " " + end_date_suffix_map[freq],
                                              "%Y-%m-%d %H:%M:%S")
    g.ENV.code = code
    g.ENV.asset = asset
    g.ENV.freq = freq
    g.ENV.start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    g.ENV.end_date = end_date

    g.ENV.date = g.ENV.start_date
    index.__get_kdata__()
    future_list = []
    while True:
        logger.info("step into ：%s", g.ENV.date)

        f1 = executor.submit(buy_cond, g.ENV)
        f1.add_done_callback(done)
        future_list.append(f1)
        f2 = executor.submit(sell_cond, g.ENV)
        f2.add_done_callback(done)
        future_list.append(f2)

        try:
            g.ENV.date_increase()
        except StockError:
            logger.info("StockError: [%s]  !", str(g.ENV))
        except EOFError:
            logger.info("step to end: [%s] , it's over !", g.ENV.date)
            break
    for future in concurrent.futures.as_completed(future_list):
        res = future.result()
        if res[-1]:
            future_result_list.append([res[0],res[1],res[2],res[3]])
    return DataFrame(future_result_list)


# def add_record(self, obj):
#     res = obj.result()
#     if not res['ok']:
#         return
#
#     # 获取调用本函数的代码所在的方法：buy/sell
#     # op_type = traceback.extract_stack()[-2][2]
#     date = g.ENV.date
#     if not g.ENV.freq.endswith("min"):
#         date_str = g.ENV.date.strftime("%Y-%m-%d") + " 15:00"
#         date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
#     result_df.loc[date] = [res['op'], g.ENV.freq, res['name']]

def done(fn):
    if fn.cancelled():
        logger.error("%s: canceled", str(g.ENV))
    elif fn.done():
        error = fn.exception()
        if error:
            logger.error("%s: error returned:%s", str(g.ENV), error)
        else:
            result = fn.result()
            logger.info("%s: value returned:%s", str(g.ENV), result)
            # 如果需要通知+condition是否满足返回True+时间是今天
            if Need_Notify and result[-1] is True and result[0].date() == datetime.datetime.today().date():
                sendMail(str(result), str(g.ENV))
