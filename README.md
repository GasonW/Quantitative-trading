# 量化交易学习项目

这是一个用于学习量化交易基础知识的项目，包含数据获取、技术指标计算和策略回测等功能。

## 项目结构

- `data/`: 存放下载的股票数据
- `notebooks/`: Jupyter notebooks
  - `01_data_collection.ipynb`: 数据获取和预处理
  - `02_technical_indicators.ipynb`: 技术指标计算和可视化
  - `03_strategy_backtest.ipynb`: 策略回测
- `src/`: 源代码
  - `indicators.py`: 技术指标计算函数
  - `utils.py`: 工具函数

## 环境设置

1. 安装Anaconda
2. 创建新的conda环境：
   ```bash
   conda create -n quant python=3.9
   conda activate quant
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

1. 启动Jupyter Notebook：
   ```bash
   jupyter notebook
   ```
2. 按照notebooks目录下的顺序依次运行：
   - 首先运行数据获取notebook
   - 然后运行技术指标notebook
   - 最后运行策略回测notebook

## 学习内容

1. 量化交易三大假设
2. 数据获取和预处理
3. 技术指标计算（MACD、RSI、布林带）
4. 策略开发和回测 