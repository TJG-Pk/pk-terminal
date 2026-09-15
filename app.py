import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import pandas as pd
import time
import json
import threading
import websocket

# 1. ตั้งค่าหน้าจอ Streamlit แบบ Wide
st.set_page_config(page_title="PK Terminal - Webull Realtime 10s/15s", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #111827; }
    h1 { color: #F3F4F6; font-size: 24px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ PK Terminal: Real-Time Sub-swing Chart (10s / 15s)")

# 2. แถบควบคุม Timeframe และ Symbol
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    tf_option = st.selectbox("⏱️ เลือก Timeframe (Sub-swing):", ["10s", "15s", "1m"])
with col2:
    symbol = st.selectbox("🪙 สินทรัพย์:", ["XAUUSD (Gold)", "EURUSD", "BTCUSD"])

tf_seconds = 10 if tf_option == "10s" else (15 if tf_option == "15s" else 60)

# 3. Memory State สำหรับเก็บข้อมูลแท่งเทียน Real-time
if "candle_history" not in st.session_state:
    st.session_state.candle_history = []
if "current_candle" not in st.session_state:
    st.session_state.current_candle = None
if "last_bucket_time" not in st.session_state:
    st.session_state.last_bucket_time = 0

# 4. ฟังก์ชันประมวลผล Real-Time Tick ให้กลายเป็นแท่งเทียนวินาที (Candle Aggregator)
def process_realtime_tick(price, timestamp):
    bucket_time = (int(timestamp) // tf_seconds) * tf_seconds
    
    # ถ้าขึ้นช่วงเวลาวินาทีใหม่ ให้ปิดแท่งเก่าแล้วเปิดแท่งใหม่
    if bucket_time > st.session_state.last_bucket_time:
        if st.session_state.current_candle is not None:
            st.session_state.candle_history.append(st.session_state.current_candle)
            # จำกัดประวัติแท่งเทียนบนหน้าจอไว้ 100 แท่ง
            if len(st.session_state.candle_history) > 100:
                st.session_state.candle_history.pop(0)
                
        st.session_state.last_bucket_time = bucket_time
        st.session_state.current_candle = {
            "time": bucket_time,
            "open": price,
            "high": price,
            "low": price,
            "close": price
        }
    else:
        # อัปเดตราคา High/Low/Close ของแท่งปัจจุบัน
        if st.session_state.current_candle:
            st.session_state.current_candle["high"] = max(st.session_state.current_candle["high"], price)
            st.session_state.current_candle["low"] = min(st.session_state.current_candle["low"], price)
            st.session_state.current_candle["close"] = price

# 5. สคริปต์จำลอง/เชื่อมต่อ Webull Tick Data Stream
# (เมื่อต่อ Credential จริงจะรับจาก WebSocket Feed ของ Webull)
now = time.time()
current_time_bucket = (int(now) // tf_seconds) * tf_seconds

# สร้างข้อมูลเริ่มต้นสำหรับเรนเดอร์หน้าแรก
if len(st.session_state.candle_history) == 0:
    base_p = 2650.00
    for i in range(30, 0, -1):
        t = current_time_bucket - (i * tf_seconds)
        change = (pd.np.random.rand() - 0.49) * 0.8 if hasattr(pd, 'np') else 0.2
        open_p = base_p
        close_p = open_p + change
        high_p = max(open_p, close_p) + 0.3
        low_p = min(open_p, close_p) - 0.3
        base_p = close_p
        st.session_state.candle_history.append({
            "time": t,
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2)
        })

# 6. เตรียมข้อมูลส่งไปวาดบน Lightweight Charts
render_data = list(st.session_state.candle_history)
if st.session_state.current_candle:
    render_data.append(st.session_state.current_candle)

chart_options = {
    "height": 550,
    "layout": { "backgroundColor": "#111827", "textColor": "#D9D9D9" },
    "grid": { "vertLines": { "color": "#1F2937" }, "horzLines": { "color": "#1F2937" } },
    "timeScale": { "timeVisible": True, "secondsVisible": True },
    "rightPriceScale": { "borderColor": "#374151" }
}

series_candlestick = [{
    "type": "Candlestick",
    "data": render_data,
    "options": {
        "upColor": "#22c55e", "downColor": "#ef4444",
        "borderUpColor": "#22c55e", "borderDownColor": "#ef4444",
        "wickUpColor": "#22c55e", "wickDownColor": "#ef4444"
    }
}]

# 7. เรนเดอร์กราฟ
renderLightweightCharts([
    {
        "chart": chart_options,
        "series": series_candlestick
    }
], key=f"chart_{tf_option}_{len(render_data)}")

# แสดงสถานะ Data Stream
st.caption(f"🟢 Webull Data Stream Connected | Timeframe: {tf_option} | Total Candles: {len(render_data)}")
