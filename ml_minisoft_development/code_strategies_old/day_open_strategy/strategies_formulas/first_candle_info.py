import pandas as pd
from tech_indicator.super_trend_builder import super_trend
import numpy as np
import math

# Instrument intraday wise data
df_bank_nifty_intraday_data = pd.read_csv("instrument_market_data_bank_nifty.csv")
df_bank_nifty_intraday_data["date_on"] = pd.to_datetime(df_bank_nifty_intraday_data["date"]).dt.date.astype(str)
df_bank_nifty_intraday_data["time_on"] = pd.to_datetime(df_bank_nifty_intraday_data["date"]).dt.time
df_bank_nifty_intraday_data_group_by_days = df_bank_nifty_intraday_data.groupby(['date_on'])
df_bank_nifty_days_data = pd.DataFrame({'days': list(df_bank_nifty_intraday_data_group_by_days.groups.keys())})

complied_records = pd.DataFrame()
current_day_dict = {}
for row_index, row_record in df_bank_nifty_days_data[1:].iterrows():

    current_day_dict['date'] = row_record.days
    df_bank_nifty_data_previous = df_bank_nifty_intraday_data[(df_bank_nifty_intraday_data['date_on'] ==
                                                               df_bank_nifty_days_data.iloc[row_index - 1].days)]

    df_bank_nifty_data_current = df_bank_nifty_intraday_data[(df_bank_nifty_intraday_data['date_on'] ==
                                                              df_bank_nifty_days_data.iloc[row_index].days)]

    df_bank_nifty_intraday_data_previous = pd.DataFrame([{'pre_open': df_bank_nifty_data_previous.open.iloc[0],
                                                          'pre_high': df_bank_nifty_data_previous.high.max(),
                                                          'pre_low': df_bank_nifty_data_previous.low.min(),
                                                          'pre_close': df_bank_nifty_data_previous.close.iloc[-1]}],
                                                        )

    df_bank_nifty_intraday_data_current = pd.DataFrame([{'cur_open': df_bank_nifty_data_current.iloc[0].open,
                                                         'cur_high': df_bank_nifty_data_current.iloc[0].high,
                                                         'cur_low': df_bank_nifty_data_current.iloc[0].low,
                                                         'cur_close': df_bank_nifty_data_current.iloc[0].close
                                                         }])

    if ((df_bank_nifty_intraday_data_current['cur_open'].values[0] < df_bank_nifty_intraday_data_previous['pre_low'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] < df_bank_nifty_intraday_data_previous['pre_low'].values[0])):
        current_day_dict['candle_position'] = 'DOWN_OPEN_OUTSIDE_DOWN_CLOSE_OUT_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] < df_bank_nifty_intraday_data_previous['pre_low'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] > df_bank_nifty_intraday_data_previous['pre_low'].values[0])):
        current_day_dict['candle_position'] = 'DOWN_OPEN_OUT_SIDE_CLOSE_IN_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] > df_bank_nifty_intraday_data_previous['pre_low'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] < df_bank_nifty_intraday_data_previous['pre_low'].values[0])):
        current_day_dict['candle_position'] = 'OPEN_IN_SIDE_DOWN_CLOSE_OUT_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] > df_bank_nifty_intraday_data_previous['pre_low'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] < df_bank_nifty_intraday_data_previous['pre_high'].values[0])):
        current_day_dict['candle_position'] = 'OPEN_IN_SIDE_CLOSE_IN_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] < df_bank_nifty_intraday_data_previous['pre_high'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] > df_bank_nifty_intraday_data_previous['pre_high'].values[0])):
        current_day_dict['candle_position'] = 'OPEN_IN_SIDE_UP_CLOSE_OUT_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] > df_bank_nifty_intraday_data_previous['pre_high'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] > df_bank_nifty_intraday_data_previous['pre_high'].values[0])):
        current_day_dict['candle_position'] = 'UP_OPEN_OUT_SIDE_UP_CLOSE_OUT_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] > df_bank_nifty_intraday_data_previous['pre_high'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] < df_bank_nifty_intraday_data_previous['pre_high'].values[0])):
        current_day_dict['candle_position'] = 'UP_OPEN_OUT_SIDE_CLOSE_IN_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] < df_bank_nifty_intraday_data_previous['pre_low'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] > df_bank_nifty_intraday_data_previous['pre_high'].values[0])):
        current_day_dict['candle_position'] = 'DOWN_OPEN_OUT_SIDE_UP_CLOSE_OUT_SIDE'

    elif ((df_bank_nifty_intraday_data_current['cur_open'].values[0] > df_bank_nifty_intraday_data_previous['pre_high'].values[0]) & (
            df_bank_nifty_intraday_data_current['cur_close'].values[0] < df_bank_nifty_intraday_data_previous['pre_low'].values[0])):
        current_day_dict['candle_position'] = 'UP_OPEN_OUT_SIDE_DOWN_CLOSE_OUT_SIDE'

    else:
        current_day_dict['candle_position'] = 'NO_CLEAR_DIRECTION'

    if df_bank_nifty_intraday_data_current['cur_open'].values[0] > df_bank_nifty_intraday_data_current['cur_close'].values[0]:
        current_day_dict['candle_type'] = 'red candle'
        current_day_dict['candle_upper_wick'] = abs(round(
            (((df_bank_nifty_intraday_data_current['cur_open'].values[0] - df_bank_nifty_intraday_data_current['cur_high'].values[0])
              / (df_bank_nifty_intraday_data_current['cur_open'].values[0])) * 100), 2))

        current_day_dict['candle_lower_wick'] = abs(round(
            (((df_bank_nifty_intraday_data_current['cur_close'].values[0] - df_bank_nifty_intraday_data_current['cur_low'].values[0])
              / (df_bank_nifty_intraday_data_current['cur_close'].values[0])) * 100), 2))
    else:
        current_day_dict['candle_type'] = 'green candle'
        current_day_dict['candle_upper_wick'] = abs(round(
            (((df_bank_nifty_intraday_data_current['cur_close'].values[0] - df_bank_nifty_intraday_data_current['cur_high'].values[0])
              / (df_bank_nifty_intraday_data_current['cur_close'].values[0])) * 100), 2))

        current_day_dict['candle_lower_wick'] = abs(round(
            (((df_bank_nifty_intraday_data_current['cur_open'].values[0] - df_bank_nifty_intraday_data_current['cur_close'].values[0])
              / (df_bank_nifty_intraday_data_current['cur_open'].values[0])) * 100), 2))

    current_day_dict['candle_width'] = abs(
        round((((df_bank_nifty_intraday_data_current['cur_high'].values[0] - df_bank_nifty_intraday_data_current['cur_low'].values[0])
                / (df_bank_nifty_intraday_data_current['cur_high'].values[0])) * 100), 2))

    current_day_dict['candle_body'] = abs(
        round((((df_bank_nifty_intraday_data_current['cur_open'].values[0] - df_bank_nifty_intraday_data_current['cur_close'].values[0])
                / (df_bank_nifty_intraday_data_current['cur_open'].values[0])) * 100), 2))

    complied_records = complied_records.append(current_day_dict, ignore_index=True)

complied_records.to_csv('first_candle_info.csv')
