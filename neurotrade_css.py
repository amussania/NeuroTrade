"""
NeuroTrade Design System — CSS injection for Streamlit
Drop-in replacement for the st.markdown CSS block in app.py

DARK MODE TOKENS  → :root (default)
LIGHT MODE TOKENS → injected via st.session_state.theme == 'light'

Design language: Delisas-inspired SaaS dashboard
- Clean data density without clutter
- 12px card radius (down from 20px)
- Restrained typography (metric: 32px, not 64px)
- Soft shadows, no gradients on card surfaces
- Consistent 8px spacing grid
"""

NEUROTRADE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════
   DESIGN TOKENS — DARK MODE (default)
═══════════════════════════════════════════ */
:root {
    /* Backgrounds */
    --bg-base:              #0D1117;
    --bg-card:              #161B22;
    --bg-deep:              #0D1117;
    --bg-hover:             #1C2128;
    --bg-active:            #1A2E24;

    /* Borders */
    --border:               #30363D;
    --border-hover:         #484F58;
    --border-subtle:        #21262D;

    /* Text */
    --text-primary:         #F0F6FC;
    --text-secondary:       #C9D1D9;
    --text-muted:           #8B949E;
    --text-dim:             #6E7681;
    --text-very-dim:        #484F58;

    /* Brand accents */
    --accent-primary:       #10B981;
    --accent-primary-bg:    rgba(16, 185, 129, 0.10);
    --accent-primary-border:rgba(16, 185, 129, 0.25);
    --accent-blue:          #58A6FF;
    --accent-blue-bg:       rgba(88, 166, 255, 0.10);
    --accent-orange:        #F7931A;
    --accent-orange-bg:     rgba(247, 147, 26, 0.10);
    --accent-red:           #F85149;
    --accent-red-bg:        rgba(248, 81, 73, 0.10);
    --accent-yellow:        #E3B341;
    --accent-yellow-bg:     rgba(227, 179, 65, 0.10);

    /* Scrollbar */
    --scrollbar-track:      #0D1117;
    --scrollbar-thumb:      #30363D;

    /* Shadows */
    --shadow-card:          0 1px 3px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3);
    --shadow-hover:         0 4px 16px rgba(0,0,0,0.5), 0 2px 6px rgba(0,0,0,0.3);

    /* Legacy compat — keep old vars mapped */
    --section-hdr-color:    #8B949E;
    --section-hdr-border:   #21262D;
    --sub-grid-border:      #30363D;
    --input-bg:             #161B22;
    --input-color:          #C9D1D9;
    --input-border:         #30363D;
    --selectbox-bg:         #161B22;
    --selectbox-color:      #C9D1D9;
    --selectbox-border:     #30363D;
    --waitlist-bg:          linear-gradient(135deg, #0D1F35 0%, #13102A 100%);
    --waitlist-headline:    #F0F6FC;
    --waitlist-sub:         #8B949E;
    --waitlist-point:       #C9D1D9;
    --waitlist-counter-bg:  rgba(16,185,129,0.06);
    --waitlist-counter-bdr: rgba(16,185,129,0.20);
    --waitlist-counter-num: #10B981;
    --waitlist-counter-lbl: #6E7681;
}

/* ═══════════════════════════════════════════
   BASE
═══════════════════════════════════════════ */
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', system-ui, sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-secondary) !important;
}

.main > div { zoom: 0.90; }

/* Hide Streamlit chrome */
#MainMenu, footer, header            { visibility: hidden; }
[data-testid="stToolbar"]            { display: none !important; }
[data-testid="stDecoration"]         { display: none !important; }
[data-testid="stHeader"]             { background: transparent !important; }
[data-testid="stStatusWidget"]       { display: none !important; }

/* Scrollbar */
::-webkit-scrollbar                  { width: 4px; }
::-webkit-scrollbar-track            { background: var(--scrollbar-track); }
::-webkit-scrollbar-thumb            { background: var(--scrollbar-thumb); border-radius: 4px; }

/* ═══════════════════════════════════════════
   SECTION HEADERS
═══════════════════════════════════════════ */
.section-header {
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 36px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 14px;
    background: var(--accent-primary);
    border-radius: 2px;
    flex-shrink: 0;
}

/* ═══════════════════════════════════════════
   CARDS — unified base class
═══════════════════════════════════════════ */
.nt-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 20px 16px 20px;
    box-shadow: var(--shadow-card);
    transition: border-color 0.15s ease, box-shadow 0.2s ease;
}
.nt-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-hover);
}

/* ═══════════════════════════════════════════
   PRICE CARDS (replaces .price-card)
═══════════════════════════════════════════ */
.price-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px 12px 0 0;
    padding: 24px 24px 20px 24px;
    margin-bottom: 0;
    transition: border-color 0.15s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-card);
}
.price-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, var(--border));
    border-radius: 12px 12px 0 0;
}
.price-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-hover);
}

.coin-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-dim);
}
.coin-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}

/* ── Toned-down metric size (was 64px) ── */
.coin-price {
    font-size: 36px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -1px;
    line-height: 1.1;
    margin: 4px 0 10px 0;
    font-variant-numeric: tabular-nums;
}

.change-pos {
    color: var(--accent-primary);
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--accent-primary-bg);
    border: 1px solid var(--accent-primary-border);
    padding: 2px 8px;
    border-radius: 20px;
}
.change-neg {
    color: var(--accent-red);
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--accent-red-bg);
    border: 1px solid rgba(248,81,73,0.25);
    padding: 2px 8px;
    border-radius: 20px;
}

.sub-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border-subtle);
}
.sub-item-label {
    color: var(--text-dim);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.sub-item-value {
    color: var(--text-muted);
    font-size: 15px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}

/* ═══════════════════════════════════════════
   ON-CHAIN TILES (replaces .oc-tile)
═══════════════════════════════════════════ */
.oc-tile {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px 14px 18px;
    transition: border-color 0.15s ease;
    box-shadow: var(--shadow-card);
}
.oc-tile:hover { border-color: var(--border-hover); }

.oc-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-dim);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.oc-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    line-height: 1.1;
    font-variant-numeric: tabular-nums;
}
.oc-unit {
    font-size: 13px;
    color: var(--text-dim);
    font-weight: 500;
    margin-left: 3px;
}

/* ═══════════════════════════════════════════
   INTELLIGENCE SCORE CARD
═══════════════════════════════════════════ */
.intel-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 28px 20px 28px;
    margin: 4px 0;
    box-shadow: var(--shadow-card);
}
.intel-score-number {
    font-size: 72px;
    font-weight: 800;
    letter-spacing: -3px;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.intel-label {
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin-top: 6px;
}
.intel-explanation {
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 400;
    margin-top: 10px;
    line-height: 1.6;
}
.intel-bar-track {
    background: var(--bg-deep);
    border-radius: 999px;
    height: 8px;
    margin: 16px 0 6px 0;
    overflow: hidden;
    border: 1px solid var(--border-subtle);
}
.intel-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s ease;
}
.intel-component { display: flex; flex-direction: column; gap: 4px; }
.intel-comp-label {
    color: var(--text-dim);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.intel-comp-bar-track {
    background: var(--bg-deep);
    border-radius: 999px;
    height: 4px;
    overflow: hidden;
}
.intel-comp-bar-fill {
    height: 100%;
    border-radius: 999px;
}
.intel-comp-value {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
    margin-top: 1px;
}

/* ═══════════════════════════════════════════
   STATUS BADGES
═══════════════════════════════════════════ */
.badge {
    display: inline-flex;
    align-items: center;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.badge--positive { background: var(--accent-primary-bg); color: var(--accent-primary); border: 1px solid var(--accent-primary-border); }
.badge--negative { background: var(--accent-red-bg);     color: var(--accent-red);     border: 1px solid rgba(248,81,73,0.25); }
.badge--neutral  { background: var(--bg-hover);          color: var(--text-muted);     border: 1px solid var(--border); }
.badge--warning  { background: var(--accent-yellow-bg);  color: var(--accent-yellow);  border: 1px solid rgba(227,179,65,0.25); }

/* ═══════════════════════════════════════════
   LIVE DOT
═══════════════════════════════════════════ */
@keyframes pulse {
    0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(16,185,129,0.4); }
    50%      { opacity:0.7; box-shadow: 0 0 0 5px rgba(16,185,129,0); }
}
.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: var(--accent-primary);
    border-radius: 50%;
    margin-right: 5px;
    animation: pulse 2.5s infinite;
    flex-shrink: 0;
}

/* ═══════════════════════════════════════════
   CHART CONTAINER
═══════════════════════════════════════════ */
.chart-wrap {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 4px;
    overflow: hidden;
}

/* ═══════════════════════════════════════════
   FEAR & GREED
═══════════════════════════════════════════ */
.fng-label-big {
    text-align: center;
    font-size: 22px;
    font-weight: 800;
    margin-top: -6px;
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}
.fng-sub {
    text-align: center;
    color: var(--text-dim);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.subsection-label {
    color: var(--text-dim);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 20px 0 10px 0;
}

/* ═══════════════════════════════════════════
   WAITLIST
═══════════════════════════════════════════ */
.waitlist-card {
    background: var(--waitlist-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 40px 44px;
    position: relative;
    overflow: hidden;
}
.waitlist-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-primary) 0%, #7C3AED 50%, var(--accent-orange) 100%);
    border-radius: 12px 12px 0 0;
}
.waitlist-headline {
    font-size: 28px;
    font-weight: 800;
    color: var(--waitlist-headline);
    letter-spacing: -0.7px;
    line-height: 1.15;
    margin-bottom: 12px;
}
.waitlist-sub {
    font-size: 14px;
    color: var(--waitlist-sub);
    line-height: 1.7;
    margin-bottom: 24px;
    max-width: 480px;
}
.waitlist-value-point {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 12px;
    font-size: 14px;
    color: var(--waitlist-point);
    font-weight: 500;
}
.waitlist-check {
    width: 18px; height: 18px;
    background: var(--accent-primary);
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
    font-size: 10px;
    color: #FFFFFF;
    font-weight: 700;
}
.waitlist-counter-box {
    background: var(--waitlist-counter-bg);
    border: 1px solid var(--waitlist-counter-bdr);
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.waitlist-counter-num {
    font-size: 28px;
    font-weight: 800;
    color: var(--waitlist-counter-num);
    letter-spacing: -1px;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.waitlist-counter-label {
    color: var(--waitlist-counter-lbl);
    font-size: 12px;
    font-weight: 500;
    line-height: 1.5;
}
.waitlist-urgency {
    color: var(--text-dim);
    font-size: 11px;
    font-weight: 500;
    text-align: center;
    margin-top: 10px;
}

/* ═══════════════════════════════════════════
   STREAMLIT COMPONENT OVERRIDES
═══════════════════════════════════════════ */

/* Selectbox */
[data-testid="stSelectbox"] > div > div,
div[data-baseweb="select"] > div {
    background-color: var(--selectbox-bg) !important;
    color: var(--selectbox-color) !important;
    border-color: var(--selectbox-border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
div[data-baseweb="select"] * { color: var(--selectbox-color) !important; font-family: 'DM Sans', sans-serif !important; }
div[data-baseweb="select"] svg { fill: var(--text-dim) !important; }
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: var(--shadow-hover) !important;
}
div[data-baseweb="option"] {
    background-color: var(--bg-card) !important;
    color: var(--selectbox-color) !important;
    font-size: 13px !important;
}
div[data-baseweb="option"]:hover { background-color: var(--bg-hover) !important; }
li[role="option"] {
    background-color: var(--bg-card) !important;
    color: var(--selectbox-color) !important;
}
li[role="option"]:hover { background-color: var(--bg-hover) !important; }

/* Text input */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextInput"] > div > div {
    background-color: var(--input-bg) !important;
    color: var(--input-color) !important;
    border-color: var(--input-border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stTextInput"] > div > div > input::placeholder {
    color: var(--text-dim) !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px var(--accent-primary-bg) !important;
}

/* Primary button */
[data-testid="stFormSubmitButton"] > button,
div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--accent-primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    padding: 10px 20px !important;
    transition: background 0.15s ease, box-shadow 0.15s ease !important;
}
[data-testid="stFormSubmitButton"] > button:hover,
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #059669 !important;
    box-shadow: 0 4px 12px rgba(16,185,129,0.3) !important;
}

/* Secondary / default button */
div[data-testid="stButton"] > button {
    background: var(--bg-hover) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: border-color 0.15s ease, background 0.15s ease !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--border-hover) !important;
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

/* Form container */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Expander */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-muted) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Spinner */
[data-testid="stSpinner"] { color: var(--accent-primary) !important; }

/* Metric — if used */
[data-testid="stMetric"] label {
    color: var(--text-dim) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* ═══════════════════════════════════════════
   MONO FONT — tx hashes, code values
═══════════════════════════════════════════ */
.mono {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 0;
}

/* ═══════════════════════════════════════════
   UTILITY CLASSES
═══════════════════════════════════════════ */
.text-primary   { color: var(--text-primary) !important; }
.text-secondary { color: var(--text-secondary) !important; }
.text-muted     { color: var(--text-muted) !important; }
.text-dim       { color: var(--text-dim) !important; }
.text-green     { color: var(--accent-primary) !important; }
.text-red       { color: var(--accent-red) !important; }
.text-orange    { color: var(--accent-orange) !important; }
.text-blue      { color: var(--accent-blue) !important; }

.mt-4  { margin-top: 4px; }
.mt-8  { margin-top: 8px; }
.mt-12 { margin-top: 12px; }
.mt-16 { margin-top: 16px; }
.mt-24 { margin-top: 24px; }
</style>
"""

NEUROTRADE_LIGHT_CSS = """
<style>
:root {
    /* Backgrounds */
    --bg-base:              #F3F6FA;
    --bg-card:              #FFFFFF;
    --bg-deep:              #E8EDF4;
    --bg-hover:             #F0F4F9;
    --bg-active:            #EEF9F5;

    /* Borders */
    --border:               #D1D9E0;
    --border-hover:         #A8B3BE;
    --border-subtle:        #E1E8EF;

    /* Text */
    --text-primary:         #0D1117;
    --text-secondary:       #24292F;
    --text-muted:           #57606A;
    --text-dim:             #6E7781;
    --text-very-dim:        #8C959F;

    /* Brand accents — same hues, lighter contexts */
    --accent-primary:       #1A7F64;
    --accent-primary-bg:    rgba(26, 127, 100, 0.08);
    --accent-primary-border:rgba(26, 127, 100, 0.20);
    --accent-blue:          #0969DA;
    --accent-blue-bg:       rgba(9, 105, 218, 0.08);
    --accent-orange:        #BF5B00;
    --accent-orange-bg:     rgba(191, 91, 0, 0.08);
    --accent-red:           #CF222E;
    --accent-red-bg:        rgba(207, 34, 46, 0.08);
    --accent-yellow:        #9A6700;
    --accent-yellow-bg:     rgba(154, 103, 0, 0.08);

    /* Scrollbar */
    --scrollbar-track:      #F3F6FA;
    --scrollbar-thumb:      #D1D9E0;

    /* Shadows */
    --shadow-card:          0 1px 3px rgba(27,31,36,0.06), 0 1px 2px rgba(27,31,36,0.04);
    --shadow-hover:         0 4px 12px rgba(27,31,36,0.10), 0 2px 4px rgba(27,31,36,0.06);

    /* Legacy compat */
    --section-hdr-color:    #57606A;
    --section-hdr-border:   #E1E8EF;
    --sub-grid-border:      #D1D9E0;
    --input-bg:             #FFFFFF;
    --input-color:          #0D1117;
    --input-border:         #D1D9E0;
    --selectbox-bg:         #FFFFFF;
    --selectbox-color:      #0D1117;
    --selectbox-border:     #D1D9E0;
    --waitlist-bg:          linear-gradient(135deg, #EBF4FF 0%, #F0E6FF 100%);
    --waitlist-headline:    #0D1117;
    --waitlist-sub:         #57606A;
    --waitlist-point:       #24292F;
    --waitlist-counter-bg:  rgba(26,127,100,0.06);
    --waitlist-counter-bdr: rgba(26,127,100,0.18);
    --waitlist-counter-num: #1A7F64;
    --waitlist-counter-lbl: #6E7781;
}

html, body, [class*="css"], .stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-secondary) !important;
}
</style>
"""
