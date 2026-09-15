import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(
    page_title="PK Terminal - Dukascopy 10s/15s Sub-swing",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS ขยายเต็มหน้าจอ
st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        .stApp { background-color: #0B0E14; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;'>
        <h3 style='color:#F59E0B; margin:0; font-weight:800;'>⚡ DUKASCOPY SWISS ECN — SUB-SWING TERMINAL</h3>
        <span style='color:#22C55E; font-size:12px; font-weight:bold;'>🟢 Timeframes Enabled: 10s | 15s | 30s | 1m</span>
    </div>
""", unsafe_allow_html=True)

# 3. Direct Dukascopy HTML5 Engine Embed (เปิด Permission ครบถ้วน)
dukascopy_direct_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #0B0E14;
            overflow: hidden;
        }
        iframe {
            width: 100%;
            height: 100vh;
            border: none;
        }
    </style>
</head>
<body>
    <iframe src="https://www.dukascopy.com/swiss/english/fx-market-tools/charts/xau-usd/"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals"
            allow="autoplay; fullscreen">
    </iframe>
</body>
</html>
"""

# 4. เรนเดอร์บน Streamlit
components.html(dukascopy_direct_html, height=800, scrolling=False)
