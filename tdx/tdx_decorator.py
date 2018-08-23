from env import ENV
from stockerror import StockError


def check(func):
    def wrapper(*args, **kw):
        if ENV.code == "":
            raise StockError("未设置当前股票")
        if ENV.freq not in ["5", "15", "30", "60", 'D', 'W', 'M']:
            raise StockError("未设置当前周期")
        if ENV.date == "":
            raise StockError("未设置当前时间")
        return func(*args, **kw)

    return wrapper


def use_ref(func):
    def wrapper(*args, **kw):
        #记录调用func前的ref
        ref_start_with = ENV.ref
        result = func(*args, **kw)
        ENV.ref = ref_start_with
        return result

    return wrapper
