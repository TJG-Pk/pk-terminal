import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่า Wide Page
st.set_page_config(
    page_title="PK Terminal - Dukascopy Fullscreen",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ลบ Padding/Margin ของ Streamlit ออกทั้งหมดเพื่อขยายเต็มจอ 100%
st.markdown("""
    <style>
        /* ขยาย Main Container ให้เต็มขอบความกว้างและความสูง */
        [data-testid="stMainBlockContainer"] {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.2rem !important;
            padding-right: 0.2rem !important;
            max-width: 100% !important;
        }
        /* ซ่อน Header และ Footer ของ Streamlit */
        header { visibility: hidden; height: 0px; }
        footer { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        .stApp { background-color: #0B0E14; }
    </style>
""", unsafe_allow_html=True)

# 3. เมนูควบคุมแบบกะทัดรัด (เพื่อประหยัดพื้นที่แนวตั้ง)
col1, col2, col3, col_space = st.columns([2, 2, 2, 6])
with col1:
    selected_instrument = st.selectbox(
        "🪙 สินทรัพย์:",
        ["XAU/USD", "EUR/USD", "GBP/USD", "USD/JPY", "USA500.IDX"],
        index=0
    )
with col2:
    selected_interval = st.selectbox(
        "⏱️ Timeframe:",
        ["10S", "15S", "30S", "1M", "5M", "15M", "1H", "1D"],
        index=6
    )
with col3:
    selected_theme = st.selectbox(
        "🎨 Theme:",
        ["dark", "light"],
        index=0
    )

# 4. Dukascopy Widget HTML (กำหนดความสูง 100% ของ Viewport)
dukascopy_script_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: {"#0B0E14" if selected_theme == "dark" else "#FFFFFF"};
            overflow: hidden;
        }}
        .widget-wrapper {{
            width: 100%;
            height: 100vh;
        }}
    </style>
</head>
<body>
    <div class="widget-wrapper">
        <script src="https://widgets.dukascopy.com/embed/embed.js" async>
        {{
          "type": "chart",
          "theme": "{selected_theme}",
          "lang": "en",
          "params": {{
            "instrument": "{selected_instrument}",
            "interval": "{selected_interval}",
            "series": "CANDLES",
            "offer": "BID"
          }}
        }}
        </script>
    </div>
</body>
</html>
"""

# 5. แสดงผล Component ด้วยความสูง 850px ให้เต็มจอ
components.html(dukascopy_script_html, height=850, scrolling=False)
