import pandas as pd
from datetime import datetime

df_bk_one_min_data = pd.read_csv('260105_bank_nifty_future.csv')
df_bk_one_min_data = df_bk_one_min_data.loc[:, ~df_bk_one_min_data.columns.str.contains('^Unnamed')]

df_bk_one_min_data['date'] = pd.to_datetime(df_bk_one_min_data['date'], format='%Y%m%d').dt.date
df_bk_one_min_data['time'] = pd.to_datetime(df_bk_one_min_data['time'], format='%H:%M').dt.time

df_bk_one_min_data['date_time'] = pd.to_datetime(
                                        df_bk_one_min_data.date.astype(str) + ' ' + df_bk_one_min_data.time.astype(str))

df_bk_one_min_data = df_bk_one_min_data[['date_time', 'open', 'high', 'low', 'close', 'volume']].sort_values(
                                                                                                         by='date_time')
df_bk_one_min_data.reset_index(inplace=True, drop=True)
df_bk_one_min_data.rename(columns={'date_time': 'date'}, inplace=True)

instrument_data_interval = df_bk_one_min_data.groupby(pd.Grouper(key='date', freq='3min')) \
    .agg({"open": "first", "close": "last", "low": "min", "high": "max", 'volume': 'sum'}).dropna(how='any')

instrument_data_interval.to_csv('df_bk_one_min_data.csv', index=True)
