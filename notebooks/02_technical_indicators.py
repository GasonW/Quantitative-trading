#%% [markdown]
# 技术指标计算与可视化

# 本notebook将演示如何：
# 1. 计算MACD、RSI和布林带指标
# 2. 可视化技术指标
# 3. 分析不同参数对指标的影响

#%% code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.indicators import calculate_macd, calculate_rsi, calculate_bollinger_bands

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # MacOS
plt.rcParams['axes.unicode_minus'] = False
print("block done")

#%% [markdown]
## 1. 加载数据

#%% code
# 加载苹果公司数据作为示例
df = pd.read_csv('../data/AAPL_data.csv', index_col=0, parse_dates=True)
df.head()

#%% [markdown]
## 2. 计算技术指标

#%% code
# 计算MACD
macd = calculate_macd(df['4. close'])

# 计算RSI
rsi = calculate_rsi(df['4. close'])

# 计算布林带
bb = calculate_bollinger_bands(df['4. close'])

print('MACD指标示例：')
print(macd.head())
print('\nRSI指标示例：')
print(rsi.head())
print('\n布林带指标示例：')
print(bb.head())

#%% [markdown]
## 3. 可视化技术指标

#%% code
# 创建子图
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))

# 绘制价格和布林带
ax1.plot(df.index, df['4. close'], label='价格', color='blue')
ax1.plot(bb.index, bb['Upper'], '--', label='上轨', color='gray')
ax1.plot(bb.index, bb['Middle'], '--', label='中轨', color='gray')
ax1.plot(bb.index, bb['Lower'], '--', label='下轨', color='gray')
ax1.set_title('价格与布林带')
ax1.legend()
ax1.grid(True)

# 绘制MACD
ax2.plot(macd.index, macd['MACD'], label='MACD', color='blue')
ax2.plot(macd.index, macd['Signal'], label='信号线', color='orange')
ax2.bar(macd.index, macd['Histogram'], label='MACD柱状图', color='gray', alpha=0.3)
ax2.set_title('MACD指标')
ax2.legend()
ax2.grid(True)

# 绘制RSI
ax3.plot(rsi.index, rsi, label='RSI', color='purple')
ax3.axhline(y=70, color='r', linestyle='--')
ax3.axhline(y=30, color='g', linestyle='--')
ax3.set_title('RSI指标')
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.show()

#%% [markdown]
## 4. 参数敏感性分析

#%% code
# 测试不同的MACD参数
macd_params = [
    (12, 26, 9),  # 标准参数
    (5, 35, 5),   # 快速参数
    (21, 55, 9)   # 慢速参数
]

plt.figure(figsize=(15, 10))

for i, (fast, slow, signal) in enumerate(macd_params, 1):
    macd_test = calculate_macd(df['4. close'], fast, slow, signal)
    
    plt.subplot(3, 1, i)
    plt.plot(macd_test.index, macd_test['MACD'], label='MACD', color='blue')
    plt.plot(macd_test.index, macd_test['Signal'], label='信号线', color='orange')
    plt.bar(macd_test.index, macd_test['Histogram'], label='MACD柱状图', color='gray', alpha=0.3)
    plt.title(f'MACD参数 ({fast}, {slow}, {signal})')
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show() 