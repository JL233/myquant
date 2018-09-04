import datetime

from condition import bottom_bc, top_bc
from kdata.const import BAR_ASSET_INDEX
from strategy.trade import Strategy

if __name__ == "__main__":
    start_date = "2018-06-14"
    stra = Strategy(bottom_bc.bottom_bc, top_bc.top_bc)
    stra.start("000001", BAR_ASSET_INDEX, start_date, end_date="2019-01-01")
