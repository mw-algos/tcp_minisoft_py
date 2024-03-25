import pandas as pd


def last_candle_exit(profit_loss_day_df, row_record):
    if profit_loss_day_df.tail(1).direction.values[0] == 'up':
        profit_loss_df = {'date_on_str': row_record.date_on_str , 'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                          'direction': 'down', 'price': row_record.close }
        profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)
    elif profit_loss_day_df.tail(1).direction.values[0] == 'down':
        profit_loss_df = {'date_on_str': row_record.date_on_str , 'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                          'direction': 'up', 'price': row_record.close}
        profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

    return profit_loss_day_df


def day_wise_profit_cal(profit_loss_day_df_, profit_loss_day_df):
    profit_loss_day_df_1 = profit_loss_day_df.iloc[0]
    profit_loss_day_df_2 = profit_loss_day_df.iloc[1]
    if profit_loss_day_df_1.direction == 'up':
        profit_loss_day_record_wise_dict = {'date_on_str': profit_loss_day_df_1.date_on_str,
                                            'instrument': profit_loss_day_df_1.instrument,
                                            'buy_traded_date_time': profit_loss_day_df_1.traded_date_time,
                                            'buy_direction': 'up',
                                            'buy_price': profit_loss_day_df_1.price,
                                            'sell_traded_date_time': profit_loss_day_df_2.traded_date_time,
                                            'sell_direction': 'down',
                                            'sell_price': profit_loss_day_df_2.price,
                                            'candle_position': profit_loss_day_df_1.candle_position

                                            }
        profit_loss_day_df_ = profit_loss_day_df_.append(profit_loss_day_record_wise_dict,
                                                         ignore_index=True)
        profit_loss_day_df = pd.DataFrame()
        # break
    elif profit_loss_day_df_1.direction == 'down':
        profit_loss_day_record_wise_dict = {
                                            'date_on_str': profit_loss_day_df_2.date_on_str,
                                            'instrument': profit_loss_day_df_1.instrument,
                                            'buy_traded_date_time': profit_loss_day_df_2.traded_date_time,
                                            'buy_direction': 'up',
                                            'buy_price': profit_loss_day_df_2.price,
                                            'sell_traded_date_time': profit_loss_day_df_1.traded_date_time,
                                            'sell_direction': 'down',
                                            'sell_price': profit_loss_day_df_1.price,
                                            'candle_position': profit_loss_day_df_1.candle_position


                                            }
        profit_loss_day_df_ = profit_loss_day_df_.append(profit_loss_day_record_wise_dict,
                                                         ignore_index=True)
        profit_loss_day_df = pd.DataFrame()

    return profit_loss_day_df_, profit_loss_day_df


def final_profit_cal(profit_loss_day_df_):
    profit_loss_day_df_['profit_loss'] = profit_loss_day_df_.buy_price - profit_loss_day_df_.sell_price
    # win_trade_percentage = 68.28 & profit_trade_percentage = -61.44 (profit)
    win_trade_percentage = round((((profit_loss_day_df_[profit_loss_day_df_['profit_loss'] < 0]).shape[0]) /
                                  (profit_loss_day_df_.shape[0])) * 100, 2)
    profit_trade_percentage = round((sum(profit_loss_day_df_[profit_loss_day_df_['profit_loss'] < 0].profit_loss)) /
                                    ((sum(profit_loss_day_df_[profit_loss_day_df_['profit_loss'] > 0].profit_loss)) -
                                     (sum(profit_loss_day_df_[profit_loss_day_df_['profit_loss'] < 0].profit_loss))) *
                                    100, 2)

    profit_loss_sum = sum(profit_loss_day_df_['profit_loss'])
    count = profit_loss_day_df_.shape[0]
    print(f'win_trade_percentage = {win_trade_percentage} '
          f'& profit_trade_percentage = {profit_trade_percentage} (profit) '
          f'& profit_loss_sum = {profit_loss_sum}'
          f' & count = {count}')


    profit_loss_day_df_['qty'] = 0
    for row_number_1, row_record_1 in profit_loss_day_df_.iterrows():
        if row_number_1 == 0:
            profit_loss_day_df_.loc[row_number_1, 'qty'] = 1
        elif profit_loss_day_df_.loc[row_number_1 - 1].profit_loss > 0:
            profit_loss_day_df_.loc[row_number_1, 'qty'] = profit_loss_day_df_.iloc[row_number_1 - 1].qty + 1

        elif profit_loss_day_df_.loc[row_number_1 - 1].profit_loss < 0:
            profit_loss_day_df_.loc[row_number_1, 'qty'] = 1

    profit_loss_day_df_['profit_loss_points'] = profit_loss_day_df_['qty'] * profit_loss_day_df_['profit_loss']

    return profit_loss_day_df_


def exit_conditions_01(profit_loss_day_df, row_record, points):
    profit_loss_day_df_record = profit_loss_day_df.iloc[0]
    if profit_loss_day_df_record.direction == 'up':
        if row_record.close > profit_loss_day_df_record.target_price:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'down', 'price': profit_loss_day_df_record.target_price}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif profit_loss_day_df_record.stop_loss < row_record.close:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'stop_loss_hit', 'price': profit_loss_day_df_record.stop_loss}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

    elif profit_loss_day_df_record.direction == 'down':
        if row_record.close < profit_loss_day_df_record.target_price:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'up', 'price': profit_loss_day_df_record.target_price}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif row_record.close > profit_loss_day_df_record.stop_loss:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'down', 'price': profit_loss_day_df_record.stop_loss}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

    return profit_loss_day_df


def back_exit_conditions_01(profit_loss_day_df, row_record, points):
    profit_loss_day_df_record = profit_loss_day_df.iloc[0]
    diff = profit_loss_day_df_record.price - row_record.close
    if profit_loss_day_df_record.direction == 'up':
        if diff < -points:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'up', 'price': row_record.close}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)
        elif diff > 0:
            if row_record.close < profit_loss_day_df_record.stop_loss:
                profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                                  'direction': 'stop_loss_hit', 'price': row_record.close}
                profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

    elif profit_loss_day_df_record.direction == 'down':
        if diff > points:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'up', 'price': row_record.close}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif diff < 0:
            if row_record.close > profit_loss_day_df_record.stop_loss:
                profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                                  'direction': 'stop_loss_hit', 'price': row_record.close}
                profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

    return profit_loss_day_df


def exit_conditions_02_super(profit_loss_day_df, row_record, points):
    profit_loss_day_df_record = profit_loss_day_df.iloc[0]
    if profit_loss_day_df_record.direction == 'up':
        if (row_record.super_trend_direction_7_3 == 'down') & (
                row_record.close > profit_loss_day_df_record.price + 100):
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'down', 'price': row_record.close}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif profit_loss_day_df_record.stop_loss < row_record.close:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'stop_loss_hit', 'price': row_record.close}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

    elif profit_loss_day_df_record.direction == 'down':

        if (row_record.super_trend_direction_7_3 == 'up') & (
                row_record.close < profit_loss_day_df_record.price - 100):
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'up', 'price': row_record.close}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

        elif row_record.close > profit_loss_day_df_record.stop_loss:
            profit_loss_df = {'instrument': 'bank_nifty', 'traded_date_time': row_record.date,
                              'direction': 'stop_loss_hit', 'price': row_record.close}
            profit_loss_day_df = profit_loss_day_df.append(profit_loss_df, ignore_index=True)

    return profit_loss_day_df
