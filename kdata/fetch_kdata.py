import tushare as ts
from dateutil.relativedelta import relativedelta

from kdata.const import DT_FMT
from kdata.mongodb import *

cons = ts.get_apis()
ts.set_token('57f99adf4d80f67478dc33bdd091e8918ea199bbe4039e50ddace7f7')
pro = ts.pro_api()


def get_start_date(freq):
    return start_date_map[freq]


def fetch_kdata(code, asset, freq):
    start_date = get_start_date(freq)
    kdata = ts.bar(code, conn=cons, asset='INDEX', adj='qfq', freq=freq, start_date=start_date, end_date='')
    return insert_kdata(asset, freq, kdata)



def fetch_kdata_lazy(code, asset, freq,end_date=''):
    # global在第一行声明，养成好习惯
    global cons
    start_date = get_date_max(code, asset, freq) + relativedelta(minutes=1)
    if isinstance(end_date,datetime.datetime):
        end_date_str=end_date.strftime(DT_FMT).replace("11:30:00","13:00:00")
        end_date=datetime.datetime.strptime(end_date_str,DT_FMT)
    kdata = ts.bar(code, conn=cons, asset=asset, adj='qfq', freq=freq, start_date=start_date, end_date=end_date)
    result = 0
    try:
        result = insert_kdata(asset, freq, kdata)
    except pymongo.errors.BulkWriteError as err:
        logger.error(err)
    except StockError as err:
        logger.error(err)
    except TypeError as e:
        cons = ts.get_apis()
        logger.error(e)
    except Exception as e:
        logger.error(e)
    return result


def fetch_trade_cal():
    cal = pro.trade_cal(exchange_id='', start_date='20091231', end_date='20181231')
    return insert_trade_cal(cal)
