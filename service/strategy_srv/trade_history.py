from common.logger import logger
from kdata.const import freq_value_map
from kdata.mongodb import get_close_by_date


def trade(df_hist):
    position = 0
    cost = 0
    base = 0
    current_long_freq = ''
    last_short=''
    last_long=""
    for index, row in df_hist.iterrows():
        print(index, row["买卖"], row["级别"])
        if row["买卖"] == 'bottom_bc' and freq_value_map[row["级别"]] > 1:
            if position == 0:
                position == 1
                cost = get_close_by_date(index)
                if base == 0:
                    base = cost
                current_long_freq = row["级别"]
                last_long
            else:
                if freq_value_map[current_long_freq] < current_long_freq[row["级别"]]:
                    current_long_freq = row["级别"]
        if row["买卖"] == 'top_bc' :
            if position == 1:
                position == 0
                cost = get_close_by_date(index)
                current_short_freq = row["级别"]
            else:
                if freq_value_map[current_short_freq] > freq_value_map[row["级别"]]:
                    current_short_freq = row["级别"]
    logger.info("最终收益:%r", cost - base)
