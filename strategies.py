import backtrader as bt

class MyStrategy(bt.Strategy):
    params = (
        ('ema_period', 7),
        ('atr_period', 7),
    )

    def __init__(self,datas):
        self.datas = datas
        self.ema = bt.indicators.ExponentialMovingAverage(
            self.datas[0].close, period=self.params.ema_period)
        print(self.ema)
        self.atr = bt.indicators.ATR(
            self.datas[0].low, self.datas[0].low, self.datas[0].close, period=self.params.atr_period)
        self.buy_price = None

    def next(self):
        # 计算上下轨
        upper_band = self.ema + 0.5 * self.atr
        lower_band = self.ema - 0.5 * self.atr

        # 如果价格大于上轨，买入
        if self.datas[0].close[0] > upper_band[0] and self.buy_price is None:
            self.buy_price = self.datas[0].close[0]
            self.buy()

        # 如果价格小于下轨，卖出
        elif self.datas[0].close[0] < lower_band[0] and self.buy_price is not None:
            self.sell(price=self.datas[0].close[0])
            self.buy_price = None

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {:.2f}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED, Price: {:.2f}'.format(order.executed.price))
