import backtrader as bt
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from strategies import MyStrategy
symbol = 'RLCUSDT'
class PandasData_more(bt.feeds.PandasData):
    lines = ('rate',) # 要添加的线
    # 设置 line 在数据源上的列位置
    params=(
        ('nullvalue', 0.0),
        ('dtformat', ('%Y-%m-%d %H:%M:%S')),
        ('datetime', 0),
        ('time', -1),
        ('high', 2),
        ('low', 3),
        ('open', 1),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
        ('rate', -1),
        )
    
data1 = pd.read_csv(f'./data/{symbol}.csv')
data1['open_time'] = pd.to_datetime(data1['open_time'])
# 导入的数据 data1 中
cerebro = bt.Cerebro()
cerebro.addobserver(bt.observers.DrawDown)
initial_cash = 1000
cerebro.broker.set_cash(initial_cash)
datafeed1 = PandasData_more(dataname=data1)
cerebro.adddata(datafeed1, name='600466.SH')
cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='_TimeDrawDown')
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
cerebro.addstrategy(MyStrategy)
results = cerebro.run()

colors = ['#729ece', '#ff9e4a', '#67bf5c', '#ed665d', '#ad8bc9', '#a8786e', '#ed97ca', '#a2a2a2', '#cdcc5d', '#6dccda']
tab10_index = [3, 0, 2, 1, 2, 4, 5, 6, 7, 8, 9]
cerebro.plot(iplot=False,  
              style='line', 
              lcolors=colors ,
              plotdist=0.1, 
              bartrans=0.2, 
              volup='#ff9896', 
              voldown='#98df8a', 
              loc='#5f5a41',
              grid=False)
# cerebro.plot(style='candlestick', iplot=False, use='tkinter')
plt.show()
 