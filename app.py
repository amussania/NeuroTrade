import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import csv
import os
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroTrade · AI Crypto Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Persistent session state (must be before any rendering) ───────────────────
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = 'bitcoin'

# ── Dark theme CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.main > div {
    zoom: 0.90;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0B1120 !important;
    color: #CBD5E1;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"]    { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stHeader"]     { background: transparent; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0B1120; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }

/* ── SECTION HEADERS ── */
.section-header {
    color: #94A3B8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 40px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid #1E293B;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 16px;
    background: linear-gradient(180deg, #00d4ff, #7c3aed);
    border-radius: 2px;
}

/* ── PRICE CARDS ── */
.price-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 20px 20px 0 0;
    padding: 28px 28px 22px 28px;
    margin-bottom: 0;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    overflow: hidden;
}
.price-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, #334155);
    border-radius: 20px 20px 0 0;
}
.price-card:hover {
    border-color: #475569;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}

.coin-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.coin-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}
.coin-price {
    font-size: 64px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1.5px;
    line-height: 1.05;
    margin: 6px 0 10px 0;
}
.change-pos {
    color: #10b981;
    font-size: 18px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(16,185,129,0.1);
    padding: 3px 10px;
    border-radius: 20px;
}
.change-neg {
    color: #ef4444;
    font-size: 18px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(239,68,68,0.1);
    padding: 3px 10px;
    border-radius: 20px;
}
.sub-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 18px;
    padding-top: 18px;
    border-top: 1px solid #334155;
}
.sub-item-label {
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.sub-item-value {
    color: #94A3B8;
    font-size: 16px;
    font-weight: 600;
}

/* ── ON-CHAIN TILES ── */
.oc-tile {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 24px 24px 20px 24px;
    transition: border-color 0.2s ease;
}
.oc-tile:hover { border-color: #475569; }
.oc-label {
    font-size: 11px;
    font-weight: 700;
    color: #64748B;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.oc-value {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    line-height: 1.1;
}
.oc-unit {
    font-size: 14px;
    color: #64748B;
    font-weight: 500;
    margin-left: 4px;
}

/* ── F&G ── */
.fng-label-big {
    text-align: center;
    font-size: 26px;
    font-weight: 800;
    margin-top: -8px;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}
.fng-sub {
    text-align: center;
    color: #475569;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.subsection-label {
    color: #64748B;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 24px 0 10px 0;
}

/* ── LIVE DOT ── */
@keyframes pulse { 0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(16,185,129,0.4); }
                   50%      { opacity:0.7; box-shadow:0 0 0 6px rgba(16,185,129,0); } }
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #10b981;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2.5s infinite;
}

/* ── CHART CONTAINER ── */
.chart-wrap {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 4px;
    overflow: hidden;
}

/* ── INTELLIGENCE SCORE ── */
.intel-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 24px;
    padding: 24px 32px 20px 32px;
    margin: 8px 0 4px 0;
    position: relative;
    overflow: hidden;
}
.intel-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(0,212,255,0.03) 0%, rgba(124,58,237,0.03) 100%);
    pointer-events: none;
}
.intel-score-number {
    font-size: 80px;
    font-weight: 800;
    letter-spacing: -3px;
    line-height: 1;
}
.intel-label {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-top: 6px;
}
.intel-explanation {
    color: #94A3B8;
    font-size: 15px;
    font-weight: 400;
    margin-top: 8px;
    line-height: 1.5;
}
.intel-bar-track {
    background: #0B1120;
    border-radius: 999px;
    height: 16px;
    margin: 20px 0 8px 0;
    overflow: hidden;
    border: 1px solid #334155;
}
.intel-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s ease;
}
.intel-component {
    display: flex;
    flex-direction: column;
    gap: 5px;
}
.intel-comp-label {
    color: #64748B;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.intel-comp-bar-track {
    background: #0B1120;
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
}
.intel-comp-bar-fill {
    height: 100%;
    border-radius: 999px;
    opacity: 0.7;
}
.intel-comp-value {
    color: #CBD5E1;
    font-size: 13px;
    font-weight: 600;
    margin-top: 1px;
}

/* ── WAITLIST ── */
.waitlist-card {
    background: linear-gradient(135deg, #0F1E38 0%, #1A1035 100%);
    border: 1px solid #334155;
    border-radius: 24px;
    padding: 52px 56px;
    position: relative;
    overflow: hidden;
}
.waitlist-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00D4FF 0%, #7C3AED 50%, #F7931A 100%);
    border-radius: 24px 24px 0 0;
}
.waitlist-headline {
    font-size: 36px;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 16px;
}
.waitlist-sub {
    font-size: 16px;
    color: #94A3B8;
    line-height: 1.7;
    margin-bottom: 32px;
    max-width: 520px;
}
.waitlist-value-point {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 14px;
    font-size: 15px;
    color: #CBD5E1;
    font-weight: 500;
}
.waitlist-check {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #00D4FF, #7C3AED);
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
    font-size: 11px;
    color: #FFFFFF;
    font-weight: 700;
}
.waitlist-counter-box {
    background: rgba(0, 212, 255, 0.06);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 24px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.waitlist-counter-num {
    font-size: 32px;
    font-weight: 900;
    color: #00D4FF;
    letter-spacing: -1px;
    line-height: 1;
}
.waitlist-counter-label {
    color: #64748B;
    font-size: 13px;
    font-weight: 500;
    line-height: 1.4;
}
.waitlist-urgency {
    color: #64748B;
    font-size: 12px;
    font-weight: 500;
    text-align: center;
    margin-top: 12px;
    letter-spacing: 0.2px;
}

/* Streamlit form element overrides inside waitlist */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ── Auto-refresh: 1 s tick drives the countdown timer; cached data re-fetches
# ── only when TTLs expire (600 s), so the frequent reruns are lightweight.
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="neurotrade_tick")
except ImportError:
    pass

# ── Constants ─────────────────────────────────────────────────────────────────
COINS = {
    "bitcoin":       {"name": "Bitcoin",   "symbol": "BTC",  "color": "#F7931A"},
    "ethereum":      {"name": "Ethereum",  "symbol": "ETH",  "color": "#627EEA"},
    "solana":        {"name": "Solana",    "symbol": "SOL",  "color": "#9945FF"},
    "ripple":        {"name": "XRP",       "symbol": "XRP",  "color": "#00AAE4"},
    "cardano":       {"name": "Cardano",   "symbol": "ADA",  "color": "#0033AD"},
    "avalanche-2":   {"name": "Avalanche", "symbol": "AVAX", "color": "#E84142"},
    "dogecoin":      {"name": "Dogecoin",  "symbol": "DOGE", "color": "#C2A633"},
    "polkadot":      {"name": "Polkadot",  "symbol": "DOT",  "color": "#E6007A"},
    "chainlink":     {"name": "Chainlink", "symbol": "LINK", "color": "#2A5ADA"},
}

BG_CARD  = "#1E293B"
BG_CHART = "#162032"

def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert a 6-digit hex color string to rgba() notation."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ── Formatters ────────────────────────────────────────────────────────────────
def fmt_price(p):
    if p is None: return "—"
    return f"${p:,.0f}" if p >= 1000 else (f"${p:,.2f}" if p >= 1 else f"${p:.4f}")

def fmt_usd(n):
    if n is None: return "—"
    if n >= 1e12: return f"${n/1e12:.2f}T"
    if n >= 1e9:  return f"${n/1e9:.2f}B"
    if n >= 1e6:  return f"${n/1e6:.2f}M"
    return f"${n:,.0f}"

def change_badge(chg):
    if chg is None: return ""
    arrow = "▲" if chg >= 0 else "▼"
    cls   = "change-pos" if chg >= 0 else "change-neg"
    return f'<span class="{cls}">{arrow} {abs(chg):.2f}%</span>'

def fng_color(v):
    if v <= 25: return "#EF4444"
    if v <= 45: return "#F97316"
    if v <= 55: return "#EAB308"
    if v <= 75: return "#84CC16"
    return "#10B981"

def fng_text(v):
    if v <= 25: return "Extreme Fear"
    if v <= 45: return "Fear"
    if v <= 55: return "Neutral"
    if v <= 75: return "Greed"
    return "Extreme Greed"

# ── Data fetching ─────────────────────────────────────────────────────────────
HEADERS = {"Accept": "application/json", "User-Agent": "NeuroTrade/1.0 (contact@neurotrade.ai)"}

@st.cache_data(ttl=600, show_spinner=False)
def fetch_prices():
    ids = ",".join(COINS.keys())
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd"
        "&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
    )
    try:
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=8", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fng_history_30():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=30", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_onchain():
    try:
        r = requests.get("https://api.blockchain.info/stats", timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_eth_onchain():
    """ETH gas prices + USD price from Etherscan gas oracle."""
    try:
        r = requests.get(
            "https://api.etherscan.io/api?module=gastracker&action=gasoracle",
            timeout=10, headers=HEADERS,
        )
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "1" and "result" in data:
            # result keys: SafeGasPrice, ProposeGasPrice, FastGasPrice, suggestBaseFee, UsdPrice
            return data["result"]
        return None
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_trending():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/search/trending",
            timeout=10, headers=HEADERS,
        )
        r.raise_for_status()
        data = r.json()
        # Returns list of coin dicts under data["coins"][*]["item"]["id"]
        return [c["item"]["id"] for c in data.get("coins", [])]
    except Exception:
        return None

FRED_API_KEY = "767a5cb44cbff6d2abcc0f5b96f77317"

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fred_series(series_id: str, api_key: str):
    try:
        url = (
            "https://api.stlouisfed.org/fred/series/observations"
            f"?series_id={series_id}&api_key={api_key}"
            "&sort_order=desc&limit=1&file_type=json"
        )
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        obs = data.get("observations", [])
        if obs:
            return obs[0].get("value")
        return None
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_btc_yearly():
    try:
        url = (
            "https://api.coingecko.com/api/v3/coins/bitcoin"
            "/market_chart?vs_currency=usd&days=365"
        )
        r = requests.get(url, timeout=20, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        if "prices" not in data:
            return None
        df = pd.DataFrame(data["prices"], columns=["ts", "price"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms")
        return df
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_whale_transactions():
    try:
        url = "https://blockchain.info/unconfirmed-transactions?format=json&limit=100"
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        txs = data.get("txs", [])
        whales = []
        for tx in txs:
            out_value = sum(o.get("value", 0) for o in tx.get("out", []))
            btc_value = out_value / 1e8
            if btc_value >= 10:
                whales.append({
                    "hash":    tx.get("hash", "")[:16] + "...",
                    "btc":     btc_value,
                    "inputs":  len(tx.get("inputs", [])),
                    "outputs": len(tx.get("out", [])),
                })
        whales.sort(key=lambda x: x["btc"], reverse=True)
        return whales[:8]
    except Exception:
        return None

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_crypto_news(query="crypto OR bitcoin OR ethereum"):
    try:
        url = (
            "https://newsapi.org/v2/everything"
            f"?q={query}&sortBy=publishedAt&pageSize=8"
            "&language=en&apiKey=dee97ecf90624a32b779c7ef24d978e8"
        )
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_chart(coin_id: str):
    # Free CoinGecko tier: days=7 auto-returns hourly data; no interval param needed
    # 1-second delay per call to respect the free-tier rate limit (30 req/min).
    # Because this function is cached, the sleep only runs on actual API requests.
    time.sleep(1)
    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        "?vs_currency=usd&days=7"
    )
    try:
        r = requests.get(url, timeout=20, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        if "prices" not in data or not data["prices"]:
            return None
        df = pd.DataFrame(data["prices"], columns=["ts", "price"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms")
        return df
    except Exception:
        return None

# ── Chart builders ────────────────────────────────────────────────────────────
def make_sparkline(df, color):
    if df is None or df.empty:
        return None
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["ts"], y=df["price"],
        mode="lines",
        line=dict(color=color, width=2),
        fill="tozeroy",
        fillcolor=hex_to_rgba(color, 0.13),
        hovertemplate="$%{y:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        height=72,
    )
    return fig

def make_price_chart(df, meta):
    if df is None or df.empty:
        return None

    chg          = ((df["price"].iloc[-1] / df["price"].iloc[0]) - 1) * 100
    trend_color  = "#10B981" if chg >= 0 else "#EF4444"
    arrow        = "▲" if chg >= 0 else "▼"
    line_color   = meta["color"]
    fill_color   = hex_to_rgba(meta["color"], 0.20)
    is_large     = df["price"].mean() > 500

    fig = go.Figure()

    # Subtle range band (min/max shading)
    fig.add_trace(go.Scatter(
        x=df["ts"], y=df["price"],
        mode="lines",
        line=dict(color=line_color, width=3),
        fill="tozeroy",
        fillcolor=fill_color,
        hovertemplate="<b>$%{y:,.2f}</b><br>%{x|%b %d, %H:%M}<extra></extra>",
        name=meta["symbol"],
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=16, r=16, t=48, b=16),
        height=260,
        showlegend=False,
        hovermode="x unified",
        title=dict(
            text=(
                f"<b style='color:#FFFFFF'>{meta['name']}</b>"
                f"  <span style='color:{trend_color};font-size:14px'>"
                f"{arrow} {abs(chg):.2f}%</span>"
                f"  <span style='color:#475569;font-size:12px'>7 days</span>"
            ),
            font=dict(size=15, family="Inter"),
            x=0.02, xanchor="left",
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#E2E8F0",
            gridwidth=1,
            showline=False,
            zeroline=False,
            tickfont=dict(size=11, color="#64748B", family="Inter"),
            tickformat="%b %d",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E2E8F0",
            gridwidth=1,
            showline=False,
            zeroline=False,
            tickfont=dict(size=11, color="#64748B", family="Inter"),
            tickprefix="$",
            tickformat=",.0f" if is_large else ",.2f",
            side="right",
        ),
    )
    return fig

def make_fng_gauge(value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(font=dict(size=52, color=color, family="Inter"), suffix=""),
        gauge=dict(
            axis=dict(range=[0, 100], visible=False),
            bar=dict(color=color, thickness=0.3),
            bgcolor="#0B1120",
            borderwidth=0,
            steps=[
                {"range": [0,   25],  "color": "#2D0F0F"},
                {"range": [25,  45],  "color": "#2D1A0F"},
                {"range": [45,  55],  "color": "#2D2A0F"},
                {"range": [55,  75],  "color": "#162D0F"},
                {"range": [75,  100], "color": "#0F2D1A"},
            ],
            threshold=dict(
                line=dict(color=color, width=4),
                thickness=0.75,
                value=value,
            ),
        ),
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=210,
        font=dict(family="Inter"),
    )
    return fig

def make_fng_history(fng_data):
    entries = fng_data["data"][:7][::-1]
    dates   = [datetime.utcfromtimestamp(int(e["timestamp"])).strftime("%b %d") for e in entries]
    values  = [int(e["value"]) for e in entries]
    colors  = [fng_color(v) for v in values]

    fig = go.Figure(go.Bar(
        x=dates, y=values,
        marker_color=colors,
        marker_line_width=0,
        text=values,
        textposition="outside",
        textfont=dict(size=12, color="#94A3B8", family="Inter"),
        hovertemplate="%{x}: <b>%{y}</b><extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            showline=False,
            tickfont=dict(color="#64748B", size=11, family="Inter"),
        ),
        yaxis=dict(range=[0, 120], visible=False),
        height=160,
        showlegend=False,
        bargap=0.3,
    )
    return fig

def make_fng_line_30(fng_data):
    entries = fng_data["data"][:30][::-1]  # oldest → newest
    dates   = [datetime.utcfromtimestamp(int(e["timestamp"])).strftime("%b %d") for e in entries]
    values  = [int(e["value"]) for e in entries]
    colors  = [fng_color(v) for v in values]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode="lines+markers",
        line=dict(color="#00D4FF", width=2),
        marker=dict(color=colors, size=7, line=dict(width=0)),
        hovertemplate="%{x}: <b>%{y}</b><extra></extra>",
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.08)",
    ))
    # Zone bands
    for y0, y1, col in [(0,25,"rgba(239,68,68,0.06)"), (25,45,"rgba(249,115,22,0.06)"),
                         (55,75,"rgba(132,204,22,0.06)"), (75,100,"rgba(16,185,129,0.06)")]:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=col, line_width=0)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=8, t=12, b=8),
        height=200,
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(showgrid=False, showline=False,
                   tickfont=dict(color="#64748B", size=10, family="Inter"),
                   tickmode="array",
                   tickvals=dates[::5],
                   ticktext=dates[::5]),
        yaxis=dict(range=[0, 100], showgrid=True, gridcolor="#E2E8F0",
                   gridwidth=1, zeroline=False,
                   tickfont=dict(color="#64748B", size=10, family="Inter")),
    )
    return fig

# ── Combined Intelligence Score ───────────────────────────────────────────────
def compute_intelligence_score(prices, fng, onchain, charts, coin_id="bitcoin"):
    """
    Synthesizes available signals into a single 0–100 score for the given asset.
    Fear & Greed is always market-wide. Momentum, trend, and on-chain are asset-specific.
    On-chain data is only available for Bitcoin (Blockchain.com).
    Returns (score: int | None, components: dict, explanation: str)
    """
    WEIGHTS = {"fng": 0.30, "momentum": 0.25, "trend": 0.25, "onchain": 0.20}
    components = {}
    sym = COINS[coin_id]["symbol"]

    # 1. Fear & Greed (30%) — market-wide, always 0–100
    if fng and "data" in fng and fng["data"]:
        components["fng"] = float(int(fng["data"][0]["value"]))

    # 2. 24h momentum (25%) — map ±15 % to 0–100
    change_24h = None
    if prices and coin_id in prices:
        change_24h = prices[coin_id].get("usd_24h_change")
        if change_24h is not None:
            components["momentum"] = max(0.0, min(100.0, (change_24h + 15) / 30 * 100))

    # 3. 7-day trend (25%) — map ±25 % to 0–100
    change_7d = None
    df_asset = charts.get(coin_id) if charts else None
    if df_asset is not None and not df_asset.empty:
        change_7d = ((df_asset["price"].iloc[-1] / df_asset["price"].iloc[0]) - 1) * 100
        components["trend"] = max(0.0, min(100.0, (change_7d + 25) / 50 * 100))

    # 4. On-chain transaction volume (20%) — BTC only (Blockchain.com); skip for ETH/SOL
    n_tx = None
    if coin_id == "bitcoin" and onchain:
        n_tx = onchain.get("n_tx", 0)
        if n_tx:
            components["onchain"] = max(0.0, min(100.0, (n_tx - 150_000) / 350_000 * 100))

    if not components:
        return None, {}, "Insufficient data available to compute score."

    # Normalize weights to whichever components loaded successfully
    total_w = sum(WEIGHTS[k] for k in components)
    score   = round(sum(components[k] * WEIGHTS[k] for k in components) / total_w)

    # Plain-English explanation
    parts = []
    if "fng" in components:
        fv = components["fng"]
        if fv <= 25:   parts.append("extreme market fear is suppressing sentiment")
        elif fv <= 45: parts.append("market fear is weighing on sentiment")
        elif fv <= 55: parts.append("sentiment is neutral")
        elif fv <= 75: parts.append("market greed is lifting sentiment")
        else:          parts.append("extreme market greed is driving sentiment")

    if change_24h is not None:
        if change_24h > 5:    parts.append(f"{sym} surged +{change_24h:.1f}% in 24h")
        elif change_24h > 1:  parts.append(f"{sym} gained +{change_24h:.1f}% in 24h")
        elif change_24h > -1: parts.append(f"{sym} is flat over 24h")
        elif change_24h > -5: parts.append(f"{sym} slipped {change_24h:.1f}% in 24h")
        else:                 parts.append(f"{sym} dropped {change_24h:.1f}% in 24h")

    if change_7d is not None:
        if change_7d > 10:    parts.append(f"strong 7-day uptrend (+{change_7d:.1f}%)")
        elif change_7d > 2:   parts.append(f"positive 7-day trend (+{change_7d:.1f}%)")
        elif change_7d > -2:  parts.append("7-day price trend is flat")
        elif change_7d > -10: parts.append(f"negative 7-day trend ({change_7d:.1f}%)")
        else:                 parts.append(f"sharp 7-day downtrend ({change_7d:.1f}%)")

    if n_tx is not None:
        if n_tx > 420_000:   parts.append("high on-chain activity signals strong demand")
        elif n_tx > 260_000: parts.append("on-chain activity is at healthy levels")
        else:                parts.append("low on-chain activity signals weak demand")

    explanation = ("Driven by " + "; ".join(parts[:3]) + ".") if parts else \
                  "Score reflects all available market signals."
    return score, components, explanation


def score_meta(score):
    """Return (label, color, bar_gradient) for a given score."""
    if score <= 30:
        return "Strong Bear",  "#EF4444", "linear-gradient(90deg,#7F1D1D,#EF4444)"
    if score <= 45:
        return "Weak Bear",    "#F97316", "linear-gradient(90deg,#7C2D12,#F97316)"
    if score <= 55:
        return "Neutral",      "#94A3B8", "linear-gradient(90deg,#334155,#94A3B8)"
    if score <= 70:
        return "Weak Bull",    "#84CC16", "linear-gradient(90deg,#365314,#84CC16)"
    return     "Strong Bull",  "#10B981", "linear-gradient(90deg,#064E3B,#10B981)"


# ── FETCH ALL DATA ────────────────────────────────────────────────────────────
with st.spinner("Loading market data…"):
    prices      = fetch_prices()
    fng         = fetch_fear_greed()
    fng30       = fetch_fng_history_30()
    onchain     = fetch_onchain()
    eth_onchain = fetch_eth_onchain()
    trending    = fetch_trending()
    news        = fetch_crypto_news()
    btc_yearly  = fetch_btc_yearly()
    whale_txs   = fetch_whale_transactions()
    macro_dff   = fetch_fred_series("DFF",      FRED_API_KEY)
    macro_dxy   = fetch_fred_series("DTWEXBGS", FRED_API_KEY)
    macro_t10   = fetch_fred_series("T10YIE",   FRED_API_KEY)
    macro_unem  = fetch_fred_series("UNRATE",   FRED_API_KEY)
    charts      = {st.session_state.selected_asset: fetch_chart(st.session_state.selected_asset)}

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
col_logo, col_ts = st.columns([3, 1])

with col_logo:
    st.markdown("""
    <div style="padding:16px 0 8px 0; display:flex; align-items:center; gap:16px;">
        <span style="font-size:32px; font-weight:900;
                     background:linear-gradient(90deg,#00D4FF 0%,#7C3AED 100%);
                     -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                     letter-spacing:-1px; line-height:1;">
            ⬡ NeuroTrade
        </span>
        <span style="color:#334155; font-size:14px; font-weight:500;
                     border-left:1px solid #1E293B; padding-left:16px;">
            AI Crypto Intelligence Platform
        </span>
    </div>
    """, unsafe_allow_html=True)

with col_ts:
    now      = datetime.utcnow().strftime("%H:%M:%S UTC")
    elapsed  = int(time.time()) % 300
    remaining = 300 - elapsed
    mins     = remaining // 60
    secs     = remaining % 60
    timer_color = "#10B981" if remaining <= 30 else "#475569"

    hdr_c1, hdr_c2 = st.columns([2, 1])
    with hdr_c1:
        st.markdown(f"""
        <div style="text-align:right; padding-top:20px;">
            <div style="margin-bottom:4px;">
                <span class="live-dot"></span>
                <span style="color:#94A3B8; font-size:13px; font-weight:600; letter-spacing:1px;">
                    LIVE
                </span>
            </div>
            <div style="color:#475569; font-size:12px;">{now}</div>
            <div style="color:#334155; font-size:11px; margin-top:2px;">Auto-refresh: 5 min</div>
            <div style="font-size:11px; margin-top:2px; color:{timer_color};">
                Next refresh in {mins}:{secs:02d}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with hdr_c2:
        st.markdown("<div style='padding-top:18px;'>", unsafe_allow_html=True)
        toggle_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        if st.button(toggle_icon, key="theme_toggle", help="Toggle light/dark mode"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ── Inject light mode overrides if needed ─────────────────────────────────────
if st.session_state.theme == 'light':
    st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        background-color: #F0F4F8 !important;
        color: #1A202C !important;
    }
    ::-webkit-scrollbar-track { background: #E2E8F0; }
    ::-webkit-scrollbar-thumb { background: #94A3B8; }
    /* Section headers */
    .section-header {
        color: #1F2937 !important;
        border-bottom-color: #CBD5E1 !important;
    }
    .section-header::before { background: linear-gradient(180deg, #00d4ff, #7c3aed); }

    /* Cards and tiles */
    .price-card, .oc-tile, .intel-card, .chart-wrap, .fng-card {
        background: #FFFFFF !important;
        border-color: #CBD5E1 !important;
    }
    .price-card:hover, .oc-tile:hover { border-color: #94A3B8 !important; }

    /* Price card */
    .coin-price { color: #0F172A !important; }
    .coin-label, .subsection-label { color: #2D3748 !important; }
    .sub-item-label, .oc-label, .fng-sub,
    .oc-unit, .waitlist-urgency { color: #64748B !important; }
    .sub-item-value, .sub-row span { color: #374151 !important; }
    .sub-grid { border-top-color: #CBD5E1 !important; }

    /* Intelligence card */
    .intel-score-number { color: #0F172A !important; }
    .intel-label { color: #0F172A !important; }
    .intel-explanation { color: #374151 !important; }
    .intel-comp-value { color: #1F2937 !important; }
    .intel-comp-label { color: #4B5563 !important; }
    .intel-bar-track, .intel-comp-bar-track {
        background: #E2E8F0 !important;
        border-color: #CBD5E1 !important;
    }
    .intel-comp-bar-fill + div, [style*="color:#334155"] { color: #64748B !important; }

    /* On-chain tiles */
    .oc-value { color: #0F172A !important; }

    /* F&G */
    .fng-label-big { color: inherit; }

    /* Chart area */
    .chart-wrap { background: #FFFFFF !important; }

    /* Dropdown selector */
    [data-testid="stSelectbox"] > div > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-color: #CBD5E1 !important;
    }
    [data-testid="stSelectbox"] > div > div > div { color: #0F172A !important; }
    [data-testid="stSelectbox"] svg { fill: #0F172A !important; }
    [data-baseweb="select"] * {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    [data-baseweb="popover"] * {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[role="option"]:hover { background-color: #F1F5F9 !important; }
    div[data-baseweb="select"] {
        background: #FFFFFF !important;
        border-color: #CBD5E1 !important;
    }
    div[data-baseweb="select"] * { color: #0F172A !important; }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
    }
    div[data-baseweb="select"] span { color: #0F172A !important; }
    div[data-baseweb="popover"] { background-color: #FFFFFF !important; }
    div[data-baseweb="menu"] { background-color: #FFFFFF !important; }
    div[data-baseweb="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    div[data-baseweb="option"]:hover { background-color: #F1F5F9 !important; }

    /* Waitlist */
    .waitlist-card {
        background: linear-gradient(135deg, #EBF4FF 0%, #F0E6FF 100%) !important;
        border-color: #CBD5E1 !important;
    }
    .waitlist-headline { color: #0F172A !important; }
    .waitlist-sub { color: #374151 !important; }
    .waitlist-value-point,
    .waitlist-card p { color: #1F2937 !important; }
    .waitlist-counter-box {
        background: rgba(0,180,220,0.06) !important;
        border-color: rgba(0,180,220,0.2) !important;
    }
    .waitlist-counter-num { color: #0284C7 !important; }
    .waitlist-counter-label { color: #374151 !important; }

    /* BTC reference price tile */
    div[style*="background:#162032"] {
        background: #1E293B !important;
    }

    /* Email input */
    [data-testid="stTextInput"] > div > div > input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-color: #CBD5E1 !important;
    }
    [data-testid="stTextInput"] > div > div {
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
    }

    /* Footer */
    div[style*="border-top"] span { color: #6B7280 !important; }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# COMBINED INTELLIGENCE SCORE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Combined Intelligence Score</div>',
            unsafe_allow_html=True)

# ── Asset selector ────────────────────────────────────────────────────────────
ASSET_COLORS = {cid: meta["color"] for cid, meta in COINS.items()}

if st.session_state.selected_asset not in ASSET_COLORS:
    st.session_state.selected_asset = 'bitcoin'

# Style the selectbox to match the dashboard aesthetic
st.markdown(f"""
<style>
div[data-testid="stSelectbox"] > div > div {{
    background: #1E293B !important;
    border: 1.5px solid #334155 !important;
    border-radius: 12px !important;
    color: #CBD5E1 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}}
div[data-testid="stSelectbox"] > div > div:hover {{
    border-color: #475569 !important;
}}
div[data-testid="stSelectbox"] > div > div > div {{
    color: #CBD5E1 !important;
}}
div[data-testid="stSelectbox"] svg {{
    fill: #64748B !important;
}}
</style>
""", unsafe_allow_html=True)

sel_col, _ = st.columns([2, 5])
with sel_col:
    selected_coin = st.selectbox(
        "Select Asset",
        options=list(COINS.keys()),
        format_func=lambda x: f"{COINS[x]['symbol']} · {COINS[x]['name']}",
        index=list(COINS.keys()).index(st.session_state.selected_asset),
        label_visibility="collapsed",
        key="asset_selectbox",
    )
st.session_state.selected_asset = selected_coin

st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

selected_meta = COINS[selected_coin]
asset_color   = ASSET_COLORS[selected_coin]

# ── Compute score for selected asset ─────────────────────────────────────────
score, comp_scores, explanation = compute_intelligence_score(
    prices, fng, onchain, charts, coin_id=selected_coin
)

# On-chain available only for BTC
has_onchain = (selected_coin == "bitcoin")
sym = selected_meta["symbol"]

WEIGHTS_DISPLAY = {
    "fng":      (f"Fear & Greed Index",        30, "Market-wide signal"),
    "momentum": (f"{sym} 24h Momentum",        25, f"{sym} price change over 24 hours"),
    "trend":    (f"{sym} 7-Day Trend",         25, f"{sym} price change over 7 days"),
    "onchain":  ("BTC On-Chain Volume",        20, "Bitcoin daily transaction count"
                 if has_onchain else "Not available for " + sym),
}

if score is not None:
    label, s_color, bar_grad = score_meta(score)

    left_score, right_breakdown = st.columns([2, 3], gap="large")

    with left_score:
        st.markdown(f"""
        <div class="intel-card">
            <div style="display:flex; align-items:flex-end; gap:20px; flex-wrap:wrap;">
                <div>
                    <div style="color:#64748B; font-size:11px; font-weight:700;
                                letter-spacing:2px; text-transform:uppercase;
                                margin-bottom:10px;">
                        {sym} · AI Market Signal
                    </div>
                    <div class="intel-score-number" style="color:{s_color};">
                        {score}
                    </div>
                    <div class="intel-label" style="color:{s_color};">{label}</div>
                </div>
                <div style="flex:1; min-width:130px; padding-bottom:8px;">
                    <div style="color:#475569; font-size:10px; font-weight:600;
                                letter-spacing:1px; text-transform:uppercase;
                                margin-bottom:6px; text-align:right;">
                        BEAR &nbsp;·&nbsp; 0 ——— 100 &nbsp;·&nbsp; BULL
                    </div>
                    <div class="intel-bar-track">
                        <div class="intel-bar-fill"
                             style="width:{score}%; background:{bar_grad};">
                        </div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:6px;">
                        <span style="color:#334155; font-size:10px;">Strong Bear</span>
                        <span style="color:#334155; font-size:10px;">Strong Bull</span>
                    </div>
                </div>
            </div>
            <div class="intel-explanation">
                ⓘ &nbsp;{explanation}
            </div>
            {
            f'<div style="margin-top:14px; padding-top:14px; border-top:1px solid #334155;">'
            f'<span style="color:#334155; font-size:11px; font-weight:500;">'
            f'⚠ On-chain component excluded for {sym} — Blockchain.com data covers Bitcoin only. '
            f'Weight redistributed across remaining signals.'
            f'</span></div>'
            if not has_onchain else ""
            }
        </div>
        """, unsafe_allow_html=True)

    with right_breakdown:
        st.markdown(f"""
        <div style="color:#64748B; font-size:11px; font-weight:700; letter-spacing:2px;
                    text-transform:uppercase; margin-bottom:16px; margin-top:4px;">
            Signal Breakdown &nbsp;·&nbsp;
            <span style="color:{asset_color}; font-weight:700;">{sym}</span>
        </div>
        """, unsafe_allow_html=True)

        for key, (display_name, weight_pct, note) in WEIGHTS_DISPLAY.items():
            if key in comp_scores:
                raw = comp_scores[key]
                lbl, col, grad = score_meta(round(raw))
                st.markdown(f"""
                <div class="intel-component" style="margin-bottom:20px;">
                    <div style="display:flex; justify-content:space-between;
                                align-items:baseline; margin-bottom:6px;">
                        <span class="intel-comp-label">{display_name}
                            <span style="color:#1E3A5F; font-weight:400;">
                                &nbsp;{weight_pct}%
                            </span>
                        </span>
                        <span class="intel-comp-value" style="color:{col};">
                            {round(raw)}&nbsp;
                            <span style="font-size:11px; color:#475569;">{lbl}</span>
                        </span>
                    </div>
                    <div class="intel-comp-bar-track">
                        <div class="intel-comp-bar-fill"
                             style="width:{raw:.1f}%; background:{grad};">
                        </div>
                    </div>
                    <div style="color:#334155; font-size:10px; margin-top:4px;">{note}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Unavailable component (e.g. on-chain for ETH/SOL)
                is_excluded = (key == "onchain" and not has_onchain)
                note_text   = f"Excluded — {note}" if is_excluded else "Awaiting data…"
                st.markdown(f"""
                <div class="intel-component" style="margin-bottom:20px; opacity:0.45;">
                    <div style="display:flex; justify-content:space-between;
                                align-items:baseline; margin-bottom:6px;">
                        <span class="intel-comp-label">{display_name}
                            <span style="color:#1E293B; font-weight:400;">&nbsp;{weight_pct}%</span>
                        </span>
                        <span style="color:#334155; font-size:12px;">—</span>
                    </div>
                    <div class="intel-comp-bar-track">
                        <div style="width:0%; height:100%;"></div>
                    </div>
                    <div style="color:#334155; font-size:10px; margin-top:4px;">{note_text}</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="intel-card" style="text-align:center; padding:48px;">
        <div style="color:#475569; font-size:16px;">
            Gathering signals — score will appear once data loads.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MARKET PRICES
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="section-header">Market Prices &nbsp;·&nbsp; '
    f'<span style="color:{asset_color};">{selected_meta["name"]}</span></div>',
    unsafe_allow_html=True,
)

# Single full-width card for the selected asset
_pc_meta = selected_meta
_pc_glow = (
    f"box-shadow:0 0 0 2px {asset_color}, 0 0 32px {asset_color}55, 0 8px 48px rgba(0,0,0,0.5);"
    f"border-color:{asset_color};"
)
if prices and selected_coin in prices:
    _p     = prices[selected_coin]
    _price = _p.get("usd")
    _chg   = _p.get("usd_24h_change")
    _mcap  = _p.get("usd_market_cap")
    _vol   = _p.get("usd_24h_vol")
    st.markdown(
        f'<div class="price-card" style="--accent:{asset_color}; {_pc_glow}">'
        f'<div class="coin-label" style="color:{asset_color}; font-size:15px;">'
        f'<span class="coin-dot" style="background:{asset_color}; width:12px; height:12px;"></span>'
        f'{_pc_meta["symbol"]}'
        f'<span style="color:#475569; font-weight:400;"> · </span>'
        f'<span style="color:#94A3B8; font-weight:500;">{_pc_meta["name"]}</span>'
        f'</div>'
        f'<div class="coin-price">{fmt_price(_price)}</div>'
        f'<div style="margin:6px 0 0 0;">'
        f'{change_badge(_chg)}'
        f'<span style="color:#475569; font-size:13px; margin-left:8px;">24h change</span>'
        f'</div>'
        f'<div class="sub-grid" style="margin-top:16px;">'
        f'<div><div class="sub-item-label">Market Cap</div>'
        f'<div class="sub-item-value" style="font-size:16px;">{fmt_usd(_mcap)}</div></div>'
        f'<div><div class="sub-item-label">Volume 24h</div>'
        f'<div class="sub-item-value" style="font-size:16px;">{fmt_usd(_vol)}</div></div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    _spark = make_sparkline(charts.get(selected_coin), asset_color)
    if _spark:
        st.plotly_chart(_spark, use_container_width=True,
                        config={"displayModeBar": False})
else:
    st.markdown(
        f'<div class="price-card" style="--accent:#334155;">'
        f'<div class="coin-label" style="color:#475569;">'
        f'<span class="coin-dot" style="background:{asset_color};"></span>'
        f'{_pc_meta["symbol"]} · {_pc_meta["name"]}'
        f'</div>'
        f'<div class="coin-price" style="color:#334155;">Data unavailable</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# 7-DAY PRICE HISTORY CHARTS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="section-header">7-Day Price History &nbsp;·&nbsp; '
    f'<span style="color:{asset_color};">{selected_meta["name"]}</span></div>',
    unsafe_allow_html=True,
)

# Single full-width chart for the selected asset only
_chart_df  = charts.get(selected_coin)
_chart_fig = make_price_chart(_chart_df, selected_meta)
if _chart_fig:
    st.plotly_chart(_chart_fig, use_container_width=True,
                    config={"displayModeBar": False})
else:
    st.markdown(
        f'<div class="oc-tile" style="height:280px; display:flex; flex-direction:column;'
        f' align-items:center; justify-content:center; gap:10px;">'
        f'<div style="font-size:32px;">📡</div>'
        f'<div style="color:#475569; font-size:14px; font-weight:600;">'
        f'{selected_meta["name"]} chart loading…</div>'
        f'<div style="color:#334155; font-size:12px;">CoinGecko rate limit — refreshes in 5 min</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# SENTIMENT & ON-CHAIN  (right panel responds to selected asset)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="section-header">Sentiment &amp; On-Chain Metrics &nbsp;·&nbsp; '
    f'<span style="color:{asset_color};">{selected_meta["name"]}</span></div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 2], gap="large")

# ── Crypto Market Sentiment (Fear & Greed) — always market-wide ───────────────
with left:
    st.markdown('<div class="subsection-label">Crypto Market Sentiment</div>',
                unsafe_allow_html=True)

    if fng and "data" in fng and fng["data"]:
        cur   = fng["data"][0]
        val   = int(cur["value"])
        label = cur.get("value_classification", fng_text(val))
        color = fng_color(val)

        st.plotly_chart(make_fng_gauge(val, color),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""
        <div class="fng-label-big" style="color:{color};">{label}</div>
        <div class="fng-sub">Today's reading · Score {val}/100</div>
        <div class="fng-sub" style="margin-top:6px; font-size:11px; color:#64748B;">
            Market-wide crypto sentiment index
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="subsection-label" style="margin-top:28px;">7-Day History</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(make_fng_history(fng),
                        use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown("""
        <div class="oc-tile" style="text-align:center; padding:48px 24px; color:#475569;">
            <div style="font-size:28px; margin-bottom:8px;">📊</div>
            <div style="font-size:14px;">Sentiment data unavailable</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Trending Status ───────────────────────────────────────────────────────
    st.markdown('<div class="subsection-label" style="margin-top:28px;">Trending Status</div>',
                unsafe_allow_html=True)
    if trending is None:
        st.markdown(
            '<div class="oc-tile">'
            '<div class="oc-label">Trending Status</div>'
            '<div class="oc-value" style="color:#475569; font-size:16px;">Unavailable</div>'
            '<div style="color:#475569; font-size:11px; margin-top:6px;">CoinGecko search ranking updated hourly</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    elif selected_coin in trending:
        _trend_rank = trending.index(selected_coin) + 1
        st.markdown(
            f'<div class="oc-tile">'
            f'<div class="oc-label">Trending Status</div>'
            f'<div class="oc-value" style="color:#10B981; font-size:22px; font-weight:800;">🔥 TRENDING</div>'
            f'<div style="color:#10B981; font-size:12px; font-weight:600; margin-top:4px; letter-spacing:1px;">#{_trend_rank} on CoinGecko right now</div>'
            f'<div style="color:#475569; font-size:11px; margin-top:6px;">CoinGecko search ranking updated hourly</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="oc-tile">'
            '<div class="oc-label">Trending Status</div>'
            '<div class="oc-value" style="color:#475569; font-size:22px; font-weight:800;">NOT TRENDING</div>'
            '<div style="color:#475569; font-size:12px; margin-top:4px;">Not in top 7 searches</div>'
            '<div style="color:#475569; font-size:11px; margin-top:6px;">CoinGecko search ranking updated hourly</div>'
            '</div>',
            unsafe_allow_html=True,
        )

# ── On-Chain panel — switches by selected asset ───────────────────────────────
with right:

    if selected_coin == "bitcoin":
        st.markdown('<div class="subsection-label">Bitcoin On-Chain Metrics</div>',
                    unsafe_allow_html=True)

        if onchain:
            hash_rate  = onchain.get("hash_rate", 0) / 1e9
            difficulty = onchain.get("difficulty", 0) / 1e12
            n_tx       = onchain.get("n_tx", 0)
            blk_time   = onchain.get("minutes_between_blocks", 0)
            total_btc  = onchain.get("totalbc", 0) / 1e8
            trade_vol  = onchain.get("trade_volume_btc", 0)
            market_px  = onchain.get("market_price_usd", 0)

            tiles = [
                ("Hash Rate",          f"{hash_rate:.2f}",   "EH/s"),
                ("Mining Difficulty",  f"{difficulty:.2f}T", ""),
                ("Transactions Today", f"{n_tx:,}",          ""),
                ("Avg Block Time",     f"{blk_time:.1f}",    "min"),
                ("BTC Circulating",    f"{total_btc:,.0f}",  "BTC"),
                ("Trade Volume",       f"{trade_vol:,.1f}",  "BTC"),
            ]

            r1 = st.columns(3, gap="medium")
            r2 = st.columns(3, gap="medium")
            for (lbl, val, unit), col in zip(tiles, list(r1) + list(r2)):
                with col:
                    st.markdown(f"""
                    <div class="oc-tile">
                        <div class="oc-label">{lbl}</div>
                        <div class="oc-value">{val}<span class="oc-unit">{unit}</span></div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

            w1, w2 = st.columns(2, gap="medium")
            with w1:
                if n_tx > 400_000:
                    nh_label, nh_color = "HIGH",   "#10B981"
                elif n_tx > 200_000:
                    nh_label, nh_color = "MEDIUM", "#F97316"
                else:
                    nh_label, nh_color = "LOW",    "#EF4444"
                st.markdown(f"""
                <div class="oc-tile">
                    <div class="oc-label">Network Health</div>
                    <div class="oc-value" style="color:{nh_color};">{nh_label}
                        <span class="oc-unit" style="color:{nh_color}88;">based on {n_tx:,} tx/day</span>
                    </div>
                </div>""", unsafe_allow_html=True)
            with w2:
                st.markdown(f"""
                <div class="oc-tile">
                    <div class="oc-label">Exchange Trade Volume (24h)</div>
                    <div class="oc-value">{trade_vol:,.1f}<span class="oc-unit">BTC</span></div>
                </div>""", unsafe_allow_html=True)

            if market_px:
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:#162032; border:1px solid #334155; border-radius:16px;
                            padding:20px 28px; display:flex; align-items:center; justify-content:space-between;">
                    <div>
                        <div style="color:#64748B; font-size:11px; font-weight:700;
                                    letter-spacing:2px; text-transform:uppercase; margin-bottom:6px;">
                            BTC Reference Price · Blockchain.com
                        </div>
                        <div style="color:#94A3B8; font-size:13px;">
                            Independent price feed for cross-reference
                        </div>
                    </div>
                    <div style="color:#F7931A; font-size:32px; font-weight:800; letter-spacing:-1px;">
                        ${market_px:,.2f}
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="oc-tile" style="text-align:center; padding:60px 24px; color:#475569;">
                <div style="font-size:28px; margin-bottom:8px;">⛓️</div>
                <div style="font-size:14px;">Blockchain data unavailable</div>
            </div>""", unsafe_allow_html=True)

    elif selected_coin == "ethereum":
        st.markdown('<div class="subsection-label">Ethereum Network Metrics</div>',
                    unsafe_allow_html=True)

        # ── Derive values ──────────────────────────────────────────────────────
        _ep = prices.get("ethereum", {}) if prices else {}
        _eth_price    = fmt_price(_ep.get("usd"))
        _eth_chg      = _ep.get("usd_24h_change", 0) or 0
        _eth_chg_col  = "#10B981" if _eth_chg >= 0 else "#EF4444"
        _eth_mcap     = fmt_usd(_ep.get("usd_market_cap"))
        _eth_vol      = fmt_usd(_ep.get("usd_24h_vol"))

        _eth_df = charts.get("ethereum") if charts else None
        if _eth_df is not None and not _eth_df.empty:
            _eth_7d = ((_eth_df["price"].iloc[-1] / _eth_df["price"].iloc[0]) - 1) * 100
        else:
            _eth_7d = None

        # ── Row 1: Price · 24h Change · Market Cap ────────────────────────────
        _er1 = st.columns(3, gap="medium")
        with _er1[0]:
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">ETH Price</div>'
                f'<div class="oc-value">{_eth_price}<span class="oc-unit">USD</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        with _er1[1]:
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">24h Change</div>'
                f'<div class="oc-value" style="color:{_eth_chg_col};">{_eth_chg:+.2f}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        with _er1[2]:
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">Market Cap</div>'
                f'<div class="oc-value">{_eth_mcap}<span class="oc-unit">USD</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # ── Row 2: 24h Volume · 7-Day Trend · Gas Prices ─────────────────────
        _er2 = st.columns(3, gap="medium")
        with _er2[0]:
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">24h Volume</div>'
                f'<div class="oc-value">{_eth_vol}<span class="oc-unit">USD</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        with _er2[1]:
            if _eth_7d is not None:
                _t_col = "#10B981" if _eth_7d >= 0 else "#EF4444"
                _t_val = f"{_eth_7d:+.2f}%"
            else:
                _t_col, _t_val = "#475569", "—"
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">7-Day Trend</div>'
                f'<div class="oc-value" style="color:{_t_col};">{_t_val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        with _er2[2]:
            if eth_onchain and eth_onchain.get("SafeGasPrice"):
                _gas_safe = eth_onchain.get("SafeGasPrice", "—")
                _gas_std  = eth_onchain.get("ProposeGasPrice", "—")
                _gas_fast = eth_onchain.get("FastGasPrice", "—")
                st.markdown(
                    f'<div class="oc-tile">'
                    f'<div class="oc-label">Gas Price (Gwei)</div>'
                    f'<div style="margin-top:8px; display:flex; flex-direction:column; gap:4px;">'
                    f'<div style="display:flex; justify-content:space-between; font-size:12px;">'
                    f'<span style="color:#64748B;">Safe</span>'
                    f'<span style="color:#10B981; font-weight:600;">{_gas_safe}</span></div>'
                    f'<div style="display:flex; justify-content:space-between; font-size:12px;">'
                    f'<span style="color:#64748B;">Standard</span>'
                    f'<span style="color:#F59E0B; font-weight:600;">{_gas_std}</span></div>'
                    f'<div style="display:flex; justify-content:space-between; font-size:12px;">'
                    f'<span style="color:#64748B;">Fast</span>'
                    f'<span style="color:#EF4444; font-weight:600;">{_gas_fast}</span></div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="oc-tile">'
                    '<div class="oc-label">Gas Price (Gwei)</div>'
                    '<div class="oc-value" style="color:#475569; font-size:16px;">Unavailable</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    elif selected_coin == "solana":
        st.markdown('<div class="subsection-label">Solana Network Metrics</div>',
                    unsafe_allow_html=True)
        if prices and "solana" in prices:
            p = prices["solana"]
            sol_tiles = [
                ("SOL Price",  fmt_price(p.get("usd")),              "USD"),
                ("24h Change", f"{p.get('usd_24h_change', 0):.2f}%", ""),
                ("Market Cap", fmt_usd(p.get("usd_market_cap")),     ""),
                ("24h Volume", fmt_usd(p.get("usd_24h_vol")),        ""),
            ]
            r1 = st.columns(4, gap="medium")
            for (label, value, unit), col in zip(sol_tiles, r1):
                with col:
                    st.markdown(f"""
                    <div class="oc-tile">
                        <div class="oc-label">{label}</div>
                        <div class="oc-value">{value}
                            <span class="oc-unit">{unit}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="oc-tile" style="margin-top:8px; opacity:0.6;">
            <div class="oc-label">Full On-Chain Data</div>
            <div class="oc-value" style="font-size:16px; color:#64748B;">
                Coming soon
            </div>
        </div>""", unsafe_allow_html=True)

    else:
        # Generic panel for XRP, ADA, AVAX, DOGE, DOT, LINK
        _coin_meta = COINS[selected_coin]
        st.markdown(
            f'<div class="subsection-label">{_coin_meta["name"]} Market Data</div>',
            unsafe_allow_html=True,
        )
        if prices and selected_coin in prices:
            _p = prices[selected_coin]
            _chg = _p.get("usd_24h_change", 0) or 0
            _chg_color = "#10B981" if _chg >= 0 else "#EF4444"
            _generic_tiles = [
                (f"{_coin_meta['symbol']} Price",  fmt_price(_p.get("usd")),      "USD"),
                ("24h Change",                      f"{_chg:+.2f}%",               ""),
                ("Market Cap",                      fmt_usd(_p.get("usd_market_cap")), ""),
                ("24h Volume",                      fmt_usd(_p.get("usd_24h_vol")),    ""),
            ]
            _gt_row = st.columns(4, gap="medium")
            for (_lbl, _val, _unit), _col in zip(_generic_tiles, _gt_row):
                with _col:
                    _val_color = _chg_color if _lbl == "24h Change" else "#E2E8F0"
                    st.markdown(
                        f'<div class="oc-tile">'
                        f'<div class="oc-label">{_lbl}</div>'
                        f'<div class="oc-value" style="color:{_val_color};">{_val}'
                        f'<span class="oc-unit">{_unit}</span></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="oc-tile" style="text-align:center; padding:60px 24px; color:#475569;">'
                '<div style="font-size:28px; margin-bottom:8px;">📊</div>'
                '<div style="font-size:14px;">Market data unavailable</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div class="oc-tile" style="margin-top:8px; opacity:0.6;">'
            '<div class="oc-label">Network &amp; On-Chain Data</div>'
            '<div class="oc-value" style="font-size:16px; color:#64748B;">Coming soon</div>'
            '</div>',
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════════════════════════════════════
# LATEST CRYPTO NEWS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Latest Crypto News</div>', unsafe_allow_html=True)

_BULLISH_KW = {"surge", "rally", "gain", "high", "bull", "rise", "up", "record", "adoption", "approve"}
_BEARISH_KW = {"crash", "drop", "fall", "bear", "low", "hack", "ban", "sell", "fear", "warning"}

def _news_sentiment(title: str):
    words = set(title.lower().split())
    if words & _BULLISH_KW:
        return "BULLISH", "#10B981"
    if words & _BEARISH_KW:
        return "BEARISH", "#EF4444"
    return "NEUTRAL", "#64748B"

def _time_ago(published_at: str) -> str:
    try:
        pub = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        delta = datetime.utcnow() - pub
        mins  = int(delta.total_seconds() // 60)
        if mins < 60:
            return f"{mins}m ago"
        hours = mins // 60
        if hours < 24:
            return f"{hours}h ago"
        return f"{hours // 24}d ago"
    except Exception:
        return ""

_articles = (news or {}).get("articles", [])
if _articles:
    _news_cols = st.columns(2, gap="large")
    for i, article in enumerate(_articles[:8]):
        _title  = article.get("title") or ""
        _source = (article.get("source") or {}).get("name", "")
        _pub    = article.get("publishedAt", "")
        _url    = article.get("url", "#")
        _ago    = _time_ago(_pub)
        _slabel, _scolor = _news_sentiment(_title)
        with _news_cols[i % 2]:
            st.markdown(
                f'<div class="oc-tile" style="margin-bottom:8px;">'
                f'<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">'
                f'<a href="{_url}" target="_blank" rel="noopener" style="color:#4A90D9; font-size:13px;'
                f' font-weight:600; line-height:1.4; text-decoration:none; flex:1;">{_title}</a>'
                f'<span style="font-size:10px; font-weight:700; letter-spacing:1px; color:{_scolor};'
                f' white-space:nowrap; margin-top:2px;">{_slabel}</span>'
                f'</div>'
                f'<div style="margin-top:8px; color:#6B7280; font-size:11px;">'
                f'{_source}'
                f'{"&nbsp;·&nbsp;" + _ago if _ago else ""}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        '<div class="oc-tile" style="text-align:center; padding:48px 24px; color:#475569;">'
        '<div style="font-size:28px; margin-bottom:8px;">📰</div>'
        '<div style="font-size:14px;">News unavailable — add your NewsAPI key to enable this section</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Signal Intelligence</div>', unsafe_allow_html=True)

_fng30_entries = (fng30 or {}).get("data", [])[:30] if fng30 else []

if _fng30_entries:
    _vals    = [int(e["value"]) for e in _fng30_entries]
    _today   = _vals[0]
    _avg     = sum(_vals) / len(_vals)
    _extreme_fear_days = sum(1 for v in _vals if v <= 25)
    _today_zone = fng_text(_today)

    # Consecutive days in current zone
    _consec = 0
    for v in _vals:
        if fng_text(v) == _today_zone:
            _consec += 1
        else:
            break

    # Tile 1 — Extreme Fear Days
    _ef_color = "#EF4444" if _extreme_fear_days > 15 else "#F97316" if _extreme_fear_days > 10 else "#10B981"

    # Tile 2 — 30-Day Avg Sentiment
    _avg_color = fng_color(int(_avg))

    # Tile 3 — Sentiment Trend
    _trend_label = "Improving" if _today > _avg else "Deteriorating"
    _trend_color = "#10B981" if _today > _avg else "#EF4444"

    # Tile 4 — Consecutive Days in Zone
    _zone_color = fng_color(_today)

    _sig_cols = st.columns(4, gap="large")
    _sig_tiles = [
        ("Extreme Fear Days", f"{_extreme_fear_days}", "/ 30 days", _ef_color),
        ("30-Day Avg Sentiment", f"{_avg:.0f}", f"/ 100  ·  {fng_text(int(_avg))}", _avg_color),
        ("Sentiment Trend", _trend_label, f"vs {_avg:.0f} avg", _trend_color),
        ("Days in Current Zone", f"{_consec}", _today_zone, _zone_color),
    ]
    for col, (lbl, val, sub, col_) in zip(_sig_cols, _sig_tiles):
        with col:
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">{lbl}</div>'
                f'<div class="oc-value" style="color:{col_}; font-size:28px;">{val}</div>'
                f'<div style="color:#64748B; font-size:11px; margin-top:4px;">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.plotly_chart(make_fng_line_30(fng30), use_container_width=True,
                    config={"displayModeBar": False})
else:
    st.markdown(
        '<div class="oc-tile" style="text-align:center; padding:48px 24px; color:#475569;">'
        '<div style="font-size:28px; margin-bottom:8px;">📊</div>'
        '<div style="font-size:14px;">Signal history unavailable</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# MACRO INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Macro Intelligence</div>', unsafe_allow_html=True)

def _safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

_dff  = _safe_float(macro_dff)
_dxy  = _safe_float(macro_dxy)
_t10  = _safe_float(macro_t10)
_unem = _safe_float(macro_unem)

# Dollar index color: green < 100 (weak dollar good), red > 104 (strong dollar bad)
_dxy_color = (
    "#10B981" if _dxy is not None and _dxy < 100 else
    "#EF4444" if _dxy is not None and _dxy > 104 else
    "#94A3B8"
)

_macro_tiles = [
    (
        "Fed Funds Rate",
        f"{_dff:.2f}" if _dff is not None else "—",
        "%",
        "#94A3B8",
        "Current interest rate target",
    ),
    (
        "US Dollar Index",
        f"{_dxy:.2f}" if _dxy is not None else "—",
        "",
        _dxy_color,
        "Dollar strength vs major currencies",
    ),
    (
        "10Y Inflation Expectations",
        f"{_t10:.2f}" if _t10 is not None else "—",
        "%",
        "#94A3B8",
        "Market implied inflation rate",
    ),
    (
        "Unemployment Rate",
        f"{_unem:.1f}" if _unem is not None else "—",
        "%",
        "#94A3B8",
        "US labor market health",
    ),
]

_macro_cols = st.columns(4, gap="large")
for col, (lbl, val, unit, col_, note) in zip(_macro_cols, _macro_tiles):
    with col:
        st.markdown(
            f'<div class="oc-tile">'
            f'<div class="oc-label">{lbl}</div>'
            f'<div class="oc-value" style="color:{col_};">{val}'
            f'<span class="oc-unit">{unit}</span></div>'
            f'<div style="color:#475569; font-size:11px; margin-top:6px;">{note}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# Plain-English macro summary
_macro_insights = []
if _dxy is not None:
    if _dxy > 104:
        _macro_insights.append("Strong dollar environment is historically a headwind for crypto assets.")
    elif _dxy < 100:
        _macro_insights.append("Weak dollar typically supports crypto and broader risk assets.")
if _dff is not None:
    if _dff > 4:
        _macro_insights.append("High rate environment increases opportunity cost of holding crypto.")
    elif _dff < 2:
        _macro_insights.append("Low rate environment is historically favourable for risk assets.")

if _macro_insights:
    st.markdown(
        '<div class="intel-explanation oc-tile" style="margin-top:16px;'
        ' font-size:13px; line-height:1.7;">'
        + "  ".join(f"· {s}" for s in _macro_insights)
        + '</div>',
        unsafe_allow_html=True,
    )
elif _dff is None and _dxy is None:
    st.markdown(
        '<div class="oc-tile" style="margin-top:12px; text-align:center;'
        ' padding:32px 24px; color:#475569;">'
        '<div style="font-size:14px;">Macro data unavailable — add your FRED API key to enable</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL BACKTESTING
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Signal Backtesting</div>', unsafe_allow_html=True)

try:
    _bt_fng_entries = (fng30 or {}).get("data", [])[:30] if fng30 else []

    if not _bt_fng_entries:
        raise ValueError("No F&G data")

    _fng_dates  = [datetime.utcfromtimestamp(int(e["timestamp"])) for e in reversed(_bt_fng_entries)]
    _fng_values = [int(e["value"]) for e in reversed(_bt_fng_entries)]
    _fng_colors = [fng_color(v) for v in _fng_values]

    # Use yearly data if available, else fall back to the 7-day selected chart
    _price_df = btc_yearly if (btc_yearly is not None and not btc_yearly.empty) \
                else charts.get("bitcoin") or charts.get(selected_coin)

    # ── Two stacked subplots (independent x-axes) ────────────────────────────
    _bt_fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        row_heights=[0.6, 0.4],
        vertical_spacing=0.10,
        subplot_titles=("BTC Price (USD)", "Fear & Greed Index (30 days)"),
    )

    if _price_df is not None and not _price_df.empty:
        _bt_fig.add_trace(go.Scatter(
            x=_price_df["ts"], y=_price_df["price"],
            mode="lines",
            name="BTC Price",
            line=dict(color="#F7931A", width=2),
            fill="tozeroy",
            fillcolor="rgba(247,147,26,0.10)",
            hovertemplate="$%{y:,.0f}<extra>BTC Price</extra>",
        ), row=1, col=1)

    _bt_fig.add_trace(go.Scatter(
        x=_fng_dates, y=_fng_values,
        mode="lines+markers",
        name="Fear & Greed",
        line=dict(color="#00D4FF", width=2),
        marker=dict(color=_fng_colors, size=7, line=dict(width=0)),
        hovertemplate="%{y}<extra>Fear & Greed</extra>",
    ), row=2, col=1)

    _bt_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=8, t=32, b=8),
        height=440,
        showlegend=False,
        hovermode="x unified",
        font=dict(family="Inter", color="#64748B", size=10),
    )
    for _ax in ("xaxis", "xaxis2"):
        _bt_fig.update_layout(**{_ax: dict(showgrid=False, showline=False,
                                           tickfont=dict(color="#64748B", size=10))})
    _bt_fig.update_layout(
        yaxis=dict(tickprefix="$", tickformat=",.0f", showgrid=True,
                   gridcolor="#E2E8F0", zeroline=False,
                   tickfont=dict(color="#F7931A", size=10)),
        yaxis2=dict(range=[0, 100], showgrid=True, gridcolor="#E2E8F0",
                    zeroline=False, tickfont=dict(color="#00D4FF", size=10)),
    )
    for ann in _bt_fig.layout.annotations:
        ann.font.color = "#94A3B8"
        ann.font.size  = 11

    st.plotly_chart(_bt_fig, use_container_width=True, config={"displayModeBar": False})

    # ── Insight tiles ────────────────────────────────────────────────────────
    _min_idx   = _fng_values.index(min(_fng_values))
    _min_val   = _fng_values[_min_idx]
    _min_date  = _fng_dates[_min_idx]
    _min_label = _min_date.strftime("%b %d, %Y")

    if _price_df is not None and not _price_df.empty:
        _bt_tmp = _price_df.copy()
        _bt_tmp["diff"] = (_bt_tmp["ts"] - _min_date).abs()
        _price_at_low  = _bt_tmp.loc[_bt_tmp["diff"].idxmin(), "price"]
        _price_today   = _price_df["price"].iloc[-1]
        _since_low_pct = ((_price_today / _price_at_low) - 1) * 100 if _price_at_low else None
    else:
        _price_at_low, _since_low_pct = None, None
    _since_col = "#10B981" if (_since_low_pct or 0) >= 0 else "#EF4444"

    _ef_days = sum(1 for v in _fng_values if v <= 25)

    _bt_cols = st.columns(3, gap="large")
    _bt_tiles = [
        ("Lowest Sentiment (30 days)",  str(_min_val),
         f"/ 100  ·  {_min_label}", fng_color(_min_val), ""),
        ("BTC Return Since Fear Low",
         f"{_since_low_pct:+.2f}%" if _since_low_pct is not None else "—",
         f"from ${_price_at_low:,.0f} on {_min_label}" if _price_at_low else "Price data unavailable",
         _since_col, ""),
        ("Extreme Fear Days (30 days)", str(_ef_days), "/ 30 days",
         "#EF4444" if _ef_days > 5 else "#10B981",
         "Historically strong accumulation zone"),
    ]
    for col, (lbl, val, sub, col_, note) in zip(_bt_cols, _bt_tiles):
        with col:
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">{lbl}</div>'
                f'<div class="oc-value" style="color:{col_}; font-size:28px;">{val}</div>'
                f'<div style="color:#64748B; font-size:11px; margin-top:4px;">{sub}</div>'
                + (f'<div style="color:#475569; font-size:11px; margin-top:6px;'
                   f' font-style:italic;">{note}</div>' if note else '')
                + '</div>',
                unsafe_allow_html=True,
            )

except Exception:
    st.markdown(
        '<div class="oc-tile" style="text-align:center; padding:48px 24px; color:#475569;">'
        '<div style="font-size:28px; margin-bottom:8px;">📈</div>'
        '<div style="font-size:14px;">Data loading — refresh in 5 minutes</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# WHALE ACTIVITY
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Whale Activity</div>', unsafe_allow_html=True)

if whale_txs is None:
    st.markdown(
        '<div class="oc-tile" style="text-align:center; padding:48px 24px; color:#475569;">'
        '<div style="font-size:28px; margin-bottom:8px;">🐋</div>'
        '<div style="font-size:14px;">Whale data unavailable — retrying next refresh</div>'
        '</div>',
        unsafe_allow_html=True,
    )
elif len(whale_txs) == 0:
    st.markdown(
        '<div class="oc-tile" style="text-align:center; padding:48px 24px; color:#475569;">'
        '<div style="font-size:28px; margin-bottom:8px;">🐋</div>'
        '<div style="font-size:14px;">No unconfirmed transactions over 10 BTC right now</div>'
        '</div>',
        unsafe_allow_html=True,
    )
else:
    _largest   = whale_txs[0]["btc"]
    _total_btc = sum(w["btc"] for w in whale_txs)
    _count     = len(whale_txs)
    _count_color = "#EF4444" if _count >= 20 else "#F97316" if _count >= 10 else "#10B981"

    # ── Summary tiles ────────────────────────────────────────────────────────
    _wh_cols = st.columns(3, gap="large")
    _wh_summary = [
        ("Largest Pending TX",  f"{_largest:,.2f}",  "BTC", "#F7931A"),
        ("Total Whale Volume",  f"{_total_btc:,.2f}", "BTC", "#94A3B8"),
        ("Whale TX Count",      str(_count),          f"of {_count} shown", _count_color),
    ]
    for col, (lbl, val, unit, col_) in zip(_wh_cols, _wh_summary):
        with col:
            st.markdown(
                f'<div class="oc-tile">'
                f'<div class="oc-label">{lbl}</div>'
                f'<div class="oc-value" style="color:{col_};">{val}'
                f'<span class="oc-unit">{unit}</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── Transaction table ────────────────────────────────────────────────────
    _hdr_cols = st.columns([3, 2, 2, 2], gap="small")
    for col, label in zip(_hdr_cols, ["TX Hash", "BTC Amount", "Inputs / Outputs", "Size"]):
        with col:
            st.markdown(
                f'<div style="color:#475569; font-size:11px; font-weight:700;'
                f' letter-spacing:1.5px; text-transform:uppercase; padding:4px 0;">{label}</div>',
                unsafe_allow_html=True,
            )

    for w in whale_txs:
        _btc = w["btc"]
        if _btc >= 100:
            _size_label, _size_color = "LARGE",    "#EF4444"
        elif _btc >= 50:
            _size_label, _size_color = "MEDIUM",   "#F97316"
        else:
            _size_label, _size_color = "STANDARD", "#94A3B8"

        _row = st.columns([3, 2, 2, 2], gap="small")
        with _row[0]:
            st.markdown(
                f'<div class="oc-tile" style="padding:10px 14px; font-family:monospace;'
                f' font-size:12px; color:#64748B;">{w["hash"]}</div>',
                unsafe_allow_html=True,
            )
        with _row[1]:
            st.markdown(
                f'<div class="oc-tile" style="padding:10px 14px;">'
                f'<span style="color:#F7931A; font-weight:700; font-size:13px;">{_btc:,.2f}</span>'
                f'<span style="color:#475569; font-size:11px;"> BTC</span></div>',
                unsafe_allow_html=True,
            )
        with _row[2]:
            st.markdown(
                f'<div class="oc-tile" style="padding:10px 14px; color:#94A3B8; font-size:12px;">'
                f'{w["inputs"]} in / {w["outputs"]} out</div>',
                unsafe_allow_html=True,
            )
        with _row[3]:
            st.markdown(
                f'<div class="oc-tile" style="padding:10px 14px;">'
                f'<span style="color:{_size_color}; font-size:11px; font-weight:700;'
                f' letter-spacing:1px;">{_size_label}</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="color:#475569; font-size:11px; margin-top:12px; text-align:right;">'
        'Showing unconfirmed BTC transactions over 10 BTC. Updates every 5 minutes.</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# WAITLIST
# ═══════════════════════════════════════════════════════════════════════════════
WAITLIST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "waitlist.csv")

def load_waitlist_count() -> int:
    if not os.path.exists(WAITLIST_FILE):
        return 0
    try:
        with open(WAITLIST_FILE, newline="", encoding="utf-8") as f:
            return max(0, sum(1 for row in csv.reader(f)) - 1)  # subtract header
    except Exception:
        return 0

def save_email(email: str) -> bool:
    """Append email + timestamp to CSV. Returns False if email already exists."""
    email = email.strip().lower()
    exists = False
    if os.path.exists(WAITLIST_FILE):
        try:
            with open(WAITLIST_FILE, newline="", encoding="utf-8") as f:
                exists = any(row[0] == email for row in csv.reader(f) if row)
        except Exception:
            pass
    if exists:
        return False
    write_header = not os.path.exists(WAITLIST_FILE)
    with open(WAITLIST_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["email", "timestamp"])
        w.writerow([email, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")])
    return True

st.markdown('<div class="section-header">Early Access</div>', unsafe_allow_html=True)

member_count = load_waitlist_count()

wl_left, wl_right = st.columns([3, 2], gap="large")

with wl_left:
    st.markdown("""
    <div class="waitlist-card">
        <div class="waitlist-headline">Get Early Access<br>to NeuroTrade</div>
        <div class="waitlist-sub">
            Join the waitlist and lock in founder pricing at
            <strong style="color:inherit;">$79&thinsp;/&thinsp;month</strong>
            for your first year. Regular price will be $99&thinsp;/&thinsp;month.
            Limited founding member spots available.
        </div>
        <p style="display:flex;align-items:center;gap:12px;margin:0 0 14px 0;
                  font-size:15px;color:inherit;font-weight:500;">
            <span style="width:22px;height:22px;border-radius:50%;flex-shrink:0;
                         background:linear-gradient(135deg,#00D4FF,#7C3AED);
                         display:inline-flex;align-items:center;justify-content:center;
                         font-size:11px;font-weight:700;color:#fff;">✓</span>
            Live AI intelligence score for BTC, ETH, SOL, XRP, ADA, AVAX, DOGE, DOT &amp; LINK
        </p>
        <p style="display:flex;align-items:center;gap:12px;margin:0 0 14px 0;
                  font-size:15px;color:inherit;font-weight:500;">
            <span style="width:22px;height:22px;border-radius:50%;flex-shrink:0;
                         background:linear-gradient(135deg,#00D4FF,#7C3AED);
                         display:inline-flex;align-items:center;justify-content:center;
                         font-size:11px;font-weight:700;color:#fff;">✓</span>
            On-chain metrics, sentiment and price signals combined
        </p>
        <p style="display:flex;align-items:center;gap:12px;margin:0;
                  font-size:15px;color:inherit;font-weight:500;">
            <span style="width:22px;height:22px;border-radius:50%;flex-shrink:0;
                         background:linear-gradient(135deg,#00D4FF,#7C3AED);
                         display:inline-flex;align-items:center;justify-content:center;
                         font-size:11px;font-weight:700;color:#fff;">✓</span>
            Email alerts when signals cross key thresholds
        </p>
    </div>
    """, unsafe_allow_html=True)

with wl_right:
    st.markdown("""
    <div style="height:3px; background:linear-gradient(90deg,#00D4FF,#7C3AED);
                border-radius:2px; margin-bottom:32px;"></div>
    """, unsafe_allow_html=True)

    # Success state stored in session
    if "waitlist_success" not in st.session_state:
        st.session_state.waitlist_success = False
    if "waitlist_duplicate" not in st.session_state:
        st.session_state.waitlist_duplicate = False

    if st.session_state.waitlist_success:
        st.markdown("""
        <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3);
                    border-radius:16px; padding:32px 28px; text-align:center;">
            <div style="font-size:36px; margin-bottom:12px;">🎉</div>
            <div style="font-size:20px; font-weight:800; color:#10B981;
                        margin-bottom:12px; letter-spacing:-0.3px;">
                You're on the list.
            </div>
            <div style="font-size:15px; color:#94A3B8; line-height:1.6;">
                Founding member pricing is locked for you.<br>
                We'll be in touch soon.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.waitlist_duplicate:
        st.markdown("""
        <div style="background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.25);
                    border-radius:16px; padding:24px 28px; text-align:center;
                    margin-bottom:16px;">
            <div style="font-size:15px; color:#EAB308; font-weight:600;">
                That email is already on the waitlist. We'll be in touch soon.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Try a different email", key="wl_reset",
                     use_container_width=True):
            st.session_state.waitlist_duplicate = False
            st.rerun()

    else:
        with st.form("waitlist_form", clear_on_submit=True):
            email_input = st.text_input(
                label="Email address",
                placeholder="Enter your email address",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button(
                "Join the Waitlist →",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            email_stripped = email_input.strip()
            if not email_stripped or "@" not in email_stripped:
                st.markdown("""
                <div style="color:#EF4444; font-size:13px; margin-top:8px;">
                    Please enter a valid email address.
                </div>
                """, unsafe_allow_html=True)
            else:
                added = save_email(email_stripped)
                if added:
                    st.session_state.waitlist_success = True
                    st.rerun()
                else:
                    st.session_state.waitlist_duplicate = True
                    st.rerun()

        st.markdown(f"""
        <div class="waitlist-urgency">
            Founding member pricing closes when we reach 150 subscribers
        </div>
        """, unsafe_allow_html=True)

    # Counter — always visible
    fresh_count = load_waitlist_count()
    st.markdown(f"""
    <div class="waitlist-counter-box">
        <div>
            <div class="waitlist-counter-num">{fresh_count}</div>
        </div>
        <div class="waitlist-counter-label">
            founding members so far<br>
            <span style="color:#334155; font-size:11px;">150 spots · {150 - fresh_count} remaining</span>
        </div>
        <div style="margin-left:auto;">
            <div style="width:80px; height:6px; background:#0B1120;
                        border-radius:999px; overflow:hidden; border:1px solid #334155;">
                <div style="width:{min(100, fresh_count / 150 * 100):.1f}%;
                            height:100%; border-radius:999px;
                            background:linear-gradient(90deg,#00D4FF,#7C3AED);">
                </div>
            </div>
            <div style="color:#334155; font-size:10px; margin-top:4px; text-align:right;">
                {min(100, fresh_count / 150 * 100):.0f}% full
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:60px; padding:20px 0; border-top:1px solid #1E293B;
            display:flex; justify-content:space-between; align-items:center;">
    <span style="color:#334155; font-size:12px;">
        Data: CoinGecko API &nbsp;·&nbsp; Alternative.me &nbsp;·&nbsp;
        Blockchain.com &nbsp;·&nbsp; Auto-refresh every 5 min
    </span>
    <span style="color:#334155; font-size:12px;">
        NeuroTrade © 2026 &nbsp;·&nbsp; For informational purposes only
    </span>
</div>
""", unsafe_allow_html=True)
