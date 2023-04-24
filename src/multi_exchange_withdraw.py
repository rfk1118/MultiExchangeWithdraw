# multi_exchange_withdraw.py
"""
多交易所批量提币程序
author: shuai
twitter: @ShuaiL0
"""
import time
import pandas as pd
from exchange_utils import *
from exchange.okx.okx_withdraw import okx_withdraw
from exchange.binance.binance_withdraw import binance_withdraw
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

if __name__ == "__main__":

    # 打开地址文件
    address_file_path = '../data/deposit_address.csv'  # 提币地址文件路径
    sleep_time = 30  # 设置提币间隔(秒)

    address_data = pd.read_csv(address_file_path)

    for index, row in address_data.iterrows():
        # 提现操作的相关参数
        wallet_address = row['wallet_address']
        tag = row['tag']
        if pd.isna(tag):
            tag = None
        currency = row['currency']
        amount = row['amount']
        chain = row['chain']
        exchange_name = row['exchange_name']

        # 设置交易所
        api_keys = load_api_keys(exchange_name)
        exchange = init_exchange(exchange_name, **api_keys)
        print(f"开始执行 {exchange.name} 交易所的提现操作")
        if exchange_name.lower() == 'okx':
            okx_withdraw(exchange, wallet_address, tag, currency, amount, chain)
        # 其他交易所的提币操作将在此处添加
        elif exchange_name.lower() == 'binance':
            binance_withdraw(exchange, wallet_address, tag, currency, amount, chain)
        else:
            print('提现失败，不支持的交易所')

        # 提币完成后暂停一段时间
        print(f'提币成功，程序暂停 {sleep_time} 秒')
        time.sleep(sleep_time)
