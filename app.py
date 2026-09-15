import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PK Terminal - Dukascopy Swiss ECN", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .popout-card {
        background-color: #121620;
        border: 1px solid #1E2638;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-top: 20px;
    }
    .btn-dukascopy {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #000000 !important;
        font-weight: 800;
        font-size: 16px;
        padding: 12px 28px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ DUKASCOPY SWISS ECN — LIVE TERMINAL")

# การ์ดควบคุมเปิดหน้าต่าง Pop-out
st.markdown("""
    <div class="popout-card">
        <h2 style="color:#F59E0B; margin-top:0;">🇨🇭 DUKASCOPY DIRECT SWISS ECN FEED</h2>
        <p style="color:#A0AEC0;">เนื่องจากระบบความปลอดภัยของ Dukascopy บล็อกการฝังหน้าเว็บข้ามโดเมน (X-Frame-Options)</p>
        <p style="color:#F8FAFC;">กดปุ่มด้านล่างเพื่อเปิดหน้าต่างกราฟ <b>XAU/USD Sub-swing (10s / 15s / 30s)</b> สดตรงจากโบรกเกอร์สวิสแบบเต็มจอ 100%</p>
        <a href="https://www.dukascopy.com/swiss/english/fx-market-tools/charts/xau-usd/" target="_blank" class="btn-dukascopy">
            🚀 Launch Dukascopy 10s/15s Chart Window
        </a>
    </div>
""", unsafe_allow_html=True)
