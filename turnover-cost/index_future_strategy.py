from rqalpha.api import *
import pandas as pd
import numpy as np

fname = "C:\Users\jgtzsx01\Documents\workspace\zjsxzy_in_js\website\everyday-update\data\market.xlsx"

def change_code(old):
    if old.endswith(".SH"):
        return old[:6] + ".XSHG"
    if old.endswith(".SZ"):
        return old[:6] + ".XSHE"

def init(context):
    context.s = "000906.XSHG"
    context.df = pd.read_excel(fname, index_col=0)
    # context.df = context.df[context.df.index >= "2016-01-01"]
    context.position = "OUT"
    context.contract_name = "IF"
    contract = get_future_contracts(context.contract_name)
    context.hold_contract = contract[3]
    subscribe(context.hold_contract)

def before_trading(context):
    contract = get_future_contracts(context.contract_name)
    context.hold_contract = contract[3]
    subscribe(context.hold_contract)

def handle_bar(context, bar_dict):
    values = context.df[context.df.index <= context.now]["current return"]
    value = values[-1]
    # mean, std = values.mean(), values.std()
    # value = (value - mean) / std
    if context.position == "OUT" and value < -0.01:
        logger.info("buying")
        # order_target_percent(context.s, 1)
        buy_open('IF1609', 1)
        context.position = "LONG"
    if context.position == "LONG" and value > 0.:
        logger.info("selling")
        # order_target_percent(context.s, 0)
        current_contract = context.future_portfolio.positions.keys()[0]
        buy_close(current_contract, 1)
        sell_open(context.hold_contract, 1)
        context.position = "SHORT"
    if context.position == "SHORT" and value < -0.01:
        logger.info("buying")
        current_contract = context.future_portfolio.positions.keys()[0]
        sell_close(current_contract, 1)
        buy_open(context.hold_contract, 1)
        context.position = "LONG"
