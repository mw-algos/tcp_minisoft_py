import pandas as pd
from datetime import datetime

df_bk_one_min_data = pd.read_csv('260105_bank_nifty_index.csv')
df_bk_one_min_data = df_bk_one_min_data.loc[:, ~df_bk_one_min_data.columns.str.contains('^Unnamed')]
df_bk_one_min_data['date'] = pd.to_datetime(df_bk_one_min_data['date'])
freq='15min'
instrument_data_interval = df_bk_one_min_data.groupby(pd.Grouper(key='date', freq=freq)) \
    .agg({"open": "first", "close": "last", "low": "min", "high": "max", 'volume': 'sum'}).dropna(how='any')

instrument_data_interval.to_csv(f'df_bk_one_{freq}_data.csv', index=True)
