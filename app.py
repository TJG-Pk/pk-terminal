import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอแบบ Wide
st.set_page_config(
    page_title="PK Terminal - Dukascopy Swiss ECN",
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

# 3. ส่วนเลือกสินทรัพย์
col_title, col_sym = st.columns([2, 1])
with col_title:
    st.markdown("<h3 style='color:#F59E0B; margin:0; font-weight:800;'>⚡ DUKASCOPY SWISS ECN LIVE TERMINAL</h3>", unsafe_allow_html=True)
with col_sym:
    selected_asset = st.selectbox(
        "🪙 เลือก Feed สินทรัพย์ (Dukascopy Direct):",
        ["DUKASCOPY:XAUUSD", "DUKASCOPY:EURUSD", "DUKASCOPY:GBPUSD", "DUKASCOPY:USDJPY"],
        index=0
    )

# 4. HTML5 Widget Container (TradingView Engine Direct to Dukascopy ECN Feed)
tv_dukascopy_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #0B0E14;
            overflow: hidden;
        }}
        .tradingview-widget-container {{
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <div class="tradingview-widget-container">
        <div id="tradingview_chart" style="width: 100%; height: 100%;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            new TradingView.widget({{
                "width": "100%",
                "height": "750",
                "symbol": "{selected_asset}",
                "interval": "1",
                "timezone": "Asia/Bangkok",
                "theme": "dark",
                "style": "1",
                "locale": "th_TH",
                "toolbar_bg": "#0B0E14",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "container_id": "tradingview_chart"
            }});
        </script>
    </div>
</body>
</html>
"""

# 5. แสดงผลบน Streamlit
components.html(tv_dukascopy_html, height=760, scrolling=False)
