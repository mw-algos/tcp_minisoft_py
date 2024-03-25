import pandas as pd
from datetime import datetime, time
import time
from common_code.strategies_formulas.first_candle_formulas import first_candle_type_input_build
from common_code.strategies_formulas.strategy_data import sup_trend

date_from = pd.to_datetime('2020-01-01')
df_bank_nifty_intraday_data = pd.read_csv('df_bk_one_5min_data_trans.csv', index_col=False)
df_bank_nifty_intraday_data = df_bank_nifty_intraday_data[df_bank_nifty_intraday_data['candle_position'] == 'OPEN_IN_SIDE_UP_CLOSE_OUT_SIDE']
df_bank_nifty_intraday_data