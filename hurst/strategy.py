from rqalpha.api import *
import numpy as np
import pandas as pd
from numpy import cumsum, log, polyfit, sqrt, std, subtract

CODE_DIR = "C:/Users/jgtzsx01/Documents/workspace/data/index-component/000300.xlsx"

def change_code(old):
    if old.endswith(".SH"):
        return old[:6] + ".XSHG"
    if old.endswith(".SZ"):
        return old[:6] + ".XSHE"

def init(context):
    context.index = "000300.XSHG"
    # context.index = "000906.XSHG" # 中证800
    df = pd.read_excel(CODE_DIR)
    context.stocks = [change_code(str(c)) for c in df["code"].tolist()]
    context.drop_window = 23
    context.hurst_window = 122
    context.volume_window = 122
    context.choose = 50
    context.counter = 0
    # scheduler.run_weekly(log_cash, 3)

'''
    Hurst exponent helps test whether the time series is:
    (1) A Random Walk (H ~ 0.5)
    (2) Trending (H > 0.5)
    (3) Mean reverting (H < 0.5)
'''
def hurst(ts):
    """Returns the Hurst Exponent of the time series vector ts"""
    # Create the range of lag values
    lags = range(2, 100)

    # Calculate the array of the variances of the lagged differences
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    # Use a linear fit to estimate the Hurst Exponent
    poly = polyfit(log(lags), log(tau), 1)

    # Return the Hurst exponent from the polyfit output
    return poly[0]*2.0

def before_trading(context):
    subscribe(context.stocks)

def rebalance(context, bar_dict):
    stock_drop = {}
    stock_dev = {}
    stock_hurst = {}
    for stock in context.stocks:
        stock_his = history_bars(stock, context.drop_window, '1d', 'close')
        if stock_his.shape[0] != context.drop_window:
            continue
        stock_return = (stock_his[-1] - stock_his[0]) / stock_his[0]
        stock_drop[stock] = stock_return

        stock_volume = history_bars(stock, context.volume_window, '1d', 'close')
        if stock_volumn[0] != context.volume_window:
            continue
        mean, std = np.mean(stock_volume), np.std(stock_volume)
        stock_dev[stock] = (stock_volume[-1] - mean) / std

        hurst_value = hurst(history_bars(stock, context.hurst_window, '1d', 'close'))
        stock_hurst[stock] = hurst_value

    sorted_stock_drop = sorted(stock_drop.items(), key=lambda x: x[1])
    sorted_stock_dev = sorted(stock_dev.items(), key=lambda x: x[1])
    sorted_stock_hurst = sorted(stock_hurst.items(), key=lambda x: x[1])

    stock_drop_list = [x for (x, v) in sorted_stock_drop[:context.choose]]
    stock_dev_list = [x for (x, v) in sorted_stock_dev[:context.choose]]
    stock_hurst_list = [x for (x, v) in sorted_stock_hurst[:context.choose]]

    stock_choose = []
    for stock in stock_hurst_list:
        if stock in stock_dev_list:
            if stock in stock_drop_list:
                stock_choose.append(stock)

    for stock in context.stock_portfolio.positions.keys():
        if stock not in stock_choose:
            order_target_percent(stock, 0)

    weight = 1.0 / len(stock_choose)
    # weight = {}
    # sum_weight = 0
    # for stock in stock_choose:
        # weight[stock] = abs(-stock_hurst[stock])
        # sum_weight += abs(-stock_hurst[stock])

    for stock in stock_choose:
        # weight[stock] /= sum_weight
        logger.info("%s -> %.2f"%(stock, weight))
        order_target_percent(stock, weight)

    return

def handle_bar(context, bar_dict):
    context.counter += 1
    if context.counter % 5 == 0:
        rebalance(context, bar_dict)

def after_trading(context):
    pass
