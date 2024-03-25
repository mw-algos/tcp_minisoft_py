import pandas as pd
from tech_indicator.super_trend_builder import super_trend


def convert_specific_time_frame(raw_df_date, required_time_frame, period, multiplier):
    df_bk_converted_data = raw_df_date
    df_bk_converted_data = df_bk_converted_data.loc[:, ~df_bk_converted_data.columns.str.contains('^Unnamed')]
    df_bk_converted_data['date'] = pd.to_datetime(df_bk_converted_data['date'])
    freq = required_time_frame
    df_bk_converted_data = df_bk_converted_data.groupby(pd.Grouper(key='date', freq=freq)) \
        .agg({"open": "first", "close": "last", "low": "min", "high": "max", 'volume': 'sum'}).dropna(how='any')
    df_bk_converted_data[['true_range', 'average_true_range_period_7', 'final_ub', 'final_lb', 'uptrend',
                          'super_trend_7_3', 'super_trend_direction_7_3']] = None
    return super_trend(df_bk_converted_data, period, multiplier)


def strategy_all_time_frames(raw_df_date):
    df_bk_one_5min_data = convert_specific_time_frame(raw_df_date, required_time_frame='5min', period=10, multiplier=3)
    df_bk_one_5min_data = df_bk_one_5min_data[
        ['open', 'close', 'low', 'high', 'volume', 'super_trend_7_3', 'super_trend_direction_7_3']]
    df_bk_one_5min_data = df_bk_one_5min_data.rename(
        columns={'super_trend_7_3': 'sp_7_3_5min', 'super_trend_direction_7_3': 'sp_dir_7_3_5min'})
    df_bk_one_10min_data = convert_specific_time_frame(raw_df_date, required_time_frame='10min', period=10,
                                                       multiplier=3)
    df_bk_one_10min_data = df_bk_one_10min_data[['super_trend_7_3', 'super_trend_direction_7_3']]
    df_bk_one_10min_data = df_bk_one_10min_data.rename(
        columns={'super_trend_7_3': 'sp_7_3_10min', 'super_trend_direction_7_3': 'sp_dir_7_3_10min'})
    df_bk_one_15min_data = convert_specific_time_frame(raw_df_date, required_time_frame='15min', period=10,
                                                       multiplier=3)
    df_bk_one_15min_data = df_bk_one_15min_data[['super_trend_7_3', 'super_trend_direction_7_3']]
    df_bk_one_15min_data = df_bk_one_15min_data.rename(
        columns={'super_trend_7_3': 'sp_7_3_15min', 'super_trend_direction_7_3': 'sp_dir_7_3_15min'})
    df_bk_one_15min_data_1 = convert_specific_time_frame(raw_df_date, required_time_frame='15min', period=10,
                                                         multiplier=1)
    df_bk_one_15min_data_1 = df_bk_one_15min_data_1[['super_trend_7_3', 'super_trend_direction_7_3']]
    df_bk_one_15min_data_1 = df_bk_one_15min_data_1.rename(
        columns={'super_trend_7_3': 'sp_7_1_15min', 'super_trend_direction_7_3': 'sp_dir_7_1_15min'})
    merged_dataframe = pd.merge_asof(df_bk_one_5min_data, df_bk_one_10min_data, on="date")
    merged_dataframe_ = pd.merge_asof(merged_dataframe, df_bk_one_15min_data, on="date")
    return pd.merge_asof(merged_dataframe_, df_bk_one_15min_data_1, on="date")


raw_df_date = pd.read_csv('df_bk_one_1min_data.csv').head(1000)
strategy_all_time_data = strategy_all_time_frames(raw_df_date)

print('')
