import pandas as pd
from datetime import datetime, time
import time
from common_code.strategies_formulas.first_candle_formulas import first_candle_type_input_build
from common_code.strategies_formulas.strategy_data import sup_trend

date_from = pd.to_datetime('2020-01-01')
df_bank_nifty_intraday_data = pd.read_csv('df_bk_one_5min_data.csv')
df_bank_nifty_super_trend_7_3, df_bank_nifty_days_data = sup_trend(df_bank_nifty_intraday_data, date_from)
new_data_frame_value = pd.DataFrame()
df_bank_nifty_super_trend_7_3['time_column'] = (df_bank_nifty_super_trend_7_3['date'].dt.time).astype(str)
for row_number_, row_record_ in df_bank_nifty_days_data.iloc[1:].iterrows():
    df_bn_st_7_3 = df_bank_nifty_super_trend_7_3[(df_bank_nifty_super_trend_7_3['date_on_str'] == row_record_.days)]
    df_bn_st_7_3.reset_index(drop=True, inplace=True)
    current_day = row_record_.days
    previous_day = df_bank_nifty_days_data.iloc[row_number_ - 1].days
    current_candle_dict_info = {'date': current_day}
    current_candle_dict_info = first_candle_type_input_build(df_bank_nifty_super_trend_7_3, current_day,
                                                             previous_day, current_candle_dict_info)
    first_open_value = current_candle_dict_info['cur_open']
    df_bn_st_7_3['candle_position'] = current_candle_dict_info['candle_position']
    df_bn_st_7_3['candle_type'] = current_candle_dict_info['candle_type']
    df_bn_st_7_3['cur_open'] = current_candle_dict_info['cur_open']
    df_bn_st_7_3['cur_high'] = current_candle_dict_info['cur_high']
    df_bn_st_7_3['cur_low'] = current_candle_dict_info['cur_low']
    df_bn_st_7_3['cur_close'] = current_candle_dict_info['cur_close']
    df_bn_st_7_3['pre_open'] = current_candle_dict_info['pre_open']
    df_bn_st_7_3['pre_high'] = current_candle_dict_info['pre_high']
    df_bn_st_7_3['pre_low'] = current_candle_dict_info['pre_low']
    df_bn_st_7_3['pre_close'] = current_candle_dict_info['pre_close']
    df_bn_st_7_3['open_per'] = ((first_open_value - df_bn_st_7_3['open'])/first_open_value) * first_open_value
    df_bn_st_7_3['high_per'] = ((first_open_value - df_bn_st_7_3['high']) / first_open_value) * first_open_value
    df_bn_st_7_3['low_per'] = ((first_open_value - df_bn_st_7_3['low']) / first_open_value) * first_open_value
    df_bn_st_7_3['close_per'] = ((first_open_value - df_bn_st_7_3['close']) / first_open_value) * first_open_value
    new_data_frame_value = new_data_frame_value.append(df_bn_st_7_3)
    print()

new_data_frame_value.to_csv('df_bk_one_5min_data_trans.csv', index=False)
print()