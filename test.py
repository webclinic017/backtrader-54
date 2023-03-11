import backtrader as bt
import pandas as pd
from strategies import MyStrategy
import datetime
import matplotlib.pyplot as plt

class My_CSVData(bt.feeds.GenericCSVData):
    params = (
    # ('fromdate', datetime.datetime(2019,1,2)),
    # ('todate', datetime.datetime(2021,1,28)),
    ('nullvalue', 0.0),
    ('dtformat', ('%Y-%m-%d %H:%M:%S')),
    ('datetime', 0),
    ('time', -1),
    ('high', 2),
    ('low', 3),
    ('open', 1),
    ('close', 4),
    ('volume', 5),
    ('openinterest', -1)
)
 
cerebro = bt.Cerebro()
data = My_CSVData(dataname='daily_price.csv')
cerebro.adddata(data, name='600466.SH')
rasult = cerebro.run()

datapath = './1.csv'
# 读取CSV文件
data = GenericCSVDataEx(
        dataname = datapath,
        nullvalue = 0.0,
        dtformat = ('%Y-%m-%d %H:%M:%S'),
        datetime = 0,
        open = 1,
        high = 2,
        low = 3,
        close = 4,
        volume = 5,
        rate = 6 
        )

# 运行回测
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
cerebro.adddata(data)
cerebro.run()

# 画出回测结果的图像
cerebro.plot()
plt.show()
