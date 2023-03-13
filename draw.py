import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('./data/1.csv')

# 将"open_time"列解析为日期时间格式
df['open_time'] = pd.to_datetime(df['open_time'])

# 创建第一个坐标轴
fig, ax1 = plt.subplots(figsize=(10,5))
ax1.set_xlabel('Time')
ax1.set_ylabel('Closing Price')
ax1.plot(df['open_time'], df['close'], label='Closing Price')
ax1.tick_params(axis='y')

# 创建第二个坐标轴
ax2 = ax1.twinx()
ax2.set_ylabel('Rate')
ax2.plot(df['open_time'], df['rate'], label='Rate')
ax2.tick_params(axis='y')

# 添加图例和标题
plt.title('Closing Price and Rate Over Time')
fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)

# 显示图形
plt.show()