from __future__ import (absolute_import, division, print_function,unicode_literals)
import datetime 
import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    params = ( ('period', 21),  ('printlog', False),('margin', 0.2), )   
    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:            
            dt = dt or self.datas[0].datetime.date(0)           
            print('%s, %s' % (dt.isoformat(), txt))    

    def __init__(self):        

        self.dataclose = self.datas[0].close      
        self.datahigh = self.datas[0].high        
        self.datalow = self.datas[0].low     

        self.order = None      
        self.buyprice = 0      
        self.buycomm = 0      
        self.newstake = 0      
        self.buytime = 0       
        # 参数计算，唐奇安通道上轨、唐奇安通道下轨、ATR        
        self.DonchianHi = bt.indicators.Highest(self.datahigh(-1), period=self.params.period, subplot=False)        
        self.DonchianLo = bt.indicators.Lowest(self.datalow(-1), period=self.params.period, subplot=False)       
        self.TR = bt.indicators.Max((self.datahigh(0)- self.datalow(0)), abs(self.dataclose(-1) -  self.datahigh(0)), abs(self.dataclose(-1)  - self.datalow(0) ))        
        self.ATR = bt.indicators.SimpleMovingAverage(self.TR, period=self.params.period, subplot=True)       
        # 唐奇安通道上轨突破、唐奇安通道下轨突破       
        self.CrossoverHi = bt.ind.CrossOver(self.dataclose(0), self.DonchianHi)        
        self.CrossoverLo = bt.ind.CrossOver(self.dataclose(0), self.DonchianLo)
        self.broker.setcommission(commission=1/10000, margin=self.params.margin)
    
    
    def get_size(self,money,is_sell=0):
        position = self.broker.getposition(self.data).size
        if is_sell == 0:
            cash = money / self.params.margin
            price = self.data.close[0]
            size = int(cash / price)
            return size
        if is_sell == 1:
            return position
        
    def notify_order(self, order):        
        if order.status in [order.Submitted, order.Accepted]:            
            return

        if order.status in [order.Completed]:            
            if order.isbuy():               
                self.log(                    
                'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %                   
                (order.executed.price,
                order.executed.value,
                order.executed.comm),doprint=True)    
                self.buyprice = order.executed.price              
                self.buycomm = order.executed.comm            
            else:             
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %                        
                     (order.executed.price,
                     order.executed.value,
                     order.executed.comm),doprint=True)                             
                self.bar_executed = len(self)       
                self.buyprice = 0
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:           
            self.log('Order Canceled/Margin/Rejected')        
        self.order = None    

    def notify_trade(self, trade):      
        if not trade.isclosed:
            return        
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm)) 

    def next(self): 
        #入场        
        now_rate = self.data.lines.rate[0]
        position = self.broker.getposition(self.data).size
        # print(position,now_rate)
        if now_rate <= -0.1 * 0.01 and self.buyprice == 0 :
            self.buy(size=self.get_size(self.broker.get_cash()))
        if now_rate >= -0.1 * 0.01 and position != 0:
            self.sell(size=self.get_size(self.broker.get_cash(),is_sell=1))
            
    def stop(self):
        print('---------stop----------')
        print(bt.num2date(self.data.datetime[0]).isoformat())
        print('getcash 当前可用资金', self.broker.getcash())
        print('getvalue 当前总资产', self.broker.getvalue())
        print('self.stats 最大回撤', self.stats.drawdown.drawdown[0])