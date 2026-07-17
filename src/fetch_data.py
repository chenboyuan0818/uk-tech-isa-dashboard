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
    return close

def save_prices(close):
    """把价格表存成 CSV，作为本地缓存。"""
    DATA_DIR.mkdir(exist_ok = True)      # 确保 data/ 文件夹存在
    path = DATA_DIR / "close_prices.csv"
    close.to_csv(path)
    print(f"已保存 {close.shape[0]} 行 × {close.shape[1]} 列 → {path}")

# 这个 if 的意思：只有"直接运行本文件"时才执行下面的代码；
# 以后 app.py 用 import 引用本模块时，不会触发下载
if __name__ == "__main__":
   prices = fetch_prices()
   save_prices(prices)
   print(prices.tail())