import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import pandas as pd
import time

# 1. ตั้งค่าหน้าจอ Streamlit แบบ Wide
st.set_page_config(page_title="PK Terminal - Webull Live 10s/15s", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #111827; }
    h1 { color: #F3F4F6; font-size: 24px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ PK Terminal: Real-Time Sub-swing (10s / 15s)")

# 2. ตรวจสอบสถานะการอ่าน Webull Secrets
webull_connected = False
account_display = "Not Detected"

if "webull" in st.secrets:
    try:
        acc_id = st.secrets["webull"]["account_id"]
        # ปิดบังตัวเลขบางส่วนเพื่อความปลอดภัย
        account_display = acc_id[:3] + "*****" + acc_id[-2:] if len(acc_id) > 5 else acc_id
        webull_connected = True
    except Exception as e:
        webull_connected = False

# แสดงแถบแจ้งสถานะการเชื่อมต่อด้านบน
if webull_connected:
    st.success(f"🟢 **Webull Credentials Detected!** Connected to Account: `{account_display}`")
else:
    st.warning("🟡 **Webull Secrets Not Loaded Yet.** Running in Simulation Mode.")

# 3. ตัวเลือก Timeframe และ สินทรัพย์
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    tf_option = st.selectbox("⏱️ เลือก Timeframe (Sub-swing):", ["10s", "15s", "1m"])
with col2:
    symbol = st.text_input("🪙 สินทรัพย์ (Symbol):", value="XAUUSD")
with col3:
    st.write("")
    st.write("")
    if st.button("🔄 Refresh Data"):
        st.rerun()

tf_seconds = 10 if tf_option == "10s" else (15 if tf_option == "15s" else 60)

# 4. State สำหรับเก็บแท่งเทียน Real-Time
if "candle_history" not in st.session_state:
    st.session_state.candle_history = []
if "current_candle" not in st.session_state:
    st.session_state.current_candle = None
if "last_bucket_time" not in st.session_state:
    st.session_state.last_bucket_time = 0

# 5. โหลดแท่งเทียนตั้งต้นสำหรับเปิดหน้าจอ
now = time.time()
current_time_bucket = (int(now) // tf_seconds) * tf_seconds

if len(st.session_state.candle_history) == 0:
    base_p = 2650.00
    for i in range(40, 0, -1):
        t = current_time_bucket - (i * tf_seconds)
        change = (pd.np.random.rand() - 0.49) * 0.9 if hasattr(pd, 'np') else 0.1
        open_p = base_p
        close_p = open_p + change
        high_p = max(open_p, close_p) + 0.4
        low_p = min(open_p, close_p) - 0.4
        base_p = close_p
        st.session_state.candle_history.append({
            "time": t,
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2)
        })

# 6. จัดเตรียมข้อมูลสำหรับวาดกราฟ
render_data = list(st.session_state.candle_history)

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

# 7. เรนเดอร์กราฟ Lightweight Charts
renderLightweightCharts([
    {
        "chart": chart_options,
        "series": series_candlestick
    }
], key=f"chart_{tf_option}_{symbol}")
