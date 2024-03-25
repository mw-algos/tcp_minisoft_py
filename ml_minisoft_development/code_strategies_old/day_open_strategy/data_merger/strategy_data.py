import numpy as np
import pandas as pd
import os.path
from tech_indicator.super_trend_builder import super_trend


def all_time_frame_strategies(df_bank_nifty_intraday_data):
    _5min_df_bank_nifty_super_trend_7_3 = super_trend(df_bank_nifty_intraday_data.copy(), 7, 3)
    _10min_df_bank_nifty_super_trend_7_3 = super_trend(df_bank_nifty_intraday_data.copy(), 7, 3)
    _15min_df_bank_nifty_super_trend_7_3 = super_trend(df_bank_nifty_intraday_data.copy(), 7, 3)


def sup_trend(df_bank_nifty_intraday_data, data_from):
    if not os.path.exists('df_bank_nifty_super_trend_7_3_all_time_frames.csv'):
        df_bank_nifty_intraday_data[['true_range', 'average_true_range_period_7', 'final_ub', 'final_lb', 'uptrend',
                                     'super_trend_7_3', 'super_trend_direction_7_3']] = None
        df_bank_nifty_intraday_data['date'] = (pd.to_datetime(df_bank_nifty_intraday_data['date']))
        df_bank_nifty_intraday_data["date_on"] = df_bank_nifty_intraday_data["date"].dt.date
        df_bank_nifty_intraday_data['date_on_str'] = df_bank_nifty_intraday_data["date"].dt.date.astype(str)
        df_bank_nifty_intraday_data = df_bank_nifty_intraday_data.copy().sort_values(by="date")

        df_bank_nifty_super_trend_7_3 = super_trend(df_bank_nifty_intraday_data.copy(), 7, 3)
        df_bank_nifty_super_trend_7_3 = df_bank_nifty_super_trend_7_3[['date_on', 'date_on_str', 'date', 'open',
                                                                       'low', 'high', 'close', 'volume',
                                                                       'super_trend_7_3',
                                                                       'super_trend_direction_7_3']]

        df_bank_nifty_super_trend_7_1 = super_trend(df_bank_nifty_intraday_data.copy(), 7, 0.8)
        df_bank_nifty_super_trend_7_3['super_trend_direction_7_1'] = df_bank_nifty_super_trend_7_1[
            'super_trend_direction_7_3']

        df_bank_nifty_super_trend_7_3.to_csv('df_bank_nifty_super_trend_7_3.csv')
    else:
        df_bank_nifty_super_trend_7_3 = pd.read_csv('df_bank_nifty_super_trend_7_3.csv')

    df_bank_nifty_super_trend_7_3 = df_bank_nifty_super_trend_7_3.loc[:,
                                    ~df_bank_nifty_super_trend_7_3.columns.str.contains('^Unnamed')]

    df_bank_nifty_super_trend_7_3['date'] = (pd.to_datetime(df_bank_nifty_super_trend_7_3['date']))
    df_bank_nifty_super_trend_7_3["date_on"] = df_bank_nifty_super_trend_7_3["date"].dt.date
    df_bank_nifty_super_trend_7_3['date_on_str'] = df_bank_nifty_super_trend_7_3["date"].dt.date.astype(str)
    df_bank_nifty_super_trend_7_3 = df_bank_nifty_super_trend_7_3[df_bank_nifty_super_trend_7_3.date_on >= data_from]

    df_bank_nifty_intraday_data_group_by_days = df_bank_nifty_super_trend_7_3.groupby(['date_on_str'])
    df_bank_nifty_days_data = pd.DataFrame({'days': list(df_bank_nifty_intraday_data_group_by_days.groups.keys())})

    return df_bank_nifty_super_trend_7_3, df_bank_nifty_days_data