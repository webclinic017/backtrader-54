import backtrader as bt
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from strategies import MyStrategy
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
    # -1表示自动按列明匹配数据，也可以设置为线在数据源中列的位置索引 (('pe',6),('pb',7),)
# class TestStrategy(bt.Strategy):
#     def __init__(self):
#         print("--------- 打印 self.datas 第一个数据表格的 lines ----------")
#         print(self.data0.lines.getlinealiases())
#         print("rate", self.data0.lines.rate[0])
        
data1 = pd.read_csv('./data/1.csv')
data1['open_time'] = pd.to_datetime(data1['open_time'])
# 导入的数据 data1 中
cerebro = bt.Cerebro()
st_date = datetime.datetime(2019,1,2)
ed_date = datetime.datetime(2021,1,28)
datafeed1 = PandasData_more(dataname=data1)
cerebro.adddata(datafeed1, name='600466.SH')
cerebro.addstrategy(MyStrategy)
rasult = cerebro.run()

# 画出回测结果的图像
cerebro.plot()
plt.show()
 