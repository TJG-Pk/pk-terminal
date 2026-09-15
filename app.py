import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from streamlit_lightweight_charts import renderLightweightCharts

# 1. Page Config (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(page_title="PK Terminal - Dukascopy & Webull", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #121620;
        border-radius: 6px;
        color: #A0AEC0;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E2638 !important;
        color: #F59E0B !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ PK INSTITUTIONAL TERMINAL")

# 2. แบ่งการใช้งานออกเป็น Tabs ป้องกันโค้ดตีกัน
tab_dukascopy, tab_tradingview = st.tabs(["🇨🇭 DUKASCOPY SWISS ECN", "📈 WEBULL / TRADINGVIEW"])

# =========================================================
# TAB 1: DUKASCOPY LIVE CHART (SWISS FEED)
# =========================================================
with tab_dukascopy:
    st.caption("🟢 Live Feed Direct from Dukascopy Bank Geneva (Raw Spreads / ECN)")
    
    col_sym, col_tf = st.columns([2, 2])
    with col_sym:
        duka_sym = st.selectbox("🪙 สินทรัพย์:", ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "USOIL"], key="duka_symbol")
    with col_tf:
        duka_tf = st.selectbox("⏱️ Timeframe ( นาที ):", ["1", "5", "15", "60"], key="duka_timeframe")

    sym_map = {"XAUUSD": 3, "EURUSD": 1, "GBPUSD": 2, "USDJPY": 6, "USOIL": 88}
    sym_id = sym_map.get(duka_sym, 3)

    # Widget HTML5 จาก Dukascopy
    dukascopy_iframe = f"""
    <div style="width:100%; height:620px; background-color:#0B0E14; border-radius:10px; overflow:hidden;">
        <iframe src="https://freeserv.dukascopy.com/widget/container/chart/{sym_id}?width=100%25&height=620&interval={duka_tf}&plot_type=candle&points=100&bars=1&price_type=bid&time_zone=7&show_tools=1&show_indicators=1&show_timeframes=1&show_symbols=1" 
                width="100%" height="620" frameborder="0" scrolling="no" style="border:none;">
        </iframe>
    </div>
    """
    components.html(dukascopy_iframe, height=630)

# =========================================================
# TAB 2: WEBULL / TRADINGVIEW TERMINAL
# =========================================================
with tab_tradingview:
    st.caption("🟢 Webull Data Stream / TradingView Lightweight Renderer")
    
    # ดึงราคาตัวอย่าง
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1m&range=1d"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3).json()
        quote = res['chart']['result'][0]['indicators']['quote'][0]
        timestamps = res['chart']['result'][0]['timestamp']
        
        df = pd.DataFrame({
            'time': timestamps,
            'open': quote['open'], 'high': quote['high'],
            'low': quote['low'], 'close': quote['close']
        }).dropna()
    except Exception:
        dates = pd.date_range(end=pd.Timestamp.now(), periods=50, freq='1min')
        df = pd.DataFrame({
            'time': [int(d.timestamp()) for d in dates],
            'open': np.random.normal(2650, 1, 50), 'high': np.random.normal(2652, 1, 50),
            'low': np.random.normal(2648, 1, 50), 'close': np.random.normal(2650.5, 1, 50)
        })

    candles = []
    for idx, row in df.tail(50).iterrows():
        candles.append({
            "time": int(row['time']), "open": float(row['open']),
            "high": float(row['high']), "low": float(row['low']), "close": float(row['close'])
        })

    chart_options = {
        "height": 500,
        "layout": { "backgroundColor": "#0B0E14", "textColor": "#A0AEC0" },
        "grid": { "vertLines": { "color": "#1E2638" }, "horzLines": { "color": "#1E2638" } },
        "timeScale": { "timeVisible": True, "secondsVisible": True }
    }

    renderLightweightCharts([{"chart": chart_options, "series": [{"type": "Candlestick", "data": candles}]}], key="tv_chart_main")
