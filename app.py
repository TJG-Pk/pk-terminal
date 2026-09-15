import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอแบบ Wide และซ่อน Sidebar
st.set_page_config(
    page_title="PK Terminal - Dukascopy Official Embed",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับ CSS ลบขอบ ลบ Header/Footer เพื่อให้แสดงผลเต็มหน้าจอ 100%
st.markdown("""
    <style>
        [data-testid="stMainBlockContainer"] {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        header, footer, #MainMenu { 
            visibility: hidden; 
            height: 0px; 
        }
        .stApp { 
            background-color: #0B0E14; 
        }
    </style>
""", unsafe_allow_html=True)

# 3. HTML Container รัน Script สดของ Dukascopy ตามรูปแบบที่กำหนด
dukascopy_embed_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            background-color: #0B0E14;
            overflow: hidden;
        }
    </style>
</head>
<body>
    <script>
    (() => {
      const script = document.createElement('script');
      script.src = 'https://widgets.dukascopy.com/embed/embed.js';
      script.async = true;
      script.type = 'text/javascript';
      script.innerHTML = JSON.stringify({
        "type": "chart",
        "theme": "dark",
        "lang": "en",
        "params": {
          "instrument": "XAU/USD",
          "interval": "1H",
          "series": "CANDLES",
          "offer": "BID"
        }
      });
      document.currentScript?.parentNode?.insertBefore(script, document.currentScript.nextSibling);
    })();
    </script>
</body>
</html>
"""

# 4. เรนเดอร์บน Streamlit ความสูง 920px เต็มจอ
components.html(dukascopy_embed_html, height=920, scrolling=False)
