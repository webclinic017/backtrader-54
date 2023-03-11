import backtrader as bt
import backtrader.indicators as btind

class MyStrategy(bt.Strategy):
    params = (
        ('ema_period', 7),
        ('atr_period', 7),
    )

    def __init__(self):
        self.sma5 = btind.SimpleMovingAverage(period=5) # 5日均线
        self.sma10 = btind.SimpleMovingAverage(period=10) # 10日均线
        self.buy_price = None

    def next(self):
        # print(f'sma5:{self.sma5[0]},sma5_1:{self.sma5[-1]}')
        # 如果价格大于上轨，买入
        if self.sma5[0] > self.sma10[0] and self.sma5[-1] < self.sma10[-1] and self.buy_price is None:
            self.buy()
            

        # 如果价格小于下轨，卖出
        elif self.sma5[0] <= self.sma10[0] and self.sma5[-1] > self.sma10[-1] and self.buy_price is not None:
            self.sell()
            self.buy_price = None

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                print('BUY EXECUTED, Price: {:.2f}'.format(order.executed.price))
                self.buy_price = order.executed.price
            elif order.issell():
                print('SELL EXECUTED, Price: {:.2f}'.format(order.executed.price))
