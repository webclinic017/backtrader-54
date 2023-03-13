import backtrader as bt
import backtrader.indicators as btind
import pandas as pd
        
class MyStrategy(bt.Strategy):
    params = (
        ('margin', 0.1),
    )

    def __init__(self):
        # 计算stoch rsi,返回两个pandas series,第一个是K线，第二个是d线
        self.stochrsi_k,self.stochrsi_d = bt.talib.STOCHRSI(self.data.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.adx = bt.talib.ADX(self.data.high, self.data.low, self.data.close, timeperiod=14)
        self.broker.setcommission(commission=1/10000, margin=self.params.margin)
        print(self.stochrsi_k)


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
        now_adx = self.adx[0]
        now_stochrsi_k = self.stochrsi_k[0]
        pre_stochrsi_k = self.stochrsi_k[-1]
        now_stochrsi_d = self.stochrsi_d[0]
        pre_stochrsi_d = self.stochrsi_d[-1]
        
        
        # 买入的情况，ADX > 50,K>D且<30
        if now_adx > 50 and now_stochrsi_k > now_stochrsi_d and pre_stochrsi_k < pre_stochrsi_d and now_stochrsi_k < 30 and now_stochrsi_d < 30:
            self.buy(size=self.get_size())

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