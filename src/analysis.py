"""投资组合分析指标计算模块。

设计原则：每个函数只做纯计算——数据进、结果出，
不读文件、不联网、不打印。取数是 fetch_data 的职责。
"""
import numpy as np

# 一年约 252 个交易日（美股惯例），年化换算的标准常数
TRADING_DAYS = 252

def annualized_volatility(returns):
    """年化波动率：日收益率标准差 × √252。"""
    return returns.std() * np.sqrt(TRADING_DAYS)

def daily_returns(prices):
    """日收益率：每天相对前一交易日的百分比变化。"""
    return prices.pct_change().dropna()

def cumulative_returns(returns):
    """累计净值曲线：起点为 1，每行是从起点累计到该日的复利倍数。

        最终累计收益率 = 曲线最后一行 - 1。"""
    return (1 + returns).cumprod()

def moving_average(prices, window):
    """N 日移动平均线。开头不足 window 天的部分为 NaN。"""
    return prices.rolling(window).mean()

def drawdown_series(returns):
    """ 每日回撤序列：当日净值相对历史峰值的跌幅（0 = 正创新高）。"""
    nav = (1 + returns).cumprod()
    return nav / nav.cummax() - 1

def max_drawdown(returns):
    """最大回撤：历史上从峰值到谷底的最大跌幅（负数）"""
    return drawdown_series(returns).min()

def portfolio_returns(returns, weights):
    """按权重合成组合的日收益率序列。

    weights 顺序须与 returns 的列一一对应，总和应为 1。
    """
    return returns.dot(weights)


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent))
    from src.fetch_data import load_prices

    prices = load_prices()
    returns = daily_returns(prices)
    weights = np.ones(len(returns.columns)) / len(returns.columns)
    port = portfolio_returns(returns, weights)

    print("等权组合三大指标：")
    print(f"累计收益: {(cumulative_returns(port).iloc[-1] - 1) * 100:.1f}%")
    print(f"年化波动率: {annualized_volatility(port) * 100:.1f}%")
    print(f"最大回撤: {max_drawdown(port) * 100:.1f}%")







