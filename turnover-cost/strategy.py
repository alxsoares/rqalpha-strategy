from rqalpha.api import *
import pandas as pd
import numpy as np
import os

BY_STOCK_DIR = "D:/Data/avg_cost/by stock"
BY_DATE_DIR = "D:/Data/avg_cost/by date"
INDEX_COMPOMENT = "C:/Users/jgtzsx01/Documents/workspace/data/index-component"

def change_code(old):
    if old.endswith(".SH"):
        return old[:6] + ".XSHG"
    if old.endswith(".SZ"):
        return old[:6] + ".XSHE"

def reverse_code(old):
    if old.endswith(".XSHG"):
        return old[:6] + ".SH"
    if old.endswith(".XSHE"):
        return old[:6] + ".SZ"

def init(context):
    index = "000300"
    # df = pd.read_excel("%s/%s.xlsx"%(INDEX_COMPOMENT, index))
    # context.candidates = set([str(c) for c in df["code"].tolist()])
    context.counter = 0
    context.switch = 23
    # context.num_stocks = 30
    # context.long = 60
    # context.short = 10
    context.s = "300104.SZ"
    df = pd.read_excel("%s/%s.xlsx"%(BY_STOCK_DIR, context.s), index_col=0)
    df = df[df.index >= "2016-03-01"]
    df["current return"] = (df["close"] - df["avg cost"]) / df["avg cost"]
    df["rolling current return"] = df["current return"].rolling(window=7).mean()
    col_name = "rolling current return"
    df["z-score"] = (df[col_name] - df[col_name].mean()) / df[col_name].std()
    context.s = change_code(context.s)
    context.df = df
    context.threshold = 0.2
    context.bought = False

def rebalance(context, bar_dict):
    df = pd.read_excel("%s/%s.xlsx"%(BY_DATE_DIR, context.now.strftime("%Y-%m-%d")), index_col=0)
    df.sort_values("rolling current return", inplace=True)
    sorted_current_return = [(change_code(s), f) for (s, f) in zip(df.index, df["rolling current return"]) if s in context.candidates]
    num = 0
    stocks_buy = []
    for stock, current_return in sorted_current_return:
        his = history_bars(stock, context.long, '1d', 'close')
        long_mean = np.mean(his)
        short_mean = np.mean(his[-context.short:])
        if current_return < 0 and short_mean > long_mean:
            num += 1
            stocks_buy.append(stock)
        if num == context.num_stocks:
            break

    for stock in context.stock_portfolio.positions.keys():
        if not stock in stocks_buy:
            logger.info("selling %s"%(stock))
            order_target_percent(stock, 0)

    weight = 1. / len(stocks_buy)
    for stock in stocks_buy:
        logger.info("buying %s %.2f"%(stock, weight))
        order_target_percent(stock, weight)

def handle_bar(context, bar_dict):
    # if context.counter % context.switch == 0:
        # rebalance(context, bar_dict)
    z_score = context.df[context.df.index <= context.now]["z-score"][-1]
    # logger.info(z_score)
    if z_score < -context.threshold and not context.bought:
        order_target_percent(context.s, 1)
        context.bought = True

    if z_score > context.threshold and context.bought:
        order_target_percent(context.s, 0)
        context.bought = False

def after_trading(context):
    context.counter += 1
