def init(context):
    context.short_selling_allowed = True
    context.coeff = 1.5254
    context.stock1 = "601939.XSHG"
    context.stock2 = "601398.XSHG"
    context.mean = -1.5796
    context.std = 0.164835349769
    context.up_line = context.mean + 2 * context.std
    context.down_line = context.mean - 2 * context.std
    context.price_diff = 0

def before_trading(context, bar_dict):
    pass

def handle_bar(context, bar_dict):
    yesterday_price1 = history(1, '1d', 'close')[context.stock1].values[0]
    yesterday_price2 = history(1, '1d', 'close')[context.stock2].values[0]
    context.price_diff = yesterday_price1 - context.coeff * yesterday_price2
    total_money = context.portfolio.portfolio_value
    if context.price_diff > context.up_line:
        order_target_value(context.stock1, -total_money)
        order_target_value(context.stock2, total_money)
    if context.price_diff < context.down_line:
        order_target_value(context.stock1, total_money)
        order_target_value(context.stock2, -total_money)
