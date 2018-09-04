from kdata.const import start_date_map

from common.stockerror import StockError
from common.env import g


def check(func):
    def wrapper(*args, **kw):
        if g.ENV.code == "":
            raise StockError("未设置当前股票")
        if g.ENV.freq not in start_date_map.keys():
            raise StockError("未设置当前周期")
        if g.ENV.date is None:
            raise StockError("未设置当前时间")
        return func(*args, **kw)

    return wrapper


def check(func):
    def wrapper(*args, **kw):
        if g.ENV.code == "":
            raise StockError("未设置当前股票")
        if g.ENV.freq not in start_date_map.keys():
            raise StockError("未设置当前周期")
        if g.ENV.date is None:
            raise StockError("未设置当前时间")

        return func(*args, **kw)

    return wrapper


def use_ref(func):
    def wrapper(*args, **kw):
        # 记录调用func前的ref
        ref_start_with = g.ENV.ref
        result = func(*args, **kw)
        g.ENV.ref = ref_start_with
        return result

    return wrapper


def index_round(func):
    def wrapper(*args, **kw):
        result = func(*args, **kw)
        return round(result, 2)

    return wrapper
