def init(context):
    context.coeff = 1.5254
    context.stock1 = "601939.XSHG"
    context.stock2 = "601398.XSHG"
    context.mean = -1.2796
    context.std = 0.16483534976
    context.up_line = context.mean + context.std
    context.down_line = context.mean - context.std
    context.price_diff = 0

def before_trading(context, bar_dict):
    pass

def handle_bar(context, bar_dict):
    yesterday_price1 = history(1, '1d', 'close')[context.stock1].values[0]
    yesterday_price2 = history(1, '1d', 'close')[context.stock2].values[0]
    context.price_diff = yesterday_price1 - context.coeff * yesterday_price2
    if context.price_diff > context.up_line:
        order_target_percent(context.stock1, 0)
        order_target_percent(context.stock2, 1)
    if context.price_diff < context.down_line:
        order_target_percent(context.stock1, 1)
        order_target_percent(context.stock2, 0)
