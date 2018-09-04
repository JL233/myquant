# 顶背驰
import copy

from condition.decorator import condition
from tdx.func import *
from tdx.candy import *


def 趋势顶背驰():
    m = BARSLAST('CROSS(get_ma60,get_ma120)')
    n = BARSLAST('CROSS(get_ma20,get_ma60)')
    warm_t = max(m, n)
    logger.debug("进入暖气带距离现在的周期是code_t:%d", warm_t)
    # 上一次MACD金叉距离现在的周期
    jc_last_t = BARSLAST(cross_macd)
    try:
        high_pre = FINDHIGH(get_high, jc_last_t, warm_t - jc_last_t, 1)[1]
        macd_highest = FINDHIGH(get_macd, jc_last_t, warm_t - jc_last_t, 1)[1]
        # DIF最大值
        dif_highest = FINDHIGH(get_dif, jc_last_t, warm_t - jc_last_t, 1)[1]
        # 现高点CLOSE
        close_highest_t, close_highest = FINDHIGH(get_close, 0, jc_last_t, 1)
        flag = close_highest_t > high_pre and HHV(get_macd, jc_last_t) < macd_highest and HHV(MACD.DIF,
                                                                                              jc_last_t) < dif_highest
        return flag
    except Exception as e:
        logger.error("call 趋势顶背驰 err:%s", e)
        return False


@condition
def top_bc(env_outer):
    """
    根据传入的g.ENV判断当前情况是否符合condition
    :param env_outer: g.ENV
    :return: True/False
    """
    g.ENV = copy.deepcopy(env_outer)

    # tdx_ref(get_macd()>0,1)典型的错误写法
    if not (rcross_macd()):
        return False
    logger.info('死叉：%s', g.ENV.date)
    if REF(get_顶背驰条件, 1):
        return True
    if 趋势顶背驰():
        return True

    return False


def get_红柱面积():
    macd = get_macd()
    if macd > 0:
        return SUM(get_macd, BARSLAST('get_macd()<0'))
    else:
        return 0


def get_X1():
    macd = get_macd()
    if macd > 0:
        return BARSLAST(rcross_macd)
    else:
        return 0


def get_顶背驰条件():
    # 已验证，没问题
    红柱面积 = get_红柱面积()
    X1 = get_X1()
    前次红柱面积 = REF(get_红柱面积, X1 + 1)

    code = "HHV(get_high, BARSLAST('get_macd()<0'))"
    本次最高价 = eval(code)
    前次最高价 = REF(code, X1 + 1)

    if 红柱面积 > 0 and 红柱面积 < 前次红柱面积 and 本次最高价 > 前次最高价:
        return True
    return False
