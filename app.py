import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอแบบ Wide
st.set_page_config(
    page_title="PK Terminal - Dukascopy Script Widget",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS ลบขอบขาว
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        .stApp { background-color: #0B0E14; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='color:#F59E0B; margin-bottom:10px;'>⚡ DUKASCOPY OFFICIAL EMBED WIDGET</h3>", unsafe_allow_html=True)

# 3. เมนูควบคุมพารามิเตอร์แบบ Dynamic
col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    selected_instrument = st.selectbox(
        "🪙 สินทรัพย์ (Instrument):",
        ["XAU/USD", "EUR/USD", "GBP/USD", "USD/JPY", "USA500.IDX"],
        index=0
    )
with col2:
    selected_interval = st.selectbox(
        "⏱️ Timeframe (Sub-swing & Main):",
        ["10S", "15S", "30S", "1M", "5M", "15M", "1H", "1D"],
        index=6
    )
with col3:
    selected_theme = st.selectbox(
        "🎨 Theme Display:",
        ["dark", "light"],
        index=0
    )

# 4. สคริปต์ Widget ของ Dukascopy Direct
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
            height: 720px;
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

# 5. แสดงผล Widget บน Streamlit
components.html(dukascopy_script_html, height=730, scrolling=False)
