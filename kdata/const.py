BAR_ASSET_INDEX = "INDEX"
DT_FMT="%Y-%m-%d %H:%M:%S"
# key  是 freq
start_date_map = {
    "5min": "2016-08-22",
    "15min": "2016-08-22",
    "30min": "2016-08-22",
    "60min": "2016-08-22",
    "D": "2009-12-31",
    "W": "2009-12-31",
    "M": "2009-12-31",
}
end_date_suffix_map = {
    "5min": "15:00:00",
    "15min": "15:00:00",
    "30min": "15:00:00",
    "60min": "15:00:00",
    "D": "00:00:00",
    "W": "00:00:00",
    "M": "00:00:00",
}
kdata_sheets = {
    "5min": "k_data_5",
    "15min": "k_data_15",
    "30min": "k_data_30",
    "60min": "k_data_60",
    "D": "k_data_day",
    "W": "k_data_week",
    "M": "k_data_month",
}
freq_value_map = {
    "5min": 1,
    "15min": 3,
    "30min": 6,
    "60min": 12,
    "D": 48,
    "W": 48 * 5,
    "M": 48 * 5 * 4,
}
