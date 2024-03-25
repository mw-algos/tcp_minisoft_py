import pandas as pd
import numpy as np
import math

from testing.strategies_formulas.first_candle_formulas import first_candle_type_input_build
from testing.strategies_formulas.strategy_conditions import last_candle_exit, day_wise_profit_cal, final_profit_cal
from testing.strategies_formulas.strategy_data import sup_trend

# win_trade_percentage = 69.44 & profit_trade_percentage = -77.98 (profit) & profit_loss_sum = -15370.799999999992 & count = 108 & total = 148

date_from = pd.to_datetime('2020-01-10')
df_bank_nifty_intraday_data = pd.read_csv("df_bk_one_min_data.csv")
df_bank_nifty_super_trend_7_3, df_bank_nifty_days_data = sup_trend(df_bank_nifty_intraday_data, date_from)

profit_loss_day_df_ = pd.DataFrame()

number_ = 1
for row_number_, row_record_ in df_bank_nifty_days_data.iloc[2:].iterrows():
    df_bn_st_7_3 = df_bank_nifty_super_trend_7_3[(df_bank_nifty_super_trend_7_3['date_on_str'] == row_record_.days)]
    df_bn_st_7_3.reset_index(drop=True, inplace=True)
    current_day = row_record_.days
    previous_day = df_bank_nifty_days_data.iloc[row_number_ - 1].days
    current_candle_dict_info = {'date': current_day}
    current_candle_dict_info = first_candle_type_input_build(df_bank_nifty_super_trend_7_3, current_day,
                                                             previous_day, current_candle_dict_info)

    if current_candle_dict_info['candle_position'] != 'UP_OPEN_OUT_SIDE_UP_CLOSE_OUT_SIDE':
        continue

    number_ = number_ + 1
    profit_loss_day_df_new = pd.DataFrame()
    profit_loss_day_df = pd.DataFrame()
    condition_11 = False
    condition_12 = False
    for row_number, row_record in df_bn_st_7_3.iloc[2:].iterrows():

        previous_record = df_bn_st_7_3.iloc[row_number - 1].super_trend_direction_7_1
        current_record = df_bn_st_7_3.iloc[row_number].super_trend_direction_7_1

        condition_01 = (profit_loss_day_df.shape[0] == 0) and \
                       current_candle_dict_info['cur_low'] > current_candle_dict_info['pre_high'] and \
                       current_candle_dict_info['candle_type'] == 'green candle' and \
                       row_record.open < current_candle_dict_info['cur_close']

        condition_02 = (profit_loss_day_df.shape[0] == 0) and \
                       current_candle_dict_info['candle_type'] == 'red candle'

        if current_candle_dict_info['candle_type'] == 'red candle' and not condition_12 and row_record.open < \
                current_candle_dict_info['pre_high']:
            condition_12 = True

        if condition_01:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_body'],
                              'traded_date_time': row_record.date,
                              'stop_loss': row_record.low - ((0.5 * row_record.low) / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': 'diff_super_trend'
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif condition_02 and row_record.high > current_candle_dict_info['cur_high'] and current_record == 'down':
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_width'],
                              'traded_date_time': row_record.date,
                              'stop_loss': row_record.low - ((0.5 * row_record.low) / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': 'diff_super_trend'
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif condition_02 and condition_12 and row_record.high > current_candle_dict_info['cur_close'] and current_record == 'up':
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_width'],
                              'traded_date_time': row_record.date,
                              'stop_loss': row_record.low - ((0.5 * row_record.low) / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': 'diff_super_trend'
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if (row_number + 2 == df_bn_st_7_3.shape[0]) & (profit_loss_day_df.shape[0] == 1):
            profit_loss_day_df = last_candle_exit(profit_loss_day_df, row_record)

        if profit_loss_day_df.shape[0] == 2:
            profit_loss_day_df_, profit_loss_day_df = day_wise_profit_cal(profit_loss_day_df_, profit_loss_day_df)
            profit_loss_day_df_1 = profit_loss_day_df_.iloc[-1]
            if profit_loss_day_df_1.buy_price - profit_loss_day_df_1.sell_price < 0:
                print(profit_loss_day_df_1.buy_price - profit_loss_day_df_1.sell_price)
                break
            break

profit_loss_day_df_ = final_profit_cal(profit_loss_day_df_)
profit_loss_day_df_.to_csv('profit_loss_day_df_.csv')
print(number_)