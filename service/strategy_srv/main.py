import concurrent
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait
import pandas as pd
from pandas import DataFrame

from common.logger import logger
from kdata import const
from service.strategy_srv.bc_srv import bc_run
from service.strategy_srv.comm_excutor import executor
from service.strategy_srv.trade_history import trade

if __name__ == '__main__':
    freqs = ['D', '60min', '30min', '15min', '5min']
    freqs = ['5min']
    start_date_str = "2018-08-20"
    end_date_str = "2018-09-30"
    result_df = DataFrame(columns=['datetime','name', 'freq', "ok"])
    code = "000001"
    asset = const.BAR_ASSET_INDEX

    future_to_df = {executor.submit(bc_run, code, asset, freq, start_date_str, end_date_str): freq for freq in freqs}
    for future in concurrent.futures.as_completed(future_to_df):
        freq = future_to_df[future]
        try:
            logger.info("Is as_completed in mainThread：%r",
                        isinstance(threading.current_thread(), threading._MainThread))
            df = future.result()
            result_df = result_df.append(df,ignore_index=True)
        except Exception as e:
            print('%r generated an exception: %s' % (freq, e))
        else:
            print('%r freq is %d bytes' % (freq, len(df)))
    # executor.shutdown(wait=True)
    print("线程池全部结束")
    # 按照索引排序
    result_df.sort_values("datetime", inplace=True)
    print(result_df)
