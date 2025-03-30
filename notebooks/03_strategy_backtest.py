#%% [markdown]
# 技术指标组合策略回测

# 本notebook将演示如何：
# 1. 设计多指标组合交易信号
# 2. 实现简单的回测系统
# 3. 分析策略表现

#%% code
import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.indicators import calculate_macd, calculate_rsi, calculate_bollinger_bands

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # MacOS
plt.rcParams['axes.unicode_minus'] = False

#%% [markdown]
## 1. 加载数据并计算指标

#%% code
# 加载数据
df = pd.read_csv('../data/AAPL_data.csv', index_col=0, parse_dates=True)

# 重命名列以使其更易读
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# 计算技术指标
macd = calculate_macd(df['Close'])
rsi = calculate_rsi(df['Close'])
bb = calculate_bollinger_bands(df['Close'])

# 合并所有指标
df['MACD'] = macd['MACD']
df['Signal'] = macd['Signal']
df['RSI'] = rsi
df['BB_Upper'] = bb['Upper']
df['BB_Lower'] = bb['Lower']

df.head()

#%% [markdown]
## 2. 设计交易信号

#%% code
def generate_signals(df):
    """生成交易信号
    1: 买入信号
    -1: 卖出信号
    0: 无信号
    """
    signals = pd.Series(0, index=df.index)
    
    # MACD金叉 + RSI超卖
    buy_condition = (df['MACD'] > df['Signal']) & (df['RSI'] < 30)
    print(buy_condition)
    
    # MACD死叉 + RSI超买
    sell_condition = (df['MACD'] < df['Signal']) & (df['RSI'] > 70)
    
    signals[buy_condition] = 1
    signals[sell_condition] = -1
    
    return signals

# 生成信号
df['Signal'] = generate_signals(df)

# 显示信号分布
print('信号分布：')
print(df['Signal'].value_counts())

#%% [markdown]
## 3. 回测系统

#%% code
def backtest(df, initial_capital=100000):
    """简单的回测系统"""
    # position 表示当前持仓状态，0表示空仓，1表示持仓
    position = 0
    capital = initial_capital
    trades = []

    # 如果有买入信号，则用当天的收盘价买入
    for i in range(1, len(df)):
        if df['Signal'].iloc[i] == 1 and position == 0:  # 买入信号
            position = 1
            entry_price = df['Close'].iloc[i]
            trades.append({
                'type': 'buy',
                'date': df.index[i],
                'price': entry_price
            })

        # 如果有卖出信号，则用当天的收盘价卖出
        elif df['Signal'].iloc[i] == -1 and position == 1:  # 卖出信号
            position = 0
            exit_price = df['Close'].iloc[i]
            profit = (exit_price - entry_price) / entry_price
            capital *= (1 + profit)
            trades.append({
                'type': 'sell',
                'date': df.index[i],
                'price': exit_price,
                'profit': profit
            })
    
    return pd.DataFrame(trades), capital

# 运行回测
initial_capital = 100000
trades_df, final_capital = backtest(df, initial_capital)

# 显示回测结果
print(f'初始资金: ${initial_capital:,.2f}')
print(f'最终资金: ${final_capital:,.2f}')
print(f'总收益率: {(final_capital/initial_capital - 1)*100:.2f}%')
print(f'交易次数: {len(trades_df)}')

if len(trades_df) > 0:
    print('\n交易记录：')
    print(trades_df)

#%% [markdown]
## 4. 可视化回测结果

# 创建三个子图
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), height_ratios=[2, 1, 1])

# 绘制价格走势
ax1.plot(df.index, df['Close'], label='价格', color='blue')

# 标记买入点
buy_points = trades_df[trades_df['type'] == 'buy']
ax1.scatter(buy_points['date'], buy_points['price'], 
          color='green', marker='^', s=100, label='买入点')

# 标记卖出点
sell_points = trades_df[trades_df['type'] == 'sell']
ax1.scatter(sell_points['date'], sell_points['price'], 
          color='red', marker='v', s=100, label='卖出点')

ax1.set_title('交易信号可视化')
ax1.set_xlabel('日期')
ax1.set_ylabel('价格 (USD)')
ax1.legend()
ax1.grid(True)

# 绘制MACD
ax2.plot(df.index, df['MACD'], label='MACD', color='blue')
ax2.plot(df.index, df['Signal'], label='Signal', color='orange')
ax2.bar(df.index, df['MACD'] - df['Signal'], color='gray', alpha=0.3)
ax2.set_ylabel('MACD')
ax2.legend()
ax2.grid(True)

# 绘制RSI
ax3.plot(df.index, df['RSI'], label='RSI', color='purple')
ax3.axhline(y=70, color='r', linestyle='--', alpha=0.5)
ax3.axhline(y=30, color='g', linestyle='--', alpha=0.5)
ax3.set_ylabel('RSI')
ax3.legend()
ax3.grid(True)

# 调整子图之间的间距
plt.tight_layout()
plt.show()