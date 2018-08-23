# 底背驰
from tdx.func import *
from tdx.candy import cross_macd


def bottom_bc():
    # tdx_ref(get_macd()<0,1)
    if not (cross_macd()):
        return False
    if REF(get_底背驰条件,1):
        return True

    # {如果现在是死叉状态，返回最近一次死叉到现在绿柱的总和}
    # 绿柱面积: = IF(get_macd_df < 0, SUM(get_macd_df, BARSLAST(JC > 0)), 0);
    # {自从上次死叉到现在的最小值}
    # 本次最低价: = LLV(L, BARSLAST(JC > 0));
    # {自从上次金叉到现在的最小值}
    # 本次最高价: = HHV(H, BARSLAST(JC < 0));
    # {如果MACD < 0，返回最近一次金叉的时间}
    # X1: = IF(get_macd_df < 0, BARSLAST(CROSS(get_macd_df.DIF, get_macd_df.DEA)), 0);
    # {X1 + 1：是隔段绿柱的最后一天}
    # 前次绿柱面积: = REF(绿柱面积, X1 + 1);
    # 前次最低价: = REF(本次最低价, X1 + 1);
    # 底背弛条件: = IF((绿柱面积 < 0 AND ABS(绿柱面积) < ABS(前次绿柱面积)
    # AND
    # 本次最低价 < 前次最低价 ), 1, 0);
    return False

def get_绿柱面积():
    macd = get_macd()
    if macd<0:
        return SUM(get_macd, BARSLAST('get_macd()>0'))
    else:
        return 0
def get_X1():
    macd = get_macd()
    if macd < 0:
        return BARSLAST(cross_macd)
    else:
        return 0
def get_底背驰条件():
    绿柱面积=get_绿柱面积()
    X1=get_X1()
    前次绿柱面积=REF(get_绿柱面积, X1+1)

    code="LLV(get_low, BARSLAST('get_macd()>0'))"
    本次最低价 = eval(code)
    前次最低价 = REF(code, X1 + 1)

    if 绿柱面积<0 and abs(绿柱面积)<abs(前次绿柱面积) and 本次最低价<前次最低价:
        return True
    return False
