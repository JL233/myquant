# 通达信指标
# 装饰器
from tdx.index import *
from tdx.tdx_decorator import *


@use_ref
def BARSLAST(func):
    # 如果当天func成立，理论上返回0，但是这里不允许返回0，所以直接ref+1
    g.ENV.ref += 1
    count = 1
    if callable(func):
        while True:
            if func():
                return count
            else:
                # 如果最初ref>0，那么count不与ref等同，需要单独计量
                count += 1
                g.ENV.ref += 1
    elif isinstance(func, str):
        while True:
            if eval(func):
                return count
            else:
                # 如果最初ref>0，那么count不与ref等同，需要单独计量
                count += 1
                g.ENV.ref += 1
    else:
        raise StockError("param not func or str")


@use_ref
def HHV(func, n):
    arr = []
    for i in range(n):
        g.ENV.ref = g.ENV.ref + 1
        high = func()
        arr.append(high)
    result = max(arr)
    return result


@use_ref
def LLV(func, n):
    arr = []
    for i in range(n):
        g.ENV.ref = g.ENV.ref + 1
        low = func()
        arr.append(low)
    result = min(arr)
    return result


@use_ref
def REF(func, n):
    """
    tdx_ref(get_macd()<0,1)这样使用不可行：
    get_macd()<0不会再tdx_ref里面执行，而是执行之后传递给tdx_ref作为参数，是一个值而不是方法
    正确的方法是
    :param func:
    :param n:
    :return:
    """
    g.ENV.ref += n
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
def SUM(func, n):
    result = 0
    for i in range(n):
        result += func()
        g.ENV.ref += 1
    return result


@use_ref
def FINDLOW(func, n, m, index):
    if index < 1 or not isinstance(index, int):
        raise ValueError("index必须是大于0的整数")
    if n < 0 or not isinstance(n, int):
        raise ValueError("n必须是>=0的整数")
    if m < 0 or not isinstance(n, int):
        raise ValueError("m必须是>=0的整数")
    g.ENV.ref += n
    map = {}
    for i in range(m):
        map[g.ENV.ref] = func()
        g.ENV.ref += 1
    # 降序reverse=True
    arr_sorted = [(k, map[k]) for k in sorted(map, key=map.get)]
    try:
        return arr_sorted[index - 1]
    except IndexError as e:
        logger.error()


@use_ref
def FINDHIGH(func, n, m, index):
    if index < 1 or not isinstance(index, int):
        raise ValueError("index必须是大于0的整数")
    if n < 0 or not isinstance(n, int):
        raise ValueError("n必须是>=0的整数")
    if m < 0 or not isinstance(n, int):
        raise ValueError("m必须是>=0的整数")
    g.ENV.ref += n
    map = {}
    for i in range(m):
        map[g.ENV.ref] = func()
        g.ENV.ref += 1
    # 降序reverse=True
    arr_sorted = [(k, map[k]) for k in sorted(map, key=map.get, reverse=True)]
    return arr_sorted[index - 1]


@use_ref
def CROSS(get_index1, get_index2):
    if get_index1 == get_index2:
        raise ValueError("cross的两个参数不能相同")
    if get_index1() > get_index2() and REF(get_index1, 1) < REF(get_index2, 1):
        return True
    return False
