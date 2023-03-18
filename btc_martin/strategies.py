import backtrader as bt
import backtrader.indicators as btind
import pandas as pd
        
class MyStrategy(bt.Strategy):
    params = (
        ('margin', 0.1),
        ('slice', 10),
    )

    def __init__(self):
        self.ema = bt.talib.EMA(self.data.close,timeperiod=7) # ema的7日均线
        self.ema_21 = bt.talib.EMA(self.data.close,timeperiod=21) # ema的7日均线
        self.atr = bt.talib.ATR(self.data.high,
                                self.data.low,
                                self.data.close,
                                timeperiod=7)
        self.rsi = bt.talib.RSI(self.data.close, timeperiod=14)
        print(self.data0.lines.getlinealiases())
        self.broker.setcommission(commission=1/10000, margin=self.params.margin)
        
        self.trend = 0 #趋势信号，多为1，空为-1，funding < ema14 做多， funding > ema14 做空
        self.buy_time = 0 #买入次数
        self.high_price = 0 #最高价格
        self.low_price = 99999 #最低价格
        self.last_buy_price = 0 #上次买入价格
        self.avg_price = 0 #持仓平均价格
        self.one_piece_money = 0 #一手持仓金额
        self.total_piece = 0 #总共购买了的份数
        self.cover = 0 # 当前阶段有平仓


    def get_size(self):
        position = self.broker.getposition(self.data).size
        if position == 0:
            cash = self.broker.get_cash() * 0.9 / self.params.margin
            price = self.data.close[0]
            size = int(cash / price)
            return size
        if position > 0:
            return position
    
    def init(self):
        self.buy_time = 0 #买入次数
        self.high_price = 0 #最高价格
        self.low_price = 99999 #最低价格
        self.last_buy_price = 0 #上次买入价格
        self.avg_price = 0 #持仓平均价格
        self.one_piece_money = 0 
        self.total_piece = 0
        
    def next(self):
        self.cover = 0
        #判断当前处于的趋势
        now_rsi = self.rsi[0]
        now_ema = self.ema[0]
        now_ema_21 = self.ema_21[0]
        pre_ema = self.ema[-1]
        pre_ema_21 = self.ema_21[-1]
        datetime =  bt.num2date(self.data.datetime[0])
        # print(now_ema,now_ema_21,pre_ema,pre_ema_21,now_rsi,datetime)
        if now_ema > now_ema_21 and pre_ema < pre_ema_21:
            self.trend = 1 #买入信号
            print(f'更新买入信号，{datetime}')
        if now_ema < now_ema_21 and pre_ema > pre_ema_21:
            self.trend = -1 #卖出信号
            # print(f'更新卖出信号，{datetime}')
        if  30 < now_rsi < 70:
            self.trend = 0 #资金费率又开始无规律波动
        
        close = self.data.lines.close[0]
        high = self.data.lines.high[0]
        low = self.data.lines.low[0]
        atr = self.atr[0]
        ema = self.ema[0]
        
        #获取当前持仓
        position = self.broker.getposition(self.data).size
        
        #更新最高价，最低价
        if position != 0:
            self.high_price = max(self.high_price, high)
            self.low_price = min(self.low_price, low)
        #检测是否平仓
        if position > 0 :
            if (close < ema - atr or self.trend != 1) and close > self.avg_price * 1.01: 
                self.sell(size=position)
                self.init()
                self.cover = 1
                print(f'平仓，多,数量{position}，价格{close}')
                
        if position < 0 :
            if (close > ema + atr or self.trend != -1) and close < self.avg_price * 0.99:
                self.buy(size=-position)
                self.cover = 1
                print(f'平仓，空,数量{position}，价格{close},平均成本{self.avg_price}')
                self.init()
                
        #初始开仓买入
        if self.trend == 1 and self.avg_price == 0 and close > ema + atr * 0.5 and self.cover == 0 :
            money = self.broker.get_cash() / self.params.margin
            self.one_piece_money = money / self.params.slice
            qty = self.one_piece_money / close
            self.buy(size=qty)
            self.last_buy_price = self.data.close[0]
            self.avg_price  = close
            self.total_piece += 1
            print(f'初始买入，多,数量{qty}，价格{close}')
        
        #初始开仓卖出
        if self.trend == -1 and self.avg_price == 0 and close < ema - atr * 0.5 and self.cover == 0:
            money = self.broker.get_cash() / self.params.margin
            self.one_piece_money = money / self.params.slice
            qty = self.one_piece_money / close
            self.sell(size=qty)
            self.last_buy_price = self.data.close[0]
            self.avg_price = close
            self.total_piece += 1
            print(f'初始买入，空,数量{qty}，价格{close}')
            
        #逆趋势加仓/多
        if position > 0 and self.total_piece <= self.params.slice - 2  and self.cover == 0:
            if close < self.last_buy_price - atr and close > self.low_price + 0.5 * atr:
                qty = self.one_piece_money * 2 / close
                self.buy(size=qty)
                #更新平均持仓价
                self.avg_price = (position * self.avg_price + self.one_piece_money * 2) / (position + qty)
                #更新上次购买价格
                self.last_buy_price = self.data.close[0]
                self.total_piece += 2
                print(f'逆势加仓，多,数量{qty}，价格{close}')
                    
        #逆趋势加仓/空
        if position < 0 and self.trend != -1 and self.total_piece <= self.params.slice - 2 and self.cover == 0:
            if close > self.last_buy_price + atr and close < self.high_price - 0.5 * atr:
                qty = self.one_piece_money * 2 / close
                self.sell(size=qty)
                #更新平均持仓价
                self.avg_price = (-position * self.avg_price + self.one_piece_money * 2) / (-position + qty)
                #更新上次购买价格
                self.last_buy_price = self.data.close[0]
                self.total_piece += 2
                print(f'逆势加仓，空,数量{qty}，价格{close}')
        
        #顺势加仓/多
        if position > 0 and self.trend == 1 and self.total_piece <= self.params.slice - 1 and close > self.last_buy_price + atr and self.cover == 0:
            qty = self.one_piece_money / close
            self.buy(size=qty)
            self.last_buy_price = self.data.close[0]
            self.total_piece += 1
            self.avg_price = (position * self.avg_price + self.one_piece_money) / (position + qty)
            print(f'顺势加仓，多,数量{qty}，价格{close}')
            
        #顺势加仓/空
        if position < 0 and self.trend == -1 and self.total_piece <= self.params.slice - 1 and close < self.last_buy_price - atr and self.cover == 0:
            qty = self.one_piece_money / close
            self.sell(size=qty)
            self.last_buy_price = self.data.close[0]
            self.total_piece += 1
            self.avg_price = (-position * self.avg_price + self.one_piece_money) / (-position + qty)
            print(f'顺势加仓，空,数量{qty}，价格{close}')
    
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
        print(bt.num2date(self.data.datetime[-1]).isoformat())
        print('self.stats 当前可用资金', self.stats.broker.cash[0])
        print('self.stats 当前总资产', self.stats.broker.value[0])
        print('self.stats 最大回撤', self.stats.drawdown.drawdown[0])
        # print('self.stats 收益', self.stats.timereturn.line[0])