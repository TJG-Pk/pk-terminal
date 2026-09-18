import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าเลย์เอาต์พื้นฐานแบบเต็มความกว้าง (Wide Mode)
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# 2. ลบ Padding ขอบขาวภายนอกแบบปลอดภัย (ดึงให้กราฟชิดขอบจอ)
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

# 3. สร้างแถบเมนูด้านบน 2 แท็บ
tab1, tab2 = st.tabs(["Chart monitor", "Oi / Intraday volume"])

# ==========================================
# เมนูที่ 1: Chart monitor (โปรเจคเดิม Dukascopy)
# ==========================================
with tab1:
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
    
    # ดึงขึ้นแสดงผลบน Streamlit พร้อมตั้งความสูงเป็น 900px
    components.html(dukascopy_script_html, height=900, scrolling=False)


# ==========================================
# เมนูที่ 2: Oi / Intraday volume (โปรเจคใหม่)
# ==========================================
with tab2:
    # เพิ่มช่องว่างนิดหน่อยให้ดูสบายตา ไม่ชิดขอบบนเกินไป
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ลิงก์ Web App Google Apps Script
    url = "https://script.google.com/macros/s/AKfycbyHn6gN2wZfvMPTYiYrcIOPbyZMpYtB4cPRUYPh0dqu0ZbS_dYLQNyUsc5jxXzItS1X/exec?v=view-lqwjrh81ZsvZ"
    
    # ดึงขึ้นแสดงผลด้วย iframe
    components.iframe(url, height=800, scrolling=True)
