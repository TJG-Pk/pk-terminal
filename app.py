import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าเลย์เอาต์พื้นฐานแบบ Wide
st.set_page_config(
    page_title="PK Terminal - Dukascopy Full View",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS บังคับทำลายขอบ Padding และซ่อน UI เดิมของ Streamlit ทุกจุด
st.markdown("""
    <style>
        /* ซ่อน Header, Footer และ Menu Bar ของ Streamlit */
        header[data-testid="stHeader"], footer, #MainMenu {
            display: none !important;
            height: 0px !important;
        }

        /* ลบ Padding/Margin ของแอป Streamlit ทุกชั้นให้กว้าง-สูง 100% เต็มจอ */
        html, body, 
        [data-testid="stAppViewContainer"], 
        [data-testid="stMain"], 
        .main, 
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100% !important;
            overflow: hidden !important;
            background-color: #0B0E14 !important;
        }

        /* บังคับ Component Iframe ให้ขยายเต็มความสูงและกว้างของจอภาพ */
        [data-testid="stCustomComponentV1"], iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Embed Dukascopy Engine ปรับสัดส่วนเป็น 100% Viewport
dukascopy_html = """
<div style="width: 100vw; height: 100vh; background-color: #0B0E14; margin: 0; padding: 0; overflow: hidden;">
    <iframe src="https://freeserv.dukascopy.com/widget/container/chart/3?width=100%25&height=100%25&interval=1&plot_type=candle&points=100&bars=1&price_type=bid&time_zone=7&show_tools=1&show_indicators=1&show_timeframes=1&show_symbols=1" 
            width="100%" 
            height="100%" 
            frameborder="0" 
            scrolling="no"
            style="border: none; width: 100vw; height: 100vh; display: block;">
    </iframe>
</div>
"""

# 4. ส่งออกหน้าจอ
components.html(dukascopy_html, height=2000, scrolling=False)
