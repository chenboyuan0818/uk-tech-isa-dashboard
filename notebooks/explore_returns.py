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

print("=" * 50)
nav = (1 + returns).cumprod() # 净值曲线（之前算过，这里重算一遍保持独立）
peak = nav.cummax()           # 每天回望：历史最高纪录是多少
drawdown = nav / peak - 1     # 每天：距离巅峰跌了多少（0 = 正创新高）
max_dd = drawdown.min()       # 最深的那个坑

print("最大回撤排行（%，越接近0越好）：")
print((max_dd * 100).round(1).sort_values(ascending = False))

print("=" * 50)
# corr() 计算所有列两两之间的相关系数，输出 7×7 矩阵
print("相关性矩阵")
print(returns.corr().round(2))

print("=" * 50)
corr = returns.corr()
# 第 1 步：做一个"上三角"面具——只保留矩阵对角线以上的部分
# np.ones(...) 生成全 True 的 7×7；np.triu(..., k=1) 只留上三角（k=1 表示不含对角线）
mask = np.triu(np.ones(corr.shape, dtype = bool), k = 1)

# 第 2 步：where(mask) = 面具外的格子全部变 NaN；stack() = 把表格"拍扁"成一列，NaN 自动丢弃
pairs = corr.where(mask).stack().dropna()

# 第 3 步：排序，得到排行榜
ranked = pairs.sort_values(ascending=False)

print("相关性最高的5对：")
print(ranked.head(5).round(2))
print("相关性最低的5对：")
print(ranked.tail(5).round(2))

print("=" * 50)
# 等权组合：7 只股票各占 1/7（先用最简单的权重方案验证逻辑）
weights = np.ones(len(returns.columns)) / len(returns.columns)

# dot = 点积：每行做"权重 × 收益率"再求和，一次算完整个序列
port_returns = returns.dot(weights)

port_nav = (1 + port_returns).cumprod()
port_vol = port_returns.std() * np.sqrt(252)
port_dd = (port_nav / port_nav.cummax() - 1).min()

print(f"等权组合 累计收益：{(port_nav.iloc[-1] - 1) * 100:.1f}%")
print(f"等权组合  年化波动率: {port_vol * 100:.1f}%")
print(f"等权组合  最大回撤: {port_dd * 100:.1f}%")
print(f"（对比）7 只股票波动率的简单平均: {(returns.std() * np.sqrt(252)).mean() * 100:.1f}%")

