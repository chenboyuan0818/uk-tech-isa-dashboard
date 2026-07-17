import yfinance as yf
# ── 实验 1：拉一只美股，看看数据结构 ──
# period="2y" 表示最近两年
# auto_adjust=True 表示自动把分红、拆股折算进价格（我们要的就是这种"可比"价格）
apple = yf.download("AAPL", period = "2y", auto_adjust = True)
print("=" * 50)
print("AAPl 数据的形状（行数，列数 ：", apple.shape)
print("=" * 50)
print("前五行")
print(apple.head())
print("最后5行")
print(apple.tail())

# ── 实验 2：拉一只伦敦股，对比看有什么不同 ──
sage = yf.download("SGE.L", period = "2y", auto_adjust = True)
print("=" * 50)
print("SGE.L 最后5行")
print(sage.tail())