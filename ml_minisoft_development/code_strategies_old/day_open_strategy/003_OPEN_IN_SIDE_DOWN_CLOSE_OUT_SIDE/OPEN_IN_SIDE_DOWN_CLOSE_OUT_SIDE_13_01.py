# win_trade_percentage = 64.0 & profit_trade_percentage = -74.28 (profit) & profit_loss_sum = -6962.349999999991 &
# count = 50 & total = 51
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

    if current_candle_dict_info['candle_position'] != 'OPEN_IN_SIDE_DOWN_CLOSE_OUT_SIDE':
        continue
    number_ = number_ + 1
    profit_loss_day_df_new = pd.DataFrame()
    profit_loss_day_df = pd.DataFrame()
    condition_1 = False
    condition_2 = False
    condition_3 = False
    condition_4 = False
    second_entry_condition_buy = False
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():

        o_l = current_candle_dict_info['pre_open'] - current_candle_dict_info['pre_low']
        h_l = current_candle_dict_info['pre_high'] - current_candle_dict_info['pre_low']

        if not condition_1 and row_record.low > current_candle_dict_info['pre_close']:
            condition_1 = True

        if not condition_2 and row_record.close < current_candle_dict_info['cur_low']:
            condition_2 = True


        if row_number == 1 and row_record.low > current_candle_dict_info['cur_low']:
            second_entry_condition_buy = True

        if (profit_loss_day_df.shape[0] == 0) and row_record.close > current_candle_dict_info['pre_high']:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_lower_wick'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': row_record.close + (0.50 * row_record.close / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': row_record.low < current_candle_dict_info['cur_low']
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)


        elif (profit_loss_day_df.shape[0] == 0) and condition_1 and not condition_2 and row_record.close < \
                current_candle_dict_info['cur_open']:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['candle_lower_wick'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': row_record.close + (0.50 * row_record.close / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': row_record.low < current_candle_dict_info['cur_low']
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif (profit_loss_day_df.shape[0] == 0) and o_l < 100 and row_record.high > current_candle_dict_info[
            'cur_open']:
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

        elif (profit_loss_day_df.shape[0] == 0) and abs(o_l - h_l) < 10 and row_record.high > current_candle_dict_info[
            'cur_open']:
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
