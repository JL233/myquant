from common.logger import logger
from tdx.index import get_macd
from tdx.func import REF


def cross_macd():
    # 调试时发现REF不一定执行，因为可能第一个条件就不满足
    result = get_macd() > 0 and REF('get_macd()<0', 1)
    return result


def rcross_macd():
    result = get_macd() < 0 and REF('get_macd()>0', 1)
    return result
