from testing.strategies_formulas.strategy_conditions import *


def day_open_close_strategy(current_candle_dict_info):
    open_inside_candle_type = 'None'
    candle_type_red = current_candle_dict_info['candle_type'] == 'red candle'
    candle_type_green = current_candle_dict_info['candle_type'] == 'green candle'
    day_cur_open_pre_close_above = current_candle_dict_info['cur_open'] > current_candle_dict_info['pre_close']
    day_cur_close_pre_close_above = current_candle_dict_info['cur_close'] > current_candle_dict_info['pre_close']

    day_cur_open_pre_close_below = current_candle_dict_info['cur_open'] < current_candle_dict_info['pre_close']
    day_cur_close_pre_close_below = current_candle_dict_info['cur_close'] < current_candle_dict_info['pre_close']

    if candle_type_red and day_cur_open_pre_close_above and day_cur_close_pre_close_above:
        open_inside_candle_type = "pre_open_close_above_close_red"
    elif candle_type_green and day_cur_open_pre_close_above and day_cur_close_pre_close_above:
        open_inside_candle_type = "pre_open_close_above_close_green"
    elif candle_type_green and day_cur_open_pre_close_below and day_cur_close_pre_close_below:
        open_inside_candle_type = "pre_open_close_below_close_green"
    elif candle_type_red and day_cur_open_pre_close_below and day_cur_close_pre_close_below:
        open_inside_candle_type = "pre_open_close_below_close_red"
    elif day_cur_open_pre_close_below and day_cur_close_pre_close_above:
        open_inside_candle_type = "pre_open_below_close_above"
    elif day_cur_open_pre_close_above and day_cur_close_pre_close_below:
        open_inside_candle_type = "pre_open_above_close_below"
    return open_inside_candle_type


def pre_close_open_close_above_red(profit_loss_day_df, profit_loss_day_df_, df_bn_st_7_3, current_candle_dict_info):
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():
        first_entry_condition = profit_loss_day_df.shape[0] == 0
        second_entry_condition = current_candle_dict_info['candle_type'] == 'red candle'
        third_entry_condition = current_candle_dict_info['cur_open'] > current_candle_dict_info['pre_close']
        fourth_entry_condition = current_candle_dict_info['cur_close'] > current_candle_dict_info['pre_close']

        fifth_entry_condition = row_record.close > current_candle_dict_info['cur_high']
        sixth_entry_condition = (current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high']) < -250
        fifth_entry_condition1 = row_record.low > current_candle_dict_info['pre_high']
        all_conditions = first_entry_condition and second_entry_condition and third_entry_condition and fourth_entry_condition

        all_conditions1 = first_entry_condition and second_entry_condition and third_entry_condition and fourth_entry_condition and fifth_entry_condition1

        if all_conditions and current_candle_dict_info['cur_low'] > current_candle_dict_info['pre_close'] \
                and fifth_entry_condition  and current_candle_dict_info['pre_close'] < current_candle_dict_info['pre_open'] \
                and (row_record.close - current_candle_dict_info['pre_high']) < -150:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions  and current_candle_dict_info['pre_close'] > current_candle_dict_info['pre_open'] \
                and (row_record.close - current_candle_dict_info['pre_low']) < -200:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions and current_candle_dict_info['pre_close'] < current_candle_dict_info['pre_open'] \
                and (row_record.close - current_candle_dict_info['pre_low']) < -400:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
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

    return profit_loss_day_df, profit_loss_day_df_


def pre_close_open_close_above_green(profit_loss_day_df, profit_loss_day_df_, df_bn_st_7_3, current_candle_dict_info):
    ci = False
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():
        first_entry_condition = profit_loss_day_df.shape[0] == 0
        second_entry_condition = current_candle_dict_info['candle_type'] == 'green candle'
        third_entry_condition = current_candle_dict_info['cur_open'] > current_candle_dict_info['pre_close']
        fourth_entry_condition = current_candle_dict_info['cur_close'] > current_candle_dict_info['pre_close']
        fifth_entry_condition = row_record.close < current_candle_dict_info['pre_close']
        sixth_entry_condition = (current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high']) < 0
        sixth_entry_condition2 = (current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high']) > 0
        sixth_entry_condition1 = abs(current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high']) > 150
        all_conditions = first_entry_condition and second_entry_condition and third_entry_condition and fourth_entry_condition

        all_conditions2 = current_candle_dict_info['pre_close'] > current_candle_dict_info['pre_open']
        all_conditions1 = current_candle_dict_info['pre_close'] < current_candle_dict_info['pre_open']
        filter_ = str(current_candle_dict_info['candle_upper_wick']) + '_' + str(current_candle_dict_info['candle_lower_wick']) + '_' +\
                  str(current_candle_dict_info['candle_width'])+ '_' + str(current_candle_dict_info['cur_close'] > current_candle_dict_info['pre_open']) +\
                  '_' + str(int(current_candle_dict_info['pre_close'] - current_candle_dict_info['pre_low'])) +\
                  '_' + str((int(current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low'])))

        #if all_conditions and all_conditions1 and not current_candle_dict_info['cur_close'] > current_candle_dict_info['pre_open'] and row_record.close < current_candle_dict_info['pre_low']:
        # if all_conditions and all_conditions1 and current_candle_dict_info['cur_high'] < current_candle_dict_info['pre_open'] and row_record.low < current_candle_dict_info['pre_close'] and int(current_candle_dict_info['pre_low'] - row_record.close) < 50:

        if all_conditions and all_conditions1 and current_candle_dict_info['cur_high'] < current_candle_dict_info[
            'pre_open'] and row_record.low < current_candle_dict_info['pre_close'] and int(
                current_candle_dict_info['pre_low'] - row_record.close) < 50:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': filter_,
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions and row_record.open < current_candle_dict_info['cur_low'] and all_conditions2:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)


        if all_conditions and all_conditions2 and (current_candle_dict_info['cur_high'] - current_candle_dict_info[ 'pre_high']) > 0 :
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions and row_record.close - current_candle_dict_info['pre_high'] > 400:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': filter_,
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
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
    return profit_loss_day_df, profit_loss_day_df_



def pre_open_close_below_close_green(profit_loss_day_df, profit_loss_day_df_, df_bn_st_7_3, current_candle_dict_info):
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():
        first_entry_condition = profit_loss_day_df.shape[0] == 0
        second_entry_condition = current_candle_dict_info['candle_type'] == 'green candle'
        third_entry_condition = current_candle_dict_info['cur_open'] < current_candle_dict_info['pre_close']
        fourth_entry_condition = current_candle_dict_info['cur_close'] < current_candle_dict_info['pre_close']

        fifth_entry_condition = row_record.close < current_candle_dict_info['cur_low']
        sixth_entry_condition = row_record.low > current_candle_dict_info['pre_high']

        all_conditions = first_entry_condition and second_entry_condition and third_entry_condition and fourth_entry_condition

        if all_conditions and current_candle_dict_info['pre_open'] > current_candle_dict_info[
            'pre_close'] and current_candle_dict_info['pre_close'] - current_candle_dict_info['pre_low'] < 200:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions and row_record.close < current_candle_dict_info['cur_open'] and current_candle_dict_info[
            'pre_close'] - current_candle_dict_info['pre_low'] > 300:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions and row_record.low > current_candle_dict_info['pre_high']:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_high'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
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
    return profit_loss_day_df, profit_loss_day_df_


def pre_open_close_below_close_red(profit_loss_day_df, profit_loss_day_df_, df_bn_st_7_3, current_candle_dict_info):
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():
        first_entry_condition = profit_loss_day_df.shape[0] == 0
        second_entry_condition = current_candle_dict_info['candle_type'] == 'red candle'
        third_entry_condition = current_candle_dict_info['cur_open'] < current_candle_dict_info['pre_close']
        fourth_entry_condition = current_candle_dict_info['cur_close'] < current_candle_dict_info['pre_close']

        fifth_entry_condition = row_record.low > current_candle_dict_info['pre_low']
        sixth_entry_condition = (current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low']) < 0

        all_conditions = first_entry_condition and second_entry_condition and third_entry_condition and fourth_entry_condition and fifth_entry_condition

        if all_conditions and current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low'] < 150:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions and current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low'] > 150:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'down', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
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
    return profit_loss_day_df, profit_loss_day_df_


def pre_open_below_close_above(profit_loss_day_df, profit_loss_day_df_, df_bn_st_7_3, current_candle_dict_info):
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():
        first_entry_condition = profit_loss_day_df.shape[0] == 0
        second_entry_condition = current_candle_dict_info['candle_type'] == 'green candle'
        third_entry_condition = current_candle_dict_info['cur_open'] < current_candle_dict_info['pre_close']
        fourth_entry_condition = current_candle_dict_info['cur_close'] > current_candle_dict_info['pre_close']
        fifth_entry_condition = row_record.low > current_candle_dict_info['pre_low']
        sixth_entry_condition = (current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low']) < 0
        all_conditions = first_entry_condition and third_entry_condition and fourth_entry_condition

        cur_low = current_candle_dict_info['cur_low']
        pre_low = current_candle_dict_info['pre_low']

        if all_conditions and row_record.low < current_candle_dict_info['cur_open']:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
                              }
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        if all_conditions and current_candle_dict_info['pre_open'] > current_candle_dict_info[
            'pre_close']  and row_record.open > current_candle_dict_info['pre_high']:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
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
    return profit_loss_day_df, profit_loss_day_df_


def pre_open_above_close_below(profit_loss_day_df, profit_loss_day_df_, df_bn_st_7_3, current_candle_dict_info):
    for row_number, row_record in df_bn_st_7_3.iloc[1:].iterrows():

        first_entry_condition = profit_loss_day_df.shape[0] == 0
        second_entry_condition = current_candle_dict_info['candle_type'] == 'red candle'
        third_entry_condition = current_candle_dict_info['cur_open'] > current_candle_dict_info['pre_close']
        fourth_entry_condition = current_candle_dict_info['cur_close'] < current_candle_dict_info['pre_close']
        fifth_entry_condition = row_record.high < current_candle_dict_info['pre_close']
        sixth_entry_condition = (current_candle_dict_info['cur_low'] - current_candle_dict_info['pre_low']) < 0
        all_conditions = first_entry_condition and third_entry_condition and fourth_entry_condition

        if all_conditions and row_record.super_trend_direction_7_1 == 'up' and row_record.high < \
                current_candle_dict_info['pre_low']:
            profit_loss_df = {'date_on_str': row_record.date_on_str,
                              'date': current_candle_dict_info['date'],
                              'instrument': current_candle_dict_info['cur_open'] - current_candle_dict_info['pre_high'],
                              'traded_date_time': row_record.date,
                              'stop_loss': current_candle_dict_info['cur_high'],
                              'target_value': current_candle_dict_info['pre_close'] - (
                                      0.10 * current_candle_dict_info['pre_close'] / 100),
                              'direction': 'up', 'price': row_record.close,
                              'candle_position': "diff_super_trend"
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
    return profit_loss_day_df, profit_loss_day_df_