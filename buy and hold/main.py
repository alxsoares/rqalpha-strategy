"""
策略：买入并持有security
"""

def init(context):
    # context.s1 = "000001.XSHE"
    context.s1 = "000902.XSHG"
    context.fired = False

def handle_bar(context, bar_dict):
    if not context.fired:
        order_percent(context.s1, 1)
        context.fired = True
