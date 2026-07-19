"""投资组合分析指标计算模块。

设计原则：每个函数只做纯计算——数据进、结果出，
不读文件、不联网、不打印。取数是 fetch_data 的职责。
"""
def daily_returns(prices):
    """日收益率：每天相对前一交易日的百分比变化。"""
    return prices.pct_change().dropna()

def cumulative_returns(returns):
    """累计净值曲线：起点为 1，每行是从起点累计到该日的复利倍数。

        最终累计收益率 = 曲线最后一行 - 1。"""
    return (1 + returns).cumprod()

if __name__ == "__main__":
     # 冒烟测试：直接运行本文件时，快速自检各函数是否正常
     import sys
     from pathlib import Path

     sys.path.append(str(Path(__file__).parent.parent))
     from src.fetch_data import load_prices

     prices = load_prices()
     returns = daily_returns(prices)
     nav = cumulative_returns(returns)
     print("两年累计收益率排行（%）：")
     print(((nav.iloc[-1] - 1) * 100).round(1).sort_values(ascending = False))





