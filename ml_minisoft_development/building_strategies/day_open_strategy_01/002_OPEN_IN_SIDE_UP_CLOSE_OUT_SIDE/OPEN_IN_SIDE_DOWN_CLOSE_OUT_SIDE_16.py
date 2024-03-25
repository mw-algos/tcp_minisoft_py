# win_trade_percentage = 69.44 & profit_trade_percentage = -75.17 (profit) & profit_loss_sum = -3553.799999999974 & count = 36 & total = 42
import pandas as pd

from testing.strategies_formulas.first_candle_formulas import first_candle_type_input_build
from testing.strategies_formulas.strategy_conditions import last_candle_exit, day_wise_profit_cal, final_profit_cal
from testing.strategies_formulas.strategy_data import sup_trend

date_from = pd.to_datetime('2020-01-01')
df_bank_nifty_intraday_data = pd.read_csv('df_bk_one_min_data_5.csv')
df_bank_nifty_super_trend_7_3, df_bank_nifty_days_data = sup_trend(df_bank_nifty_intraday_data, date_from)

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

    if current_candle_dict_info['candle_position'] != 'OPEN_IN_SIDE_UP_CLOSE_OUT_SIDE':
        continue
    number_ = number_ + 1
    profit_loss_day_df_new = pd.DataFrame()
    profit_loss_day_df = pd.DataFrame()
    third_entry_condition_sell = True
    second_entry_condition_sell = False
    second_entry_condition_buy = False
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():
        previous_record = df_bn_st_7_3.iloc[row_number - 1].super_trend_direction_7_1
        current_record = df_bn_st_7_3.iloc[row_number].super_trend_direction_7_1

        previous_record_ = df_bn_st_7_3.iloc[row_number - 1].super_trend_direction_7_3
        current_record_ = df_bn_st_7_3.iloc[row_number].super_trend_direction_7_3

        if previous_record != current_record:
            profit_loss_df = {'date_on_str': row_record.date_on_str, 'instrument': 'bank_nifty',
                              'traded_date_time': row_record.date,
                              'direction': current_record, 'price': row_record.close}
            profit_loss_day_df_new = profit_loss_day_df_new.append(profit_loss_df, ignore_index=True)

        if profit_loss_day_df_new.shape[0] > 2:
            third = profit_loss_day_df_new.iloc[profit_loss_day_df_new.shape[0] - 3].price
            second = profit_loss_day_df_new.iloc[profit_loss_day_df_new.shape[0] - 2].price
            first = profit_loss_day_df_new.iloc[profit_loss_day_df_new.shape[0] - 1].price

        stop_loss = ((current_candle_dict_info['cur_close'] - current_candle_dict_info['pre_low']) /
                     current_candle_dict_info['cur_open'])
        diff_super_trend = abs(round(stop_loss * 100, 2))

        primary_entry_condition_sell = (profit_loss_day_df.shape[0] == 0) and (current_candle_dict_info['candle_type'] == 'green candle')

        if row_number == 1:
            second_entry_condition_buy = row_record.open > row_record.close

        if primary_entry_condition_sell and row_record.close < current_candle_dict_info['cur_low'] and profit_loss_day_df_new.shape[0] > 0 and current_record == 'up':
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_width'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': row_record.close + (0.50 * row_record.close / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': row_record.low < current_candle_dict_info['cur_low']
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif primary_entry_condition_sell and row_record.close > current_candle_dict_info['cur_high'] and profit_loss_day_df_new.shape[0] > 0 and current_record == 'down':
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_width'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': row_record.close + (0.50 * row_record.close / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': row_record.low < current_candle_dict_info['cur_low']
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
