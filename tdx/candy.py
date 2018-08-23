from tdx.index import get_macd
from tdx.func import REF


def cross_macd():
    result= get_macd() > 0 and REF('get_macd()<0', 1)
    return result