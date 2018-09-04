import datetime
import time

import pandas

import pymongo
import pandas as pd
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient

from common.logger import logger
from common.stockerror import StockError
from kdata.const import start_date_map, BAR_ASSET_INDEX

client = MongoClient('localhost', 27017)
# getting a database
db = client.stock
kdata_sheets = {
    "5min": "k_data_5",
    "15min": "k_data_15",
    "30min": "k_data_30",
    "60min": "k_data_60",
    "D": "k_data_day",
    "W": "k_data_week",
    "M": "k_data_month",
}
# 建立联合唯一索引：code+datetime
index_kdata = [('code', pymongo.DESCENDING), ('datetime', pymongo.DESCENDING), ]
index_trade_cal = [('datetime', pymongo.DESCENDING), ]
collectionlist = db.collection_names()
for collection in collectionlist:
    if collection.startswith('k_data'):
        logger.debug("表%s建立联合唯一索引: %s", collection, index_kdata)
        db[collection].ensure_index(index_kdata, unique=True)
    if collection == "trade_cal":
        logger.debug("表%s建立联合唯一索引: %s", collection, index_trade_cal)
        db[collection].ensure_index(index_trade_cal, unique=True)


def get_sheet(asset, freq):
    sheet_name = kdata_sheets[freq]
    if asset != '':
        sheet_name = sheet_name + "_" + str(asset)
    return db[sheet_name]


def get_start_end(sheet):
    start = sheet.find().sort([("date", pymongo.ASCENDING)]).limit(1)
    end = sheet.find().sort([("date", pymongo.DESCENDING)]).limit(1)
    start = list(start)[0]["date"].split(" ")[0]
    end = list(end)[0]["date"].split(" ")[0]
    return start, end


# 或者db = client['users']
def get_kdata(code, freq, asset, start=None, end=None, ):
    if start is None:
        start = start_date_map[freq]
    if end is None:
        end = datetime.datetime.today()
    if isinstance(start, datetime.datetime):
        start = start.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(end, datetime.datetime):
        end = end.strftime('%Y-%m-%d %H:%M:%S')
    # sort:-1是降序，1是升序
    result = get_sheet(asset, freq).find({"日期": {"$gte": start, "$lte": end},
                                          "code": code}).sort([('datetime', pymongo.DESCENDING), ])
    result_list = list(result)
    df = pd.DataFrame(result_list)
    if df.empty:
        print("get_kdata df.empty", code, freq, asset, start, end)
        raise StockError("kdata is empty")
    return df


def insert_kdata(asset, freq, kdata):
    if kdata is None:
        raise TypeError("kdata is None when insert_kdata")
    if kdata.empty:
        raise ValueError("kdata is Empty when insert_kdata")
    # 对DataFrame的个别列进行重命名
    # k_data = k_data.rename(columns={'code': 'code_origin'})
    # 代码
    # k_data['code'] = code
    # 周期
    kdata['freq'] = freq
    kdata['datetime'] = kdata.index
    kdata['datetime'] = kdata['datetime'].apply(
        lambda x: x - relativedelta(minutes=150) if x.strftime('%Y-%m-%d %H:%M:%S').endswith("13:00:00") else x)
    kdata['日期'] = kdata['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    # 盘中tushare返回的11:30的k线时间是13:00，这里手动维持数据正确性
    kdata.replace("13:00:00", "11:30:00", inplace=True)
    # 没用，还是datetime
    # kdata['datetime'] = pd.to_datetime(kdata.index, unit='ms')
    kdata = kdata[['code', '日期', 'open', 'close', 'high', 'low', 'vol', 'amount', 'p_change', 'freq', 'datetime']]
    # inplace默认为False,如果该值为False，那么原来的pd顺序没变，只是返回的是排序的
    kdata = kdata.sort_values("datetime", ascending=True, inplace=False)
    records = pandas.io.json.loads(kdata.T.to_json()).values()
    # ordered=False，如果插入某条时出现错误，其他记录也会被尽可能的插入
    insert_result = get_sheet(asset, freq).insert_many(records, ordered=True)
    insert_count = len(insert_result.inserted_ids)
    return insert_count


def get_date_max(code, asset='', freq='', sheet=None):
    if sheet is None:
        sheet = get_sheet(asset, freq)
    cursor = sheet.find({"code": code}).sort([('datetime', pymongo.DESCENDING), ]).limit(1)
    try:
        one = list(cursor)[0]
    except IndexError as e:
        return datetime.datetime.strptime(start_date_map[freq], '%Y-%m-%d')
    max_date = pd.to_datetime(one['datetime'], unit='ms')
    return max_date


def get_date_min(code, asset='', freq='', sheet=None):
    if sheet is None:
        sheet = get_sheet(asset, freq)
    cursor = sheet.find({"code": code}).sort([('datetime', pymongo.ASCENDING)]).limit(3)
    try:
        one = list(cursor)[0]
    except IndexError as e:
        return None
    max_date = pd.to_datetime(one['datetime'], unit='ms')
    return max_date


def get_date_next(dt, code, asset, freq, sheet=None):
    dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

    if sheet is None:
        sheet = get_sheet(asset, freq)
    cursor = sheet.find({"code": code, '日期': {'$gt': dt_str}}).sort([('datetime', pymongo.ASCENDING)]).limit(1)
    try:
        one = list(cursor)[0]
    except IndexError as e:
        return None
    if one is None:
        return None
    max_date = pd.to_datetime(one['datetime'], unit='ms')
    return max_date


def check_data():
    df = pd.DataFrame(columns=['记录数', 'start_date', 'end_date'])
    collectionlist = db.collection_names()
    for collection in collectionlist:
        for code in db[collection].distinct("code"):
            df.loc[collection] = [db[collection].find().count(),
                                  get_date_min(code, sheet=db[collection]),
                                  get_date_max(code, sheet=db[collection])]
    print(df)


def get_close_by_date(code,asset,date):
    date_str=date.strftime("%Y-%m-%d %H:%M:%S")
    cursor = get_sheet(asset, '5min').find({"code": code,'日期':date_str}).limit(1)
    try:
        one = list(cursor)[0]
    except IndexError as e:
        return None
    else:
        return one['close']

def insert_trade_cal(df):
    if df is None:
        raise StockError("[insert_trade_cal] 参数 df==None")
    df['datetime'] = pd.to_datetime(df['cal_date'], format='%Y%m%d')
    df = df.rename(columns={'cal_date': '日期'})
    df['日期'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df = df.sort_values("datetime", ascending=False, inplace=False)
    records = pandas.io.json.loads(df.T.to_json()).values()
    # ordered=False，如果插入某条时出现错误，其他记录也会被尽可能的插入
    insert_result = db["trade_cal"].insert_many(records, ordered=False)
    insert_count = len(insert_result.inserted_ids)
    return insert_count


def get_trade_cal_max():
    one = db["trade_cal"].find_one()
    if one is None:
        return None
    max_date = one['datetime']
    return max_date


def get_next_trade_cal(dt):
    """
    :param dt:
    :return: 下一个交易日期，datetime格式
    """
    dt_str = dt.strftime('%Y-%m-%d')
    cursor = db["trade_cal"].find({'日期': {'$gt': dt_str}, 'is_open': 1}).sort([('datetime', pymongo.ASCENDING)]).limit(
        1)

    one = list(cursor)[0]
    next_date = pd.to_datetime(one['datetime'], unit='ms')
    return next_date
