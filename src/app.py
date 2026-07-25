import streamlit as st
from fetch_data import load_prices

import numpy as np
import analysis

import pandas as pd

import plotly.express as px

st.title("🇬🇧🇺🇸 UK & US Tech Stock ISA Portfolio Dashboard")
st.caption("⚠️ For educational purposes only — not investment advice")


# ── @st.cache_data: give the slow data load a "memory" ──
@st.cache_data
def get_prices():
    return load_prices()


with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🔄 Refresh to latest data"):
        load_prices(force_refresh=True)   # Layer 1: force re-download, overwrite the CSV
        st.cache_data.clear()             # Layer 2: clear Streamlit's cached result
        st.success("Data updated!")

prices = get_prices()
n = len(prices.columns)

with st.sidebar:
    st.subheader("🎚️ Holding weights (%)")
    raw = {}
    for t in prices.columns:
        raw[t] = st.slider(t, 0, 100, 100 // n)

# Normalise: whatever the user picks, scale proportionally so the weights sum to 1
total_w = sum(raw.values())
if total_w == 0:
    st.warning("Please assign a weight to at least one stock")
    st.stop()
weights = np.array([raw[t] / total_w for t in prices.columns])


st.subheader("📈 Relative performance (all rebased to 100 at the start)")
rebased = prices / prices.iloc[0] * 100
st.line_chart(rebased)

# ── Section 1: Portfolio Overview ──
st.markdown("---")
st.header("① Portfolio Overview")

returns = analysis.daily_returns(prices)
port = analysis.portfolio_returns(returns, weights)

# Reuse the analysis functions to compute the three headline metrics
total_returns = analysis.cumulative_returns(port).iloc[-1] - 1
vol = analysis.annualized_volatility(port)
mdd = analysis.max_drawdown(port)

# Three metric cards side by side
c1, c2, c3 = st.columns(3)
c1.metric("Total Return", f"{total_returns * 100:.1f}%")
c2.metric("Annualised Volatility", f"{vol * 100:.1f}%")
c3.metric("Max Drawdown", f"{mdd * 100:.1f}%")

# Portfolio cumulative net-asset-value curve
st.subheader("Portfolio cumulative NAV")
st.line_chart(analysis.cumulative_returns(port))

# ── Section 2: Single-Stock Analysis ──
st.markdown("---")
st.header("② Single-Stock Analysis")

pick = st.selectbox("Choose a stock", prices.columns)

stock = prices[pick]
ma_df = pd.DataFrame({
    "Price": stock,
    "MA20": analysis.moving_average(stock, 20),
    "MA50": analysis.moving_average(stock, 50),
    "MA200": analysis.moving_average(stock, 200),
})
st.subheader(f"{pick} — price and moving averages")
st.line_chart(ma_df)

st.subheader(f"{pick} — daily return distribution")
fig = px.histogram(x=returns[pick] * 100, nbins=50)
fig.update_layout(xaxis_title="Daily return (%)", yaxis_title="Number of days", showlegend=False)
st.plotly_chart(fig, use_container_width=True)


# ── Section 3: Risk Analysis ──
st.markdown("---")
st.header("③ Risk Analysis")

st.subheader("Correlation heatmap")
st.caption("Red = move together (weak diversification), Blue = independent or opposite (strong diversification)")

corr = returns.corr()
fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    aspect="auto",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Portfolio drawdown (underwater plot)")
st.caption("0 = new high; the depth below shows how far the portfolio is from its historical peak")
dd = analysis.drawdown_series(port)
st.area_chart(dd)

# ── Section 4: Raw Data ──
st.markdown("---")
st.header("④ Raw Data")
st.caption("All analysis is based on the closing prices below — download to verify for yourself")

st.dataframe(prices, use_container_width=True)
csv = prices.to_csv().encode("utf-8")
st.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name="close_prices.csv",
    mime="text/csv",
)
