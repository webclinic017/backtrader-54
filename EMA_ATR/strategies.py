import backtrader as bt
import backtrader.indicators as btind
import pandas as pd
        
class MyStrategy(bt.Strategy):
    params = (
        ('margin', 0.1),
    )

    def __init__(self):
        self.sma7 = btind.SimpleMovingAverage(period=7) # 10日均线
        self.atr7 = bt.talib.ATR(self.data.high,
                                self.data.low,
                                self.data.close,
                                timeperiod=7) * 0.5
        self.buy_price = None
        print(self.data0.lines.getlinealiases())
        print(self.data.lines.rate[0])
        self.broker.setcommission(commission=1/10000, margin=self.params.margin)


    def get_size(self):
        position = self.broker.getposition(self.data).size
        if position == 0:
            cash = self.broker.get_cash() * 0.9 / self.params.margin
            price = self.data.close[0]
            size = int(cash / price)
            return size
        if position > 0:
            return position
        
    def next(self):
        # print(f'sma5:{self.sma5[0]},sma5_1:{self.sma5[-1]}')
        # 如果价格大于上轨，买入
        now_rate = self.data.lines.rate[0]
        if now_rate < -0.1 * 0.01 and self.data.close[0] > (self.sma7[0] + self.atr7[0])  and self.buy_price is None:
            print(f'buy close price : {self.data.close[0]} atr price {self.atr7[0]} now rate {now_rate}')
            self.buy(size=self.get_size())
            

        # 如果价格小于下轨，卖出
        elif (now_rate > -0.1 * 0.01 or self.data.close[0] < (self.sma7[0] - self.atr7[0])) and self.buy_price is not None:
            print(f'sell close price : {self.data.close[0]} atr price {self.atr7[0]} now rate {now_rate} last buy price {self.buy_price}')
            self.sell(size=self.get_size())
            

    def notify_order(self, order):
        if order.status == order.Completed:
            if order.isbuy():
                self.buy_price = order.executed.price
                print('Buy order completed. Price: {}, Size: {}, Value: {}, Commission: {}'.format(
                    order.executed.price,
                    order.executed.size,
                    order.executed.value,
                    order.executed.comm
                ))
            elif order.issell():
                self.buy_price = None
                print('Sell order completed. Price: {}, Size: {}, Value: {}, Commission: {}'.format(
                    order.executed.price,
                    order.executed.size,
                    order.executed.value,
                    order.executed.comm
                ))


    def stop(self):
        print('---------stop----------')
        print(bt.num2date(self.data.datetime[0]).isoformat())
        print('getcash 当前可用资金', self.broker.getcash())
        print('getvalue 当前总资产', self.broker.getvalue())
        print(bt.num2date(self.data.datetime[-1]).isoformat())
        print('self.stats 当前可用资金', self.stats.broker.cash[0])
        print('self.stats 当前总资产', self.stats.broker.value[0])
        print('self.stats 最大回撤', self.stats.drawdown.drawdown[0])
        # print('self.stats 收益', self.stats.timereturn.line[0])