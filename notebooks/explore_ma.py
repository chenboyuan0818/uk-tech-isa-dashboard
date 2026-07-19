import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import matplotlib.pyplot as plt
from src.fetch_data import load_prices

prices = load_prices()
stock = prices["NVDA"]

# rolling(50) = 一个宽度 50 行的"滑动窗口"，.mean() = 对每个窗口位置求平均
ma50 = stock.rolling(50).mean()
ma200 = stock.rolling(200).mean()

plt.figure(figsize = (12, 6))
plt.plot(stock.index, stock, label = "NVDA Close", linewidth = 1)
plt.plot(ma50.index, ma50, label = "MA50", linewidth = 2)
plt.plot(ma200.index, ma200, label = "MA200", linewidth = 2)
plt.legend()
plt.title("NVDA with Moving Averges")
plt.grid(alpha = 0.3)
plt.show()