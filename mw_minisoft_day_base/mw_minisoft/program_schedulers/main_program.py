import os
import sys

import pandas as pd

from mw_minisoft.historical_feed.historical_feed import *
from mw_minisoft.instruments_operations.instrument_read_write_operations import download_write_instrument_tokens
from mw_minisoft.order_management.generate_strategy_orders import storage_regular_orders
from mw_minisoft.persistence_operations.account_management import *
from mw_minisoft.trade_lib.session_builder.retrive_request_token import generate_user_session
from mw_minisoft.trade_logger.logger import cus_logger


def user_account_balance():
    user_amount = pd.DataFrame()
    user_accounts = pd.read_csv(USER_INPUTS_FILE)
    for user_account_index, user_account in user_accounts.iterrows():
        user_session = generate_user_session(user_account)
        user_data = pd.DataFrame(user_session.funds()['fund_limit'])
        user_data_balance = user_data[user_data['title'] == 'Total Balance']
        user_data_df = {'date': str(date.today()), 'user_name': user_account['name'],
                        'user_id': user_account.user_id,
                        'balance': "{:,}".format(int(user_data_balance.equityAmount.values[0]))}
        user_amount = user_amount.append(user_data_df, ignore_index=True)
    user_amount.to_csv('resources/telegram/user_amount.csv', index=False)
    print(user_amount)


def ticks_indi_file_update():
    trade_inst = pd.read_csv('resources/account_data/account/trade_inst.csv')

    ticks_indi_template = pd.read_csv('resources/account_data/account/ticks_indi_template.csv')
    ticks_indi_file = pd.read_csv('resources/account_data/account/ticks_indi.csv')
    ticks_indi_file = ticks_indi_file.iloc[0:0]

    for trade_inst_index, trade_inst_record in trade_inst.iterrows():
        if trade_inst_record.inst_date_diff == 0:
            segment = trade_inst_record.inst_segment
            inst_name = trade_inst_record.inst_name
            inst_name_tem = ticks_indi_template.instrument_name
            ticks_indi_template = ticks_indi_template[inst_name_tem == segment+':'+inst_name]
            ticks_indi_file.append(ticks_indi_template.head(1), ignore_index = True)
    ticks_indi_template.to_csv('resources/account_data/account/ticks_indi.csv', index=False)


def strategy_execution_steps(auto_inputs):
    """
    New instrument data will be added, and technical values will be generated on top of it; recently,
    the order management process will begin.
    """
    # user_account_balance()
    generate_historical_data(auto_inputs)
    model_indicator_data_generator(auto_inputs)
    storage_regular_orders(auto_inputs)
    # place_regular_orders(auto_inputs)
    # write_user_positions()


def remove_create_dir():
    """
    All files such as order, user order, and ticks will be deleted.
    """
    # folders = [ORDERS_FOLDER_, TICKS_FOLDER_, USER_ORDERS_FOLDER_, USER_ORDERS_POSITIONS_]
    folders = [TICKS_FOLDER_, USER_ORDERS_POSITIONS_]
    cus_logger.info('The process of deleting old files has begun.')
    for folder in folders:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            os.remove(file_path)


def execute_strategy_programs():
    """
    A user session token will be generated, and the most recent instruments file will be downloaded and saved to the
    local directory.
    """
    cus_logger.info("strategy execution started")
    auto_inputs = pd.read_csv(AUTO_INPUTS_FILE)
    user_info = pd.read_csv(USER_INPUTS_FILE)
    user_info = user_info[user_info.day != date.today().day]

    if user_info.shape[0] > 0:
        download_each_user_tokens()
        download_write_instrument_tokens()
        calculate_expiry_date()
        ticks_indi_file_update()
        remove_create_dir()

    strategy_execution_steps(auto_inputs)
    cus_logger.info("strategy execution completed")


def scheduler_main_program_run(env, minutes, super_trend_period, super_trend_multiplier):
    """
    This function will update the input parameters and launch the main programme.
    """
    try:
        cus_logger.info("%s main program execution started", env)
        update_auto_inputs(env, minutes, super_trend_period, super_trend_multiplier)
        execute_strategy_programs()
        cus_logger.info("%s main program execution ended", env)
        sys.exit()
    except Exception as exception:
        cus_logger.exception(exception)