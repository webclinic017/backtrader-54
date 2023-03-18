import pandas as pd

symbol = 'ETHUSDT'
# 读取CSV文件
df = pd.read_csv("./BNBUSDT.csv")

# 删除第一列
df = df.drop(df.columns[0], axis=1)

# 将结果保存到新的CSV文件
df.to_csv("BNBUSDT.csv", index=False)