import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าเลย์เอาต์พื้นฐานแบบเต็มความกว้าง (Wide Mode)
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# 2. ลบ Padding ขอบขาวภายนอกแบบปลอดภัย (ดึงให้ชิดขอบจอ)
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# ส่วนที่ 1: Oi / Intraday Volume (ด้านบน)
# ==========================================
url = "https://script.google.com/macros/s/AKfycbyHn6gN2wZfvMPTYiYrcIOPbyZMpYtB4cPRUYPh0dqu0ZbS_dYLQNyUsc5jxXzItS1X/exec?v=view-lqwjrh81ZsvZ"

components.iframe(url, height=800, scrolling=True)


# ==========================================
# ส่วนที่ 2: Chart Monitor (ด้านล่าง - XAU/USD 15m Dark Mode)
# ==========================================
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
            background-color: #131722; /* ปรับพื้นหลังเป็นสีมืดให้เนียนไปกับ Dark Theme */
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
      "theme": "dark",
      "lang": "en",
      "params": {
        "instrument": "XAU/USD",
        "interval": "15m",
        "series": "CANDLES",
        "offer": "BID",
        "type": "minimal"
      }
    }
    </script>
</body>
</html>
"""

components.html(dukascopy_script_html, height=900, scrolling=False)
