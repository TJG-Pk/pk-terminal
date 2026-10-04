import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from massive import RESTClient

# 1. ตั้งค่าเลย์เอาต์พื้นฐานแบบเต็มความกว้าง (Wide Mode)
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# 2. ลบ Padding ขอบขาวภายนอกแบบปลอดภัย
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# ฟังก์ชันสำหรับดึงข้อมูลจาก Massive API (พร้อม Cache)
# ==========================================
API_KEY = "rbMxkAv3RG6XkHQxLMfAbMb5qeuyFiWH"

@st.cache_data(ttl=300)  # Caching ข้อมูลไว้ 5 นาทีเพื่อความเร็ว
def fetch_futures_contracts(api_key):
    try:
        client = RESTClient(api_key)
        # ดึงรายการ Futures Contracts 100 รายการ
        contracts = list(client.list_futures_contracts(limit="100", sort="product_code.asc"))
        
        # แปลง Object จาก Massive API เป็น List ของ Dictionary
        data = []
        for c in contracts:
            # ดึง Attributes ปลอดภัยด้วย getattr
            data.append({
                "Ticker": getattr(c, "ticker", getattr(c, "symbol", "N/A")),
                "Product Code": getattr(c, "product_code", "N/A"),
                "Name": getattr(c, "name", "N/A"),
                "Expiration Date": getattr(c, "expiration_date", getattr(c, "cme_expiration_date", "N/A")),
                "Active": getattr(c, "active", True),
            })
        return pd.DataFrame(data), None
    except Exception as e:
        return pd.DataFrame(), str(e)


# ==========================================
# ส่วนที่ 1: Massive Futures Contracts Explorer (ของใหม่)
# ==========================================
st.markdown("### 📋 Massive Futures Contracts Explorer")

df_contracts, error_msg = fetch_futures_contracts(API_KEY)

if error_msg:
    st.error(f"⚠️ เกิดข้อผิดพลาดในการดึงข้อมูลจาก Massive API: {error_msg}")
elif not df_contracts.empty:
    # ตัวกรองข้อมูล (Filter UI)
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.metric(label="Total Contracts Loaded", value=len(df_contracts))
        
    with col2:
        search_query = st.text_input("🔍 ค้นหาตาม Ticker หรือ Product Code:", placeholder="เช่น ES, NQ, GC, CL...")

    # กรองข้อมูลตามที่พิมพ์ค้นหา
    if search_query:
        df_filtered = df_contracts[
            df_contracts["Ticker"].astype(str).str.contains(search_query, case=False) |
            df_contracts["Product Code"].astype(str).str.contains(search_query, case=False) |
            df_contracts["Name"].astype(str).str.contains(search_query, case=False)
        ]
    else:
        df_filtered = df_contracts

    # แสดงผลตาราง Interactive DataFrame
    st.dataframe(
        df_filtered, 
        use_container_width=True, 
        height=300,
        hide_index=True
    )
else:
    st.info("ไม่พบข้อมูลสัญญา Futures")

st.markdown("---")


# ==========================================
# ส่วนที่ 2: Oi / Intraday Volume (Google Apps Script)
# ==========================================
st.markdown("### 📊 Oi / Intraday Volume")

url = "https://script.google.com/macros/s/AKfycbyHn6gN2wZfvMPTYiYrcIOPbyZMpYtB4cPRUYPh0dqu0ZbS_dYLQNyUsc5jxXzItS1X/exec?v=view-lqwjrh81ZsvZ"
components.iframe(url, height=700, scrolling=True)

st.markdown("---")


# ==========================================
# ส่วนที่ 3: Chart Monitor (Dukascopy)
# ==========================================
st.markdown("### 📈 Chart Monitor (EUR/USD)")

dukascopy_script_html = """
<!DOCTYPE html>
<html style="height: 100%; width: 100%;">
<head>
    <meta charset="utf-8">
    <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #ffffff;
        }
        body > div, iframe {
            width: 100% !important;
            height: 100% !important;
            border: none !important;
        }
    </style>
</head>
<body>
    <script src="https://widgets.dukascopy.com/embed/embed.js" async>
    {
      "type": "chart",
      "theme": "light",
      "lang": "en",
      "params": {
        "instrument": "EUR/USD",
        "interval": "1H",
        "series": "CANDLES",
        "offer": "BID"
      }
    }
    </script>
</body>
</html>
"""

components.html(dukascopy_script_html, height=800, scrolling=False)
