import pandas as pd
# win_trade_percentage = 64.34 & profit_trade_percentage = -73.16 (profit) & profit_loss_sum = -35270.14999999998 & count = 258  & total = 357
from open_inside_close_inside_fun_1 import *
from testing.strategies_formulas.first_candle_formulas import first_candle_type_input_build
from testing.strategies_formulas.strategy_conditions import final_profit_cal
from testing.strategies_formulas.strategy_data import sup_trend

date_from = pd.to_datetime('2020-01-01')
df_bank_nifty_intraday_data = pd.read_csv('df_bk_one_min_data_5.csv')
df_bank_nifty_super_trend_7_3, df_bank_nifty_days_data = sup_trend(df_bank_nifty_intraday_data, date_from)

profit_loss_day_df_ = pd.DataFrame()
number_ = 1
number_of_orders = 0


for row_number_, row_record_ in df_bank_nifty_days_data.iloc[1:].iterrows():
    df_bn_st_7_3 = df_bank_nifty_super_trend_7_3[(df_bank_nifty_super_trend_7_3['date_on_str'] == row_record_.days)]
    df_bn_st_7_3.reset_index(drop=True, inplace=True)
    current_day = row_record_.days
    previous_day = df_bank_nifty_days_data.iloc[row_number_ - 1].days
    current_candle_dict_info = {'date': current_day}
    current_candle_dict_info = first_candle_type_input_build(df_bank_nifty_super_trend_7_3, current_day,
                                                             previous_day, current_candle_dict_info)

    open_inside_candle_type = day_open_close_strategy(current_candle_dict_info)
    if current_candle_dict_info['candle_position'] == 'OPEN_IN_SIDE_CLOSE_IN_SIDE':
        number_ = number_ + 1
        profit_loss_day_df_new = pd.DataFrame()
        profit_loss_day_df = pd.DataFrame()

        if open_inside_candle_type == "pre_open_close_above_close_red":
            profit_loss_day_df, profit_loss_day_df_ = pre_close_open_close_above_red(profit_loss_day_df,
                                                                                     profit_loss_day_df_,
                                                                                     df_bn_st_7_3,
                                                                                     current_candle_dict_info)

        if open_inside_candle_type == "pre_open_close_above_close_green":
            profit_loss_day_df, profit_loss_day_df_ = pre_close_open_close_above_green(profit_loss_day_df,
                                                                                       profit_loss_day_df_,
                                                                                       df_bn_st_7_3,
                                                                                       current_candle_dict_info)

        if open_inside_candle_type == "pre_open_close_below_close_green":
            profit_loss_day_df, profit_loss_day_df_ = pre_open_close_below_close_green(profit_loss_day_df,
                                                                                       profit_loss_day_df_,
                                                                                       df_bn_st_7_3,
                                                                                       current_candle_dict_info)

        if open_inside_candle_type == "pre_open_close_below_close_red":
            profit_loss_day_df, profit_loss_day_df_ = pre_open_close_below_close_red(profit_loss_day_df,
                                                                                     profit_loss_day_df_,
                                                                                     df_bn_st_7_3,
                                                                                     current_candle_dict_info)
        if open_inside_candle_type == "pre_open_below_close_above":
            profit_loss_day_df, profit_loss_day_df_ = pre_open_below_close_above(profit_loss_day_df,
                                                                                 profit_loss_day_df_,
                                                                                 df_bn_st_7_3,
                                                                                 current_candle_dict_info)
        if open_inside_candle_type == "pre_open_above_close_below":
            profit_loss_day_df, profit_loss_day_df_ = pre_open_above_close_below(profit_loss_day_df,
                                                                                 profit_loss_day_df_,
                                                                                 df_bn_st_7_3,
                                                                                 current_candle_dict_info)
profit_loss_day_df_ = final_profit_cal(profit_loss_day_df_)
profit_loss_day_df_.to_csv('profit_loss_day_df_.csv')
print(number_)
