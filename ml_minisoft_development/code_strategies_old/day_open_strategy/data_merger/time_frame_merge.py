import pandas as pd

df_bk_one_1min_data = pd.read_csv('df_bk_one_1min_data.csv')
df_bk_one_1min_data['date']  = (pd.to_datetime(df_bk_one_1min_data['date']))

df_bk_one_5min_data = pd.read_csv('df_bk_one_5min_data.csv')
df_bk_one_5min_data['date']  = (pd.to_datetime(df_bk_one_5min_data['date']))

merged_dataframe = pd.merge_asof(df_bk_one_1min_data, df_bk_one_5min_data, on="date")

print('')