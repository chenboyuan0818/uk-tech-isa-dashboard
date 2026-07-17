import yfinance as yf

TICKERS = ["MU", "NVDA", "AAPL", "TSM", "SGE.L", "OCDO.L", "AUTO.L"]

data = yf.download(TICKERS, period = "2y", auto_adjust = True)

print("形状", data.shape)
print("=" * 50)
# 只看收盘价这一层，这是分析中最常用的切法
close = data["Close"]
print("收盘价表的前五行：")
print(close.head())
print("=" * 50)
print("收盘价表的后五行：")
print(close.tail())
print("=" * 50 )
# isna() 检查每个格子是否为空，sum() 按列统计空格数量
print("每只股票缺失数值量")
print(close.isna().sum())

