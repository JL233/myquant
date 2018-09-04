# 底背驰
import copy
import logging

from common.env import Global
from common.logger import logger
from condition.decorator import condition
from tdx.func import *
from tdx.candy import cross_macd, rcross_macd


def 趋势底背驰():
    m = BARSLAST('CROSS(get_ma120, get_ma60)')
    n = BARSLAST('CROSS(get_ma60, get_ma20)')
    cold_t = max(m, n)
    logger.debug("进入冷气带距离现在的周期是code_t:%d", cold_t)
    # 上一次MACD死叉距离现在的周期
    sc_last_t = BARSLAST(rcross_macd)
    try:
        low_pre = FINDLOW(get_low, sc_last_t, cold_t - sc_last_t, 1)[1]
        macd_least = FINDLOW(get_macd, sc_last_t, cold_t - sc_last_t, 1)[1]
        # DIF最小值
        dif_least = FINDLOW(get_dif, sc_last_t, cold_t - sc_last_t, 1)[1]
        # 现低点CLOSE
        close_least_t, close_least = FINDLOW(get_close, 0, sc_last_t, 1)
        flag = close_least < low_pre and LLV(get_macd, sc_last_t) > macd_least and LLV(get_dif, sc_last_t) > dif_least
        return flag
    except Exception as e:
        logger.error("call 趋势底背驰 err:%s", e)
        return False

@condition
def bottom_bc(env_outer):
    """
    根据传入的g.ENV判断当前情况是否符合condition
    :param env_outer: g.ENV
    :return: True/False
    """
    g.ENV = copy.deepcopy(env_outer)

    # tdx_ref(get_macd()<0,1)
    if not (cross_macd()):
        return False

    logger.info('金叉：%s', g.ENV.date)
    if REF(get_底背驰条件, 1):
        return True
    if 趋势底背驰():
        return True
    return False


def get_绿柱面积():
    macd = get_macd()
    if macd < 0:
        last_macd_lt_0 = BARSLAST('get_macd()>0')
        macd_sum = SUM(get_macd, last_macd_lt_0)
        return macd_sum
    else:
        return 0


def get_X1():
    macd = get_macd()
    if macd < 0:
        return BARSLAST(cross_macd)
    else:
        return 0


def get_底背驰条件():
    绿柱面积 = get_绿柱面积()
    X1 = get_X1()
    前次绿柱面积 = REF(get_绿柱面积, X1 + 1)

    code = "LLV(get_low, BARSLAST('get_macd()>0'))"
    本次最低价 = eval(code)
    前次最低价 = REF(code, X1 + 1)

    if 绿柱面积 < 0 and abs(绿柱面积) < abs(前次绿柱面积) and 本次最低价 < 前次最低价:
        return True
    return False
