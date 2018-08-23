from env import ENV
from stockerror import StockError
# 通达信指标
from tdx.index import *
# 装饰器
from tdx.tdx_decorator import *
from tdx.index import *


@use_ref
@check
def BARSLAST(func):
    count = 0
    if callable(func):
        while True:
            if func():
                return count
            else:
                # 如果最初ref>0，那么count不与ref等同，需要单独计量
                count += 1
                ENV.ref += 1
    elif isinstance(func, str):
        while True:
            if eval(func):
                return count
            else:
                # 如果最初ref>0，那么count不与ref等同，需要单独计量
                count += 1
                ENV.ref += 1
    else:
        raise StockError("param not func or str")


@use_ref
@check
def HHV(func, n):
    arr = []
    for i in range(n):
        ENV.ref = ENV.ref + i
        arr.append(func())
    result = max(arr)
    return result


@use_ref
@check
def LLV(func, n):
    arr = []
    for i in range(n):
        ENV.ref = ENV.ref + i
        arr.append(func())
    result = min(arr)
    return result


@use_ref
@check
def REF(func, n):
    """
    tdx_ref(get_macd()<0,1)这样使用不可行：
    get_macd()<0不会再tdx_ref里面执行，而是执行之后传递给tdx_ref作为参数，是一个值而不是方法
    正确的方法是
    :param func:
    :param n:
    :return:
    """
    ENV.ref += n
    if callable(func):
        result = func()
        return result
    elif isinstance(func, str):
        # 代码字符串可以正常调用的前提是已经import相关模块
        result = eval(func)
        return result
    else:
        raise StockError("param not func or str")


@use_ref
@check
def SUM(func, n):
    result = 0
    for i in range(n):
        result += func()
        ENV.ref += 1
    return result
