def init(context):
    context.i = 0
    context.security = "000001.XSHE"
    context.hold = False

def handle_bar(context, bar_dict):
    context.i += 1
    if context.i < 30:
        return

    security = context.security

    short_mavg = history(10, '1d', 'close')[security].mean()
    long_mavg = history(30, '1d', 'close')[security].mean()

    if short_mavg > long_mavg and not context.hold:
        order_target_percent(security, 1)
        context.hold = True
    elif short_mavg < long_mavg and context.hold:
        order_target_percent(security, 0)
        context.hold = False
