"""从 Yahoo Finance 下载股票数据并保存到本地 CSV。"""

from pathlib import Path

import pandas as pd
import yfinance as yf
# ── 配置区：全大写 = 常量 ──
TICKERS = ["MU", "NVDA", "AAPL", "TSM", "SGE.L", "OCDO.L", "AUTO.L"]
PERIOD = "2y"
# Path(__file__) 是"本文件的路径"，.parent 是上一级文件夹
# 所以这句的意思：不管从哪里运行脚本，都能准确定位到项目根目录下的 data/ 文件夹
DATA_DIR = Path(__file__).parent.parent / "data"

def fetch_prices():
    """下载全部股票的收盘价，返回清洗后的 DataFrame。"""
    raw = yf.download(TICKERS, period = PERIOD, auto_adjust = True, progress = False)
    close = raw["Close"]
    # 前向填充：休市日沿用前一个交易日的价格（经济含义：持仓价值 = 最后已知价格）
    close = close.ffill()
    # 开头几行可能因为"该股票还没上市/数据还没开始"而是 NaN，ffill 补不了，直接丢弃
    close = close.dropna()
    # 验货：yfinance 断网时不报错，而是安静返回空表——必须自己检查，主动把它变成异常
    if close.empty:
        raise RuntimeError("下载结果为空：可能是断网或者Yahoo 接口故障")
    return close

def save_prices(close):
    """把价格表存成 CSV，作为本地缓存。"""
    DATA_DIR.mkdir(exist_ok = True)      # 确保 data/ 文件夹存在
    path = DATA_DIR / "close_prices.csv"
    close.to_csv(path)
    print(f"已保存 {close.shape[0]} 行 × {close.shape[1]} 列 → {path}")



def load_prices(force_refresh = False):
    """获取价格数据的统一入口：优先读本地缓存，必要时才联网下载。
    force_refresh=True 时强制重新下载。
        """
    cache = DATA_DIR / "close_prices.csv"
    # 情况一：有缓存且不要求刷新 → 直接读本地文件，零网络请求
    if cache.exists() and not force_refresh:
        print("使用本地缓存")
        return pd.read_csv(cache, index_col = "Date", parse_dates = True)
        # 情况二：需要下载 → 用 try/except 兜住可能的网络失败
    try:
        prices = fetch_prices()
    except Exception as error:
        print(f"下载失败：{error}")
        if cache.exists():
                print("退而求其次，使用本地缓存")
                return pd.read_csv(cache, index_col = "Date", parse_dates = True)
        raise #连缓存都没有，只能把错误原样抛出，让程序停下
    save_prices(prices)
    return prices

if __name__ == "__main__":
    prices = load_prices(force_refresh=True)  # 直接运行本文件 = 主动刷新数据
    print(prices.tail())