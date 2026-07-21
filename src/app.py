import streamlit as st
from fetch_data import load_prices

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

st.subheader("📝原始价格数据")
st.dataframe(prices)

st.subheader("📈 相对表现(全部归一化到起点 = 100)")
rebased = prices / prices.iloc[0] * 100
st.line_chart(rebased)


