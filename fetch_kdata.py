from dateutil.relativedelta import relativedelta

from stock_db.mongodb import insert_kdata
import stock_lib


def init_k_data(code, ktype, day):
    """
day表示每次取数据的时间段相隔几天，太长的话没那么多数据返回
5分钟的数据一次只返回三四百条
    """
    index = True
    for i in range(1):
        end = stock_lib.date
        start = end - relativedelta(days=day)
        print("i=", i, "end: ", end, ",start:", start)
        insertResult = insert_kdata(code, index, ktype, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        print("插入条数：", len(insertResult.inserted_ids))
        stock_lib.set_current(date_new=start)
