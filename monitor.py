import datetime

import tushare as ts
from dateutil.relativedelta import relativedelta

def rule1(stock,date_str):
    start_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    start = (start_date - relativedelta(days=10)).strftime("%Y-%m-%d")
    data_dict=ts.get_hist_data(stock,start=start,end=date_str)
    v_ma5=data_dict['v_ma5'][0]
    v_ma10=data_dict['v_ma10'][0]
    v_ma5_yesterday=data_dict['v_ma5'][1]
    v_ma10_yesterday=data_dict['v_ma10'][1]
    if v_ma5<v_ma10 or (v_ma5<v_ma5_yesterday and v_ma10<v_ma10_yesterday):
        return False
    return True
    print(v_ma5,v_ma10)
print(rule1('300009','2017-11-21'))

