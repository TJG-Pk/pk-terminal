import streamlit as st
import streamlit.components.v1 as components

def render_dukascopy_chart(symbol="XAUUSD", interval="1", height=550):
    """
    Dukascopy Official Live Chart Engine (Swiss ECN Feed)
    - symbol_id: 3 = XAU/USD (Gold), 1 = EUR/USD, 2 = GBP/USD, 6 = USD/JPY
    """
    symbol_map = {
        "XAUUSD": 3,
        "EURUSD": 1,
        "GBPUSD": 2,
        "USDJPY": 6,
        "USOIL": 88
    }
    sym_id = symbol_map.get(symbol.upper(), 3)
    
    # HTML5 Widget Spec สดจาก Dukascopy Swiss Gateway
    dukascopy_html = f"""
    <div style="width: 100%; height: {height}px; background-color: #0B0E14; border-radius: 8px; overflow: hidden;">
        <iframe src="https://freeserv.dukascopy.com/widget/container/chart/{sym_id}?width=100%25&height={height}&interval={interval}&plot_type=candle&points=100&bars=1&price_type=bid&time_zone=7&show_tools=1&show_indicators=1&show_timeframes=1&show_symbols=1" 
                width="100%" 
                height="{height}" 
                frameborder="0" 
                scrolling="no"
                style="border: none;">
        </iframe>
    </div>
    """
    components.html(dukascopy_html, height=height + 10)

# =========================================================
# การนำไปเรียกใช้ใน UI ของ Terminal
# =========================================================
st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <h3 style='color:#F8FAFC; margin:0;'>🇨🇭 DUKASCOPY SWISS ECN LIVE CHART</h3>
        <span style='color:#22C55E; font-size:12px; font-weight:bold;'>🟢 Direct ECN Liquidity Feed</span>
    </div>
""", unsafe_allow_html=True)

col_sym, col_tf = st.columns([2, 2])
with col_sym:
    duka_symbol = st.selectbox("🪙 เลือกสินทรัพย์ (Dukascopy Feed):", ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "USOIL"])
with col_tf:
    duka_tf = st.selectbox("⏱️ Timeframe (Dukascopy):", ["1", "5", "15", "60", "D"], format_func=lambda x: f"{x} Minute" if x.isdigit() else "1 Day")

# เรนเดอร์กราฟ Dukascopy
render_dukascopy_chart(symbol=duka_symbol, interval=duka_tf, height=580)
