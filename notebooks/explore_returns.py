import sys
from pathlib import Path

# 让 Python 能找到 src/ 里的模块（把项目根目录加进模块搜索路径）
sys.path.append(str(Path(__file__).parent.parent))

from src.fetch_data import load_prices

prices = load_prices()  # 不传参数 → 用缓存，秒开

# pct_change = percent change，pandas 一行算出全表的日收益率
returns = prices.pct_change().dropna()

print("最后5天的日收益率：")
print((returns.tail() * 100).round(2))
print("=" * 50)
print("两年里单日最大涨幅：")
print((returns.max() * 100).round(2))
print("两年里单日最大跌幅：")
print((returns.min() * 100).round(2))

print("=" * 50)
# cumprod = cumulative product（累乘）：每一行 = 从起点到该日的复利倍数
cumulative = (1 + returns).cumprod()

print("每只股票的两年累计收益率 %：")
final = (cumulative.iloc[-1] - 1) * 100   # iloc[-1] = 按位置取最后一行
print(final.round(1).sort_values(ascending = False))

print("=" * 50)
import numpy as np

# std() = 标准差（standard deviation），× √252 换算成年尺度
volatility = returns.std() * np.sqrt(252)

print("年化波动率排行（%）：")
print((volatility * 100).round(1).sort_values(ascending=False))