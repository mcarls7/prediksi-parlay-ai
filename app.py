import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

# --- KONFIGURASI FINAL: ELANGBOLA AI (prediksibola.id) ---
st.set_page_config(page_title="ELANGBOLA AI - prediksibola.id", page_icon="🦅", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { background-color: #0f172a; border: 1px solid #d4af37; padding: 15px; border-radius: 12px; color: #d4af37; }
    
    /* STYLE TIKET EXCLUSIVE ELANGBOLA */
    .ticket-elang { 
        background-color: #ffffff; 
        color: #000000; 
        padding: 30px; 
        border-radius: 8px; 
        font-family: 'Courier New', monospace; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.6); 
        border-top: 15px solid #1b5e20; 
        border-bottom: 8px solid #1b5e20;
    }
    .slogan { 
        color: #1b5e20; 
        font-weight: bold; 
        font-style: italic; 
        font-size: 16px; 
        margin-top: 15px; 
        border-top: 1px dashed #ccc;
        padding-top: 10px;
    }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e293b; 
        border-radius: 5px; 
        color: white; 
        padding: 10px 25px; 
        font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state: st.session_state.messages = []
if "matches" not in st.session_state: st.session_state.matches = []
if "parlay" not in st.session_state: st.session_state.parlay = None
if "history" not in st.session_state: st.session_state.history = []

# --- SIDEBAR: EXECUTIVE CONTROL ---
st.sidebar.title("🦅 ELANGBOLA AI")
st.sidebar.caption("Official: prediksibola.id")
api_key = st.sidebar.text_input("The Odds API Key", type="password")
bankroll = st.sidebar.number_input("Whale Bankroll (Rp)", value=1000000, step=100000)

if st.session_state.history:
    df_h = pd.DataFrame(st.session_state.history)
    st.sidebar.markdown("---")
    profit = df_h['Profit'].sum()
    st.sidebar.metric("NET PROFIT", f"Rp {profit:,}", delta=f"{profit:,}")
    win_rate = (df_h['Status'] == 'WIN').sum() / len(df_h) * 100
    st.sidebar.write(f"**Win Rate:** {win_rate:.1f}%\")

# --- CORE LOGIC ---
def scan_global(key):
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={key}&regions=eu&markets=h2h"
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- UI LAYOUT ---
st.title("🤖 ELANGBOLA AI - prediksibola.id")

t1, t2, t3, t4 = st.tabs(["💬 ANALISIS CHAT", "🌍 MARKET SCANNER", "📊 DATA PNL", "🛡️ RISK MANAGEMENT"])

with t1:
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.subheader("💬 AI Betting Consultant")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("Tanya prediksi parlay jitu..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                if st.session_state.matches:
                    picks = random.sample(st.session_state.matches, min(3, len(st.session_state.matches)))
                    total_odds = 1.0
                    for p in picks: total_odds *= p['Odds']
                    
                    response = f"### 🦅 ELANGBOLA VIP ANALYSIS\n"
                    for i, p in enumerate(picks):
                        response += f"{i+1}. **{p['Match']}**\n   - Pick: `{p['Pick']}` (@{p['Odds']})\n"
                    
                    response += f"\n**🎯 TOTAL ODDS: {total_odds:.2f}x**\n"
                    response += f"**🔥 Sehati Gas! Ragu Skip!**"
                    st.session_state.parlay = {"picks": picks, "total": total_odds}
                else:
                    response = "Data market kosong. Scan dulu di tab **MARKET SCANNER**!"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    with c2:
        if st.session_state.parlay:
            st.subheader("🎫 Struk Resmi")
            ticket_items = "".join([f"• {x['Match']}<br>&nbsp;&nbsp;<b>{x['Pick']} @{x['Odds']}</b><br>" for x in st.session_state.parlay['picks']])
            st.markdown(f"""
                <div class="ticket-elang">
                    <center>
                        <b style="font-size: 24px;">🦅 ELANGBOLA AI</b><br>
                        <small>prediksibola.id | {datetime.now().strftime('%d %B %Y')}</small>
                    </center>
                    <hr style="border: 1px dashed #000;">
                    {ticket_items}
                    <hr style="border: 1px dashed #000;">
                    <b style="font-size: 20px;">TOTAL ODDS: {st.session_state.parlay['total']:.2f}x</b>
                    <center><div class="slogan">"Sehati Gas! Ragu Skip!"</div></center>
                </div>
                """, unsafe_allow_html=True)
            if st.button("📥 SIMPAN KE DATABASE"):
                st.session_state.history.append({
                    "Jam": datetime.now().strftime('%H:%M'),
                    "Legs": f"{len(st.session_state.parlay['picks'])} Tim",
                    "Odds": round(st.session_state.parlay['total'], 2),
                    "Stake": 100000,
                    "Status": "PENDING",
                    "Profit": 0,
                    "CumProfit": (st.session_state.history[-1]["CumProfit"] if st.session_state.history else 0)
                })
                st.success("Tiket Berhasil Dicatat!")

with t2:
    st.subheader("🌍 Multi-League Radar")
    if st.button("🔎 JALANKAN SCANNER"):
        if api_key:
            with st.spinner("Memindai bursa taruhan..."):
                data = scan_global(api_key)
                if data:
                    processed = []
                    for m in data:
                        for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                            if o['price'] >= 1.80:
                                processed.append({"Match": f"{m['home_team']} vs {m['away_team']}", "Pick": o['name'], "Odds": o['price']})
                    st.session_state.matches = processed
                    st.success("Database Updated!")
        else: st.warning("Masukkan API Key!")
    
    if st.session_state.matches:
        st.dataframe(pd.DataFrame(st.session_state.matches), use_container_width=True)

with t3:
    st.subheader("📈 Performance Analytic")
    if st.session_state.history:
        df_log = pd.DataFrame(st.session_state.history)
        st.markdown("---")
        idx_upd = st.number_input("Index Tiket", min_value=0, max_value=len(st.session_state.history)-1)
        res_upd = st.selectbox("Update Status", ["WIN", "LOSE"])
        if st.button("CONFIRM UPDATE"):
            st.session_state.history[idx_upd]["Status"] = res_upd
            s, o = st.session_state.history[idx_upd]["Stake"], st.session_state.history[idx_upd]["Odds"]
            profit = (s * o) - s if res_upd == "WIN" else -s
            st.session_state.history[idx_upd]["Profit"] = profit
            cp = 0
            for i in range(len(st.session_state.history)):
                cp += st.session_state.history[i]["Profit"]
                st.session_state.history[i]["CumProfit"] = cp
            st.rerun()
        st.table(df_log)
    else: st.info("Belum ada data.")

with t4:
    st.subheader("🛡️ Professional Risk Management")
    c1, c2 = st.columns(2)
    c1.metric("Total Saldo", f"Rp {bankroll:,}")
    c2.info(f"💡 **Saran Bet Aman:** Rp {bankroll * 0.05:,.0f} (5%)")

st.markdown("---")
st.caption("© 2026 prediksibola.id | ELANGBOLA AI | Sehati Gas! Ragu Skip!")
    
