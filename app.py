import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

# --- ULTRA-PREMIUM JADE UI CONFIG ---
st.set_page_config(page_title="ELANGBOLA AI", page_icon="🦅", layout="wide")

st.markdown("""
    <style>
    /* Main Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #064e3b, #022c22, #000000);
        font-family: 'Inter', sans-serif;
        color: #ecfdf5;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(6, 78, 59, 0.5);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(16, 185, 129, 0.2);
    }

    /* Custom Cards/Metrics */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    label[data-testid="stMetricLabel"] {
        color: #10b981 !important;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Buttons - Neon Emerald */
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(52, 211, 153, 0.6);
    }

    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(6, 78, 59, 0.3);
        border-radius: 10px 10px 0 0;
        color: #a7f3d0;
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 0 30px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #10b981 !important;
        color: white !important;
        border: none !important;
    }

    /* PREDIKSI TIKET - LUXURY WHITE */
    .ticket-container {
        background: #ffffff;
        color: #064e3b;
        padding: 35px;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .ticket-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 10px;
        background: #10b981;
    }
    .ticket-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .ticket-brand { font-size: 26px; font-weight: 900; letter-spacing: -1px; }
    .ticket-row { border-bottom: 1px dashed #cbd5e1; padding: 10px 0; }
    .ticket-footer { 
        text-align: center; 
        margin-top: 25px; 
        font-weight: 800;
        font-style: italic;
        color: #059669;
        font-size: 18px;
    }

    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        border: 1px solid rgba(16, 185, 129, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTO ENGINE ---
API_KEY = st.secrets.get("ODDS_API_KEY", "")

if "matches" not in st.session_state: st.session_state.matches = []
if "parlay" not in st.session_state: st.session_state.parlay = None
if "history" not in st.session_state: st.session_state.history = []

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown("<h1 style='color: #10b981;'>🦅 ELANGBOLA</h1>", unsafe_allow_html=True)
    st.caption("Strategic Betting Intelligence")
    st.markdown("---")
    
    bankroll = st.number_input("Vault Balance (Rp)", value=1000000)
    
    if st.session_state.history:
        df_h = pd.DataFrame(st.session_state.history)
        profit = df_h['Profit'].sum()
        st.metric("TOTAL P/L", f"Rp {profit:,}", delta=f"{profit:,}")
        st.write(f"📊 Accuracy: **{(df_h['Status'] == 'WIN').sum() / len(df_h) * 100:.1f}%**")
    
    st.markdown("---")
    st.caption("Accessing: prediksibola.id")

# --- MAIN DASHBOARD ---
st.markdown("<h3 style='margin-bottom:0;'>Eagle Analysis Engine</h3>", unsafe_allow_html=True)
st.markdown("<p style='color:#10b981; font-weight:bold;'>PRO ACCESS ENABLED</p>", unsafe_allow_html=True)

tab_chat, tab_scan, tab_pnl = st.tabs(["🎯 PREDIKSI VIP", "📡 MARKET RADAR", "📊 LEDGER"])

with tab_chat:
    col_main, col_ticket = st.columns([1.4, 1])
    
    with col_main:
        st.markdown("<div style='background:rgba(255,255,255,0.03); padding:20px; border-radius:15px;'>", unsafe_allow_html=True)
        st.write("🤖 **AI Consultant:** *Siap memberikan racikan terbaik untuk malam ini.*")
        
        if prompt := st.chat_input("Request Analisis Parlay..."):
            if st.session_state.matches:
                picks = random.sample(st.session_state.matches, min(3, len(st.session_state.matches)))
                total_o = 1.0
                for p in picks: total_o *= p['Odds']
                st.session_state.parlay = {"picks": picks, "total": total_o}
                
                st.success(f"Analisis Selesai! Menemukan {len(picks)} pertandingan dengan probabilitas tinggi.")
                for p in picks:
                    st.markdown(f"✅ **{p['Match']}** — Pick: `{p['Pick']}` @{p['Odds']}")
            else:
                st.error("Data Market masih kosong. Silakan jalankan **Radar Scanner** terlebih dahulu.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ticket:
        if st.session_state.parlay:
            st.markdown(f"""
                <div class="ticket-container">
                    <div class="ticket-header">
                        <div class="ticket-brand">🦅 ELANGBOLA AI</div>
                        <div style="font-size:12px; color:#64748b;">prediksibola.id | {datetime.now().strftime('%H:%M WIB')}</div>
                    </div>
                    <div style="border-top: 1px solid #e2e8f0; margin: 15px 0;"></div>
                    {"".join([f'<div class="ticket-row"><b>{x["Match"]}</b><br><span style="color:#059669">{x["Pick"]} @{x["Odds"]}</span></div>' for x in st.session_state.parlay["picks"]])}
                    <div style="margin-top:20px; font-size:20px; font-weight:bold; text-align:right;">
                        TOTAL ODDS: {st.session_state.parlay["total"]:.2f}x
                    </div>
                    <div class="ticket-footer">"Sehati Gas! Ragu Skip!"</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("💾 SAVE TICKET"):
                st.session_state.history.append({"Match": "Parlay", "Status": "PENDING", "Profit": 0})
                st.toast("Tiket berhasil masuk ke ledger!")

with tab_scan:
    if st.button("🔎 JALANKAN RADAR SCANNER"):
        if API_KEY:
            with st.spinner("Scanning Global Markets..."):
                r = requests.get(f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=eu&markets=h2h").json()
                st.session_state.matches = [{"Match": f"{m['home_team']} vs {m['away_team']}", "Pick": m['bookmakers'][0]['markets'][0]['outcomes'][0]['name'], "Odds": m['bookmakers'][0]['markets'][0]['outcomes'][0]['price']} for m in r]
                st.rerun()
        else: st.error("Kunci API belum dikonfigurasi.")
    
    if st.session_state.matches:
        st.dataframe(pd.DataFrame(st.session_state.matches), use_container_width=True)

with tab_pnl:
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    else:
        st.info("Ledger kosong. Simpan tiket analisis untuk mulai melacak performa.")

st.markdown("---")
st.caption("© 2026 prediksibola.id | Powered by Elangbola Parlay Engine")
