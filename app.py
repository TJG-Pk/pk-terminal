import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าเลย์เอาต์พื้นฐานแบบ Wide
st.set_page_config(
    page_title="PK Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS แบบปลอดภัย (ไม่กระทบโครงสร้างหลักของ Streamlit Cloud)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. HTML Embed ตัวกราฟ Dukascopy
dukascopy_html = """
<div style="width: 100%; height: 85vh; background-color: #0B0E14;">
    <iframe src="https://freeserv.dukascopy.com/widget/container/chart/3?width=100%25&height=100%25&interval=1&plot_type=candle&points=100&bars=1&price_type=bid&time_zone=7&show_tools=1&show_indicators=1&show_timeframes=1&show_symbols=1" 
            width="100%" 
            height="100%" 
            frameborder="0" 
            scrolling="no"
            style="border: none;">
    </iframe>
</div>
"""

# 4. แสดงผล Component
components.html(dukascopy_html, height=800, scrolling=False)
