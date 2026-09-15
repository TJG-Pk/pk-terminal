import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import pandas as pd
import time
import random

# ตั้งค่าหน้าจอ Streamlit ให้เป็นแบบ Wide Mode (เต็มจอ)
st.set_page_config(page_title="PK Terminal - Second TF", layout="wide")

st.title("⚡ PK Trading Terminal (Secondary Timeframe)")

# แถบเลือก Timeframe และสินทรัพย์
col1, col2 = st.columns([1, 4])
with col1:
    tf_option = st.selectbox("เลือก Timeframe (Sub-swing):", ["10s", "15s", "1m"])
    symbol = st.text_input("สินทรัพย์:", value="XAUUSD")

# แปลงความยาววินาที
tf_seconds = 10 if tf_option == "10s" else (15 if tf_option == "15s" else 60)

# จำลองการคำนวณและสร้างแท่งเทียน Sub-swing
def generate_second_candles(seconds_interval, count=30):
    now = int(time.time())
    base_price = 2650.00
    candles = []
    
    for i in range(count):
        t = now - ((count - i) * seconds_interval)
        change = (random.random() - 0.49) * 1.2
        open_p = base_price
        close_p = open_p + change
        high_p = max(open_p, close_p) + random.random() * 0.5
        low_p = min(open_p, close_p) - random.random() * 0.5
        base_price = close_p
        
        candles.append({
            "time": t,
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2)
        })
    return candles

# ดึงข้อมูลแท่งเทียนตาม TF ที่เลือก
candles_data = generate_second_candles(tf_seconds)

# ตั้งค่ากราฟ TradingView Lightweight Charts
chart_options = {
    "height": 600,
    "layout": {
        "backgroundColor": "#111827",
        "textColor": "#D9D9D9"
    },
    "grid": {
        "vertLines": {"color": "#1F2937"},
        "horzLines": {"color": "#1F2937"}
    },
    "timeScale": {
        "timeVisible": True,
        "secondsVisible": True
    }
}

series_candlestick = [{
    "type": "Candlestick",
    "data": candles_data,
    "options": {
        "upColor": "#22c55e",
        "downColor": "#ef4444",
        "borderUpColor": "#22c55e",
        "borderDownColor": "#ef4444",
        "wickUpColor": "#22c55e",
        "wickDownColor": "#ef4444"
    }
}]

# แสดงผลกราฟบน Streamlit
renderLightweightCharts([
    {
        "chart": chart_options,
        "series": series_candlestick
    }
], key=f"chart_{tf_option}")
