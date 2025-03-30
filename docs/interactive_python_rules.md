# 交互式Python文件规范

本文档定义了项目中交互式Python文件的编写规范，用于统一代码风格和提高可维护性。

## 1. 文件命名

- 使用小写字母
- 单词之间用下划线连接
- 使用有意义的描述性名称
- 以`.py`为扩展名
- 示例：`technical_indicators.py`, `strategy_backtest.py`

## 2. 文件结构

### 2.1 Markdown块
使用以下格式标记Markdown内容：
```python
#%% [markdown]
# 标题

# 描述性文本
# 1. 第一点
# 2. 第二点
# 3. 第三点
```

### 2.2 代码块
使用以下格式标记代码内容：
```python
#%% code
import pandas as pd
import numpy as np

# 你的代码
```

### 2.3 章节划分
使用以下格式标记章节：
```python
#%% [markdown]
## 1. 章节标题

#%% code
# 相关代码
```

## 3. 代码风格

### 3.1 导入语句
- 标准库导入放在最前面
- 第三方库导入放在中间
- 本地模块导入放在最后
- 按字母顺序排序

```python
#%% code
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.indicators import calculate_macd, calculate_rsi
```

### 3.2 中文支持
对于需要显示中文的文件，添加以下设置：
```python
#%% code
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # MacOS
plt.rcParams['axes.unicode_minus'] = False
```


## 4. 示例

```python
#%% [markdown]
# 数据分析示例

# 本文件将演示如何：
# 1. 加载数据
# 2. 处理数据
# 3. 可视化结果

#%% code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

#%% [markdown]
## 1. 数据加载

#%% code
# 加载数据
df = pd.read_csv('data.csv')
``` 