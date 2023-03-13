import talib
import pandas as pd
import numpy as np

df = pd.read_csv('./data/1.csv')
close = df['close']

stochrsi_k = talib.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

print(stochrsi_k[0])
print(stochrsi_k[1])

