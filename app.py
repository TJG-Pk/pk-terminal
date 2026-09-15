import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอแบบ Wide และซ่อน Sidebar
st.set_page_config(
    page_title="PK Terminal - Dukascopy XAU/USD Direct Chart",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS ลบขอบขาว (Padding) และลบ Header ของ Streamlit ออกให้ขยายเต็มหน้าจอ 100%
st.markdown("""
    <style>
        /* ลบ Padding ส่วนเกินรอบหน้าจอ */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        /* ซ่อน Header / Footer ของ Streamlit */
        header { visibility: hidden; }
        footer { visibility: hidden; }
        .stApp { background-color: #0B0E14; }
    </style>
""", unsafe_allow_html=True)

# 3. ส่วนแสดงผลหัวข้อ Terminal
st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;'>
        <h3 style='color:#F59E0B; margin:0; font-weight:800;'>⚡ DUKASCOPY SWISS ECN — XAU/USD LIVE CHART</h3>
        <span style='color:#22C55E; font-size:12px; font-weight:bold;'>🟢 Swiss Direct Feed Connected (ID: 3)</span>
    </div>
""", unsafe_allow_html=True)

# 4. Dukascopy Standalone Chart Engine Spec (ID: 3 = XAU/USD)
dukascopy_xauusd_html = """
<div style="width: 100%; height: 820px; background-color: #0B0E14; border-radius: 8px; overflow: hidden;">
    <iframe src="https://freeserv.dukascopy.com/widget/container/chart/3?width=100%25&height=820&interval=1&plot_type=candle&points=100&bars=1&price_type=bid&time_zone=7&show_tools=1&show_indicators=1&show_timeframes=1&show_symbols=1" 
            width="100%" 
            height="820" 
            frameborder="0" 
            scrolling="no"
            style="border: none; width: 100%; height: 820px;">
    </iframe>
</div>
"""

# 5. เรนเดอร์บน Streamlit
components.html(dukascopy_xauusd_html, height=830, scrolling=False)
