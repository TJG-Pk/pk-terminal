import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าเลย์เอาต์พื้นฐานแบบเต็มความกว้าง (Wide Mode)
st.set_page_config(page_title="Dukascopy Chart Terminal", layout="wide")

# 2. ลบ Padding ขอบขาวภายนอกแบบปลอดภัย (ไม่กระทบโครงสร้าง React ของ Streamlit)
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

# 3. โครงสร้าง HTML สำหรับรัน Script ของ Dukascopy ที่คุณส่งมา
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
        /* บังคับให้ Element ที่ Script สร้างขึ้นขยายเต็มพื้นที่ 100% */
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

# 4. ดึงขึ้นแสดงผลบน Streamlit พร้อมตั้งความสูงเป็น 900px ให้ใหญ่เต็มจอ
components.html(dukascopy_script_html, height=900, scrolling=False)

import streamlit as st
import pandas as pd

# ... (บรรทัดที่ 1 ถึง 100 โค้ดเดิมของ PK ที่มีอยู่แล้ว) ...
st.title("โปรเจกต์เทรดของ PK")
st.write("ข้อมูลของหน้าเดิม")

# ========================================================
# เลื่อนมาบรรทัดล่างสุด แล้ววางโค้ดของจินจินต่อท้ายตรงนี้ได้เลยค่ะ!
# ========================================================
import streamlit.components.v1 as components

url = "https://script.google.com/macros/s/AKfycbyHn6gN2wZfvMPTYiYrcIOPbyZMpYtB4cPRUYPh0dqu0ZbS_dYLQNyUsc5jxXzItS1X/exec?v=view-lqwjrh81ZsvZ"
components.iframe(url, height=800, scrolling=True)
