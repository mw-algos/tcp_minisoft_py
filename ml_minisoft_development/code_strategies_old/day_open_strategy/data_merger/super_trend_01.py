import pandas as pd
import numpy as np
import math

date_from = pd.to_datetime('2020-01-10')
df_bank_nifty_intraday_data = pd.read_csv("bank_nifty_index.csv")
profit_loss_day_df_ = pd.DataFrame()

number_ = 1
for row_number_, row_record_ in df_bank_nifty_days_data.iloc[1:].iterrows():
    df_bn_st_7_3 = df_bank_nifty_super_trend_7_3[(df_bank_nifty_super_trend_7_3['date_on_str'] == row_record_.days)]
    df_bn_st_7_3.reset_index(drop=True, inplace=True)
    current_day = row_record_.days
    previous_day = df_bank_nifty_days_data.iloc[row_number_ - 1].days
    current_candle_dict_info = {'date': current_day}
    current_candle_dict_info = first_candle_type_input_build(df_bank_nifty_super_trend_7_3, current_day,
                                                             previous_day, current_candle_dict_info)

    if current_candle_dict_info['candle_position'] != 'UP_OPEN_OUT_SIDE_UP_CLOSE_OUT_SIDE':
        continue

    profit_loss_day_df_new = pd.DataFrame()
    profit_loss_day_df = pd.DataFrame()
    for row_number, row_record in df_bn_st_7_3.iloc[2:].iterrows():
        previous_record = df_bn_st_7_3.iloc[row_number - 1].super_trend_direction_7_1
        current_record = df_bn_st_7_3.iloc[row_number].super_trend_direction_7_1

        previous_record_ = df_bn_st_7_3.iloc[row_number - 1].super_trend_direction_7_3
        current_record_ = df_bn_st_7_3.iloc[row_number].super_trend_direction_7_3

        diff = ((row_record.close - row_record.super_trend_7_3) / row_record.close)
        diff_super_trend = abs(round(diff * 100, 2))

        if current_record_ != previous_record_:
            profit_loss_df = {'date_on_str': row_record.date_on_str, 'instrument': 'bank_nifty',
                              'traded_date_time': row_record.date,
                              'direction': current_record, 'price': row_record.close}
            profit_loss_day_df_new = profit_loss_day_df_new.append(profit_loss_df, ignore_index=True)

        if profit_loss_day_df_new.shape[0] > 1:
            second = profit_loss_day_df_new.iloc[profit_loss_day_df_new.shape[0] - 2].price
            first = profit_loss_day_df_new.iloc[profit_loss_day_df_new.shape[0] - 1].price

        if (profit_loss_day_df.shape[0] == 0) and (current_record == 'down') and (
                row_record.open < current_candle_dict_info['cur_open']) & (diff_super_trend < 1):
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_width'],
                              'traded_date_time': row_record.date,
                              'stop_loss':  row_record.low - ((0.5 * row_record.low)/100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': diff_super_trend
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        # with-out stop loss -> 1500 points -> with stop loss -> 80 percent occurrence -> remove and test it
        elif profit_loss_day_df.shape[0] == 1:
            profit_loss_day_df_1 = profit_loss_day_df.iloc[0]
            if profit_loss_day_df_1.direction == 'down' and row_record.close < profit_loss_day_df_1.stop_loss:
                profit_loss_df = {'date_on_str': row_record.date_on_str,
                                  'date': current_candle_dict_info['date'], 'instrument': 'bank_nifty',
                                  'traded_date_time': row_record.date,
                                  'stop_loss': row_record.close + 300,
                                  'direction': 'up', 'price': row_record.close
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
