import numpy as np
import pandas as pd

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    计算MACD指标
    
    参数:
    prices: 价格序列
    fast: 快速EMA周期
    slow: 慢速EMA周期
    signal: 信号线周期
    
    返回:
    DataFrame包含MACD、信号线和MACD柱状图
    """
    # 计算快速和慢速EMA
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    
    # 计算MACD线
    macd_line = ema_fast - ema_slow
    
    # 计算信号线
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    
    # 计算MACD柱状图
    macd_hist = macd_line - signal_line
    
    return pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': macd_hist
    })

def calculate_rsi(prices, period=14):
    """
    计算RSI指标
    
    参数:
    prices: 价格序列
    period: RSI周期
    
    返回:
    RSI值序列
    """
    # 计算价格变化
    delta = prices.diff()
    
    # 分离上涨和下跌
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # 计算RS和RSI
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_bollinger_bands(prices, period=20, num_std=2):
    """
    计算布林带
    
    参数:
    prices: 价格序列
    period: 移动平均周期
    num_std: 标准差倍数
    
    返回:
    DataFrame包含上轨、中轨和下轨
    """
    # 计算中轨（简单移动平均）
    middle_band = prices.rolling(window=period).mean()
    
    # 计算标准差
    std = prices.rolling(window=period).std()
    
    # 计算上轨和下轨
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    return pd.DataFrame({
        'Upper': upper_band,
        'Middle': middle_band,
        'Lower': lower_band
    }) 