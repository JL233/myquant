import pandas

import pymongo
import pandas as pd
from pymongo import MongoClient
import tushare as ts
from pymongo.errors import BulkWriteError

from stockerror import StockError

ts.set_token("57f99adf4d80f67478dc33bdd091e8918ea199bbe4039e50ddace7f7")
client = MongoClient('localhost', 27017)
# getting a database
db = client.stock
k_data_sheets = {
    "5min": "k_data_05",
    "15min": "k_data_15",
    "30min": "k_data_30",
    "60min": "k_data_60",
    "D": "k_data_day",
    "W": "k_data_week",
    "M": "k_data_month",
    "5": "k_data_05",
    "15": "k_data_15",
    "30": "k_data_30",
    "60": "k_data_60",
    "D": "k_data_day",
    "W": "k_data_week",
    "M": "k_data_month",
}
index = [('code', pymongo.DESCENDING), ('freq', pymongo.DESCENDING), ('date', pymongo.DESCENDING),
         ('autype', pymongo.DESCENDING), ('index', pymongo.DESCENDING)]
for k in k_data_sheets:
    db[k_data_sheets[k]].ensure_index(index, unique=True)


def get_sheet(ktype):
    return db[k_data_sheets[ktype]]
def get_start_end(sheet):
    start=sheet.find().sort([("date",pymongo.ASCENDING)]).limit(1)
    end=sheet.find().sort([("date",pymongo.DESCENDING)]).limit(1)
    start=list(start)[0]["date"].split(" ")[0]
    end=list(end)[0]["date"].split(" ")[0]
    return start,end

# 或者db = client['users']
def get_k_data(code=None, start='', end='',
               freq='D',
               index=False):
    # sort:-1是降序，1是升序
    result = get_sheet(freq).find().sort([('date', pymongo.ASCENDING)])
    df = pd.DataFrame(list(result))
    if df.empty:
        print("df.empty")
        raise StockError("k_data is empty")
    return df


def insert_kdata(code, asset, freq, start, end):
    sheet=get_sheet(freq)
    cons = ts.get_apis()
    k_data =ts.bar(code, conn=cons, freq='5min', start_date='2016-01-01', end_date='',asset=asset)
    # 对DataFrame的个别列进行重命名
    k_data = k_data.rename(columns={'code': 'code_origin'})
    # 代码
    k_data['code'] = code
    # 周期
    k_data['freq'] = freq
    # 是否指数
    k_data['asset'] = asset
    k_data = k_data[['code', 'index', 'date', 'ktype', 'open', 'close', 'high', 'low', 'volume', 'code_origin']]
    # inplace默认为False,如果该值为False，那么原来的pd顺序没变，只是返回的是排序的
    k_data.sort_values("date", ascending=False, inplace=True)
    records = pandas.io.json.loads(k_data.T.to_json()).values()
    global insert_result
    insert_result=sheet.insert_many(records,ordered=False)
    # except BulkWriteError as e:
    #     print("insert_many出现重复，忽略错误")
    return insert_result
