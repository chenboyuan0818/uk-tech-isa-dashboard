import streamlit as st
from fetch_data import load_prices

import numpy as np
import analysis


st.title("🇬🇧英国科技股 ISA 组合分析仪表盘")
st.caption("⚠️ 仅供教育与学习用途，不构成任务投资建议")

# ── @st.cache_data:给慢操作装上"记忆" ──
@st.cache_data
def get_prices():
    return load_prices()

with st.sidebar:
    st.header("⚙️ 设置")
    if st.button("🔄 刷新为最新数据"):
        load_prices(force_refresh = True)     # 第1层:强制重新下载,覆盖 CSV
        st.cache_data.clear()                 # 第2层:清空 Streamlit 记忆
        st.success("数据已更新!")

prices = get_prices()
n = len(prices.columns)
with st.sidebar:
    st.subheader("🎚️ 持仓权重 (%)")
    raw = {}
    for t in prices.columns:
        raw[t] = st.slider(t, 0, 100, 100 // n)

# 归一化:不管用户拖成多少,都按比例缩放到"总和=1",保证是合法组合
total_w = sum(raw.values())
if total_w == 0:
    st.warning("请至少给一只股票分配权重")
    st.stop()
weights = np.array([raw[t] / total_w for t in prices.columns])

st.subheader("📝原始价格数据")
st.dataframe(prices)

st.subheader("📈 相对表现(全部归一化到起点 = 100)")
rebased = prices / prices.iloc[0] * 100
st.line_chart(rebased)

# ── 板块一:组合总览 ──
st.markdown("---")
st.header("① 组合总览")

# 先用等权组合(每只 1/7),之后再加"手动调权重"的滑块
n = len(prices.columns)


returns = analysis.daily_returns(prices)
port = analysis.portfolio_returns(returns, weights)

# 复用阶段三的函数算三个指标
total_returns = analysis.cumulative_returns(port).iloc[-1] - 1
vol = analysis.annualized_volatility(port)
mdd = analysis.max_drawdown(port)

# 三个并排的指标卡片
c1, c2, c3 = st.columns(3)
c1.metric("累计收益", f"{total_returns * 100:.1f}%")
c2.metric("年化波动率", f"{vol * 100:.1f}%")
c3.metric("最大回撤", f"{mdd * 100:.1f}%")

# 组合净值曲线
st.subheader("组合累计净值曲线(等权)")
st.line_chart(analysis.cumulative_returns(port))