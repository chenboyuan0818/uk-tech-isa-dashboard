import streamlit as st
from fetch_data import load_prices

import numpy as np
import analysis

import pandas as pd

import plotly.express as px

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

# ── 板块二:个股分析 ──
st.markdown("---")
st.header("② 个股分析")

pick = st.selectbox("选择一只股票", prices.columns)

stock = prices[pick]
ma_df = pd.DataFrame({
    "价格": stock,
    "MA20": analysis.moving_average(stock, 20),
    "MA50": analysis.moving_average(stock, 50),
    "MA200": analysis.moving_average(stock, 200),
})
st.subheader(f"{pick} 价格与移动平均线")
st.line_chart(ma_df)

st.subheader(f"{pick} 日收益分布")
fig = px.histogram(x = returns[pick] * 100, nbins = 50)
fig.update_layout(xaxis_title="日收益率 (%)", yaxis_title="天数", showlegend=False)
st.plotly_chart(fig, use_container_width = True)


# ── 板块三:风险分析 ──
st.markdown("---")
st.header("③ 风险分析")

st.subheader("相关性热力图")
st.caption("红 = 同涨同跌(分散差),蓝 = 走势独立或相反(分散好)")

corr = returns.corr()
fig = px.imshow(
    corr,
    text_auto = "2f",
    color_continuous_scale = "RdBu_r",
    zmin = -1, zmax = 1,
    aspect = "auto",
)
st.plotly_chart(fig, use_container_width = True)

st.subheader("组合回撤曲线(水下图)")
st.caption("0 = 创出新高;向下的深度 = 当前距历史峰值跌了多少")
dd = analysis.drawdown_series(port)
st.area_chart(dd)





















