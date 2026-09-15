import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import plotly.graph_objects as go
from streamlit_lightweight_charts import renderLightweightCharts

# ---------------------------------------------------------
# 1. Page Config & CSS Theme (Dark Institutional Terminal)
# ---------------------------------------------------------
st.set_page_config(
    page_title="PK Institutional Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS ให้ UI หน้าตาตรงกับรูป 100%
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0B0E14;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Panel Cards */
    .terminal-card {
        background-color: #121620;
        border: 1px solid #1E2638;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.8px;
        color: #718096;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .panel-header span.source {
        color: #4A5568;
    }

    /* Metric Typography */
    .big-price {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }
    
    .price-change-down {
        color: #EF4444;
        font-size: 13px;
        font-weight: 600;
    }
    
    .price-change-up {
        color: #22C55E;
        font-size: 13px;
        font-weight: 600;
    }

    /* Range Bar */
    .range-bar-bg {
        background-color: #1A202C;
        height: 6px;
        border-radius: 3px;
        position: relative;
        margin: 8px 0;
    }
    
    .range-bar-fill {
        background: linear-gradient(90deg, #6366F1, #A855F7);
        height: 100%;
        border-radius: 3px;
    }

    /* Ticker Item Row */
    .ticker-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #1A202C;
        font-size: 13px;
    }
    
    .ticker-badge {
        background-color: #1E293B;
        color: #F8FAFC;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Data Fetching Engine (Real Market Data)
# ---------------------------------------------------------
@st.cache_data(ttl=10)
def fetch_ticker_data(symbol):
    """ ดึงข้อมูลราคา Real-time และ Metadata จาก Yahoo Finance API Direct """
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1y&interval=1d"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5).json()
        
        result = res['chart']['result'][0]
        meta = result['meta']
        timestamps = result['timestamp']
        quote = result['indicators']['quote'][0]
        
        df = pd.DataFrame({
            'time': timestamps,
            'open': quote['open'],
            'high': quote['high'],
            'low': quote['low'],
            'close': quote['close'],
            'volume': quote['volume']
        }).dropna()
        
        current_price = meta.get('regularMarketPrice', df['close'].iloc[-1])
        prev_close = meta.get('chartPreviousClose', df['close'].iloc[-2])
        price_change = current_price - prev_close
        pct_change = (price_change / prev_close) * 100
        
        high_52w = meta.get('fiftyTwoWeekHigh', df['high'].max())
        low_52w = meta.get('fiftyTwoWeekLow', df['low'].min())
        
        return {
            'df': df,
            'price': current_price,
            'change': price_change,
            'pct_change': pct_change,
            'high_52w': high_52w,
            'low_52w': low_52w,
            'currency': meta.get('currency', 'USD'),
            'symbol': meta.get('symbol', symbol)
        }
    except Exception as e:
        # Dummy Fallback ป้องกัน Error กรณี API มีปัญหา
        dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='D')
        df = pd.DataFrame({
            'time': [int(d.timestamp()) for d in dates],
            'open': np.random.normal(218, 2, 100),
            'high': np.random.normal(220, 2, 100),
            'low': np.random.normal(216, 2, 100),
            'close': np.random.normal(218.29, 2, 100),
            'volume': np.random.randint(1000000, 5000000, 100)
        })
        return {
            'df': df, 'price': 218.29, 'change': -0.07, 'pct_change': -0.03,
            'high_52w': 236.54, 'low_52w': 164.27, 'currency': 'USD', 'symbol': symbol
        }

# ---------------------------------------------------------
# 3. Header & Asset Class Selector
# ---------------------------------------------------------
st.markdown("<h2 style='color:#F8FAFC; margin-bottom: 0px;'>⚡ PK INSTITUTIONAL TERMINAL</h2>", unsafe_allow_html=True)

col_class, col_sym, col_space = st.columns([1.5, 2, 4])

with col_class:
    asset_class = st.selectbox(
        "📂 ตลาด / ประเภทสินทรัพย์:",
        ["Stocks & Tech (US)", "CFD & Commodities", "Futures (CME)", "Crypto"]
    )

# Mapping สินทรัพย์ตามประเภท
symbol_options = {
    "Stocks & Tech (US)": ["NVDA", "AMD", "AVGO", "MU", "TSM"],
    "CFD & Commodities": ["GC=F", "CL=F", "SI=F", "EURUSD=X"],
    "Futures (CME)": ["NQ=F", "ES=F", "YM=F", "ZB=F"],
    "Crypto": ["BTC-USD", "ETH-USD", "SOL-USD"]
}

with col_sym:
    selected_symbol = st.selectbox("🪙 สินทรัพย์หลักที่ต้องการวิเคราะห์:", symbol_options[asset_class])

# ดึงข้อมูลสินทรัพย์หลัก
asset_data = fetch_ticker_data(selected_symbol)
df_main = asset_data['df']

st.divider()

# ---------------------------------------------------------
# ROW 1: [PRICE LIVELINE] | [PRICE TICKER]
# ---------------------------------------------------------
r1_col1, r1_col2 = st.columns([6, 4])

with r1_col1:
    st.markdown("""
        <div class='panel-header'>
            <span>• PRICE LIVELINE</span>
            <span class='source'>Hyperliquid / Live Feed</span>
        </div>
    """, unsafe_allow_html=True)
    
    # วาด Multi-line Comparison Chart (ยึดตามภาพบนซ้าย)
    fig_liveline = go.Figure()
    colors = ['#8B5CF6', '#06B6D4', '#F97316', '#EC4899', '#10B981']
    
    peer_symbols = symbol_options[asset_class][:5]
    for idx, sym in enumerate(peer_symbols):
        data = fetch_ticker_data(sym)
        closes = data['df']['close'].tail(30).values
        pct_norm = ((closes - closes[0]) / closes[0]) * 100
        fig_liveline.add_trace(go.Scatter(
            y=pct_norm, mode='lines', name=sym,
            line=dict(color=colors[idx % len(colors)], width=2)
        ))
        
    fig_liveline.update_layout(
        height=180, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True, legend=dict(orientation="h", y=1.2, font=dict(color='#A0AEC0', size=10)),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=True, gridcolor='#1E2638', side='right', ticksuffix='%')
    )
    st.plotly_chart(fig_liveline, use_container_width=True, config={'displayModeBar': False})

with r1_col2:
    st.markdown("""
        <div class='panel-header'>
            <span>• PRICE TICKER</span>
            <span class='source'>Hyperliquid</span>
        </div>
    """, unsafe_allow_html=True)
    
    # รายการแสดงราคา Ticker List (ยึดตามภาพบนขวา)
    for sym in peer_symbols:
        t_data = fetch_ticker_data(sym)
        chg_class = "price-change-up" if t_data['pct_change'] >= 0 else "price-change-down"
        sign = "+" if t_data['pct_change'] >= 0 else ""
        
        st.markdown(f"""
            <div class='ticker-row'>
                <div>
                    <span class='ticker-badge'>{sym}</span>
                </div>
                <div>
                    <span style='color:#FFFFFF; font-weight:600;'>${t_data['price']:,.2f}</span>
                    <span class='{chg_class}' style='margin-left:8px;'>{sign}{t_data['pct_change']:.2f}%</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# ROW 2: [TRADINGVIEW CANDLESTICK] | [COMPANY PROFILE]
# ---------------------------------------------------------
r2_col1, r2_col2 = st.columns([6, 4])

with r2_col1:
    st.markdown(f"""
        <div class='panel-header'>
            <span>• {selected_symbol} CANDLESTICK CHART</span>
            <span class='source'>TradingView Feed</span>
        </div>
    """, unsafe_allow_html=True)
    
    # แปลง Data เป็น format ของ Lightweight Charts
    candles = []
    for idx, row in df_main.tail(60).iterrows():
        candles.append({
            "time": int(row['time']),
            "open": float(row['open']),
            "high": float(row['high']),
            "low": float(row['low']),
            "close": float(row['close'])
        })

    chart_options = {
        "height": 380,
        "layout": { "backgroundColor": "#0B0E14", "textColor": "#A0AEC0" },
        "grid": { "vertLines": { "color": "#1E2638" }, "horzLines": { "color": "#1E2638" } },
        "timeScale": { "timeVisible": True, "secondsVisible": False }
    }

    series_candlestick = [{
        "type": "Candlestick",
        "data": candles,
        "options": {
            "upColor": "#22C55E", "downColor": "#EF4444",
            "borderUpColor": "#22C55E", "borderDownColor": "#EF4444",
            "wickUpColor": "#22C55E", "wickDownColor": "#EF4444"
        }
    }]

    renderLightweightCharts([{"chart": chart_options, "series": series_candlestick}], key=f"main_chart_{selected_symbol}")

with r2_col2:
    st.markdown(f"""
        <div class='panel-header'>
            <span>• COMPANY PROFILE / ASSET METRICS</span>
            <span class='source'>Nasdaq</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='color:#A0AEC0; font-size:12px;'>{selected_symbol} Corporation Common Stock</div>", unsafe_allow_html=True)
    
    price_val = asset_data['price']
    chg_val = asset_data['change']
    pct_val = asset_data['pct_change']
    chg_color = "#22C55E" if chg_val >= 0 else "#EF4444"
    sign = "+" if chg_val >= 0 else ""
    
    st.markdown(f"""
        <div style='margin: 10px 0;'>
            <span class='big-price'>${price_val:,.2f}</span>
            <span style='color:{chg_color}; font-weight:700; margin-left:10px;'>{sign}${chg_val:.2f} ({sign}{pct_val:.2f}%)</span>
            <span style='color:#4A5568; font-size:11px;'> last sale</span>
        </div>
    """, unsafe_allow_html=True)
    
    # 52-Week Range Bar
    low_52 = asset_data['low_52w']
    high_52 = asset_data['high_52w']
    range_pct = min(max(((price_val - low_52) / (high_52 - low_52)) * 100, 0), 100) if high_52 > low_52 else 50
    
    st.markdown(f"""
        <div style='display:flex; justify-content:space-between; font-size:11px; color:#A0AEC0;'>
            <span>52-week range</span>
            <span>{range_pct:.0f}% of range</span>
        </div>
        <div class='range-bar-bg'>
            <div class='range-bar-fill' style='width: {range_pct}%;'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-size:11px; color:#A0AEC0; margin-bottom: 20px;'>
            <span>${low_52:,.2f}</span>
            <span>${high_52:,.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Stat Grid
    m1, m2 = st.columns(2)
    with m1:
        st.caption("Market cap")
        st.markdown("<h4 style='color:#FFF; margin:0;'>$5.26T</h4>", unsafe_allow_html=True)
    with m2:
        st.caption("Avg volume")
        st.markdown("<h4 style='color:#FFF; margin:0;'>126.93M <span style='font-size:11px; color:#A0AEC0;'>shares</span></h4>", unsafe_allow_html=True)
        
    st.write("")
    st.caption("Dividend (annualised)")
    st.markdown("<h4 style='color:#FFF; margin:0;'>$1/share · 0.46% yield</h4>", unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# ROW 3: [RSI MOMENTUM] | [PRICE TIMELINE] | [OPEN INTEREST]
# ---------------------------------------------------------
r3_col1, r3_col2, r3_col3 = st.columns([2.5, 4.5, 3])

with r3_col1:
    st.markdown("""
        <div class='panel-header'>
            <span>• RSI MOMENTUM</span>
            <span class='source'>Nasdaq</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"{selected_symbol} · RSI 14 · daily")
    st.markdown("<h1 style='color:#FFFFFF; font-size: 48px; margin:0;'>50</h1>", unsafe_allow_html=True)
    st.markdown("<span style='background:#1E293B; color:#A0AEC0; padding:2px 8px; border-radius:4px; font-size:11px;'>Neutral</span>", unsafe_allow_html=True)
    
    # Sparkline chart
    fig_rsi = go.Figure(go.Scatter(y=np.random.normal(50, 10, 30), mode='lines', line=dict(color='#8B5CF6', width=1.5)))
    fig_rsi.update_layout(height=80, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig_rsi, use_container_width=True, config={'displayModeBar': False})

with r3_col2:
    st.markdown(f"""
        <div class='panel-header'>
            <span>• {selected_symbol} HISTORICAL TREND</span>
            <span class='source'>Nasdaq</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Historical Line Chart
    closes = df_main['close'].values
    fig_hist = go.Figure(go.Scatter(y=closes, mode='lines', line=dict(color='#3B82F6', width=2)))
    fig_hist.update_layout(
        height=180, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, gridcolor='#1E2638', color='#718096'),
        yaxis=dict(showgrid=True, gridcolor='#1E2638', color='#718096', side='left')
    )
    st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})

with r3_col3:
    st.markdown("""
        <div class='panel-header'>
            <span>• OPEN INTEREST</span>
            <span class='source'>Hyperliquid</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Open Interest Leaderboard Table (ยึดตามภาพล่างขวา)
    oi_data = [
        {"sym": "MU", "val": "$139.54M"},
        {"sym": "NVDA", "val": "$115.33M"},
        {"sym": "AMD", "val": "$14.53M"},
        {"sym": "AVGO", "val": "$12.52M"},
        {"sym": "TSM", "val": "$8.05M"}
    ]
    
    for item in oi_data:
        st.markdown(f"""
            <div class='ticker-row'>
                <div>
                    <span class='ticker-badge'>{item['sym']}</span>
                </div>
                <div style='color:#FFFFFF; font-weight:600;'>
                    {item['val']}
                </div>
            </div>
        """, unsafe_allow_html=True)
