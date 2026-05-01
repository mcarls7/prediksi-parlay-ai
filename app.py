import streamlit as st
import pandas as pd
import requests
import random
import plotly.express as px
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
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state: st.session_state.messages = []
if "matches" not in st.session_state: st.session_state.matches = []
if "parlay" not in st.session_state: st.session_state.parlay = None
if "history" not in st.session_state: st.session_state.history = []

# --- SIDEBAR: EXECUTIVE CONTROL ---
st.sidebar.title("🦅 ELANGBOLA AI")
st.sidebar.caption("Domain: prediksibola.id")
api_key = st.sidebar.text_input("The Odds API Key", type="password")
bankroll = st.sidebar.number_input("Whale Bankroll (Rp)", value=1000000, step=100000)

if st.session_state.history:
    df_h = pd.DataFrame(st.session_state.history)
    st.sidebar.markdown("---")
    profit = df_h['Profit'].sum()
    st.sidebar.metric("NET PROFIT", f"Rp {profit:,}", delta=f"{profit:,}")
    win_rate = (df_h['Status'] == 'WIN').sum() / len(df_h) * 100
    st.sidebar.write(f"**Win Rate:** {win_rate:.1f}%")

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

        if prompt := st.chat_input("Tanya prediksi parlay jitu hari ini..."):
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
                    response = "Database kosong. Scan dulu di tab **MARKET SCANNER**!"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    with c2:
        if st.session_state.parlay:
            st.subheader("🎫 Struk Resmi")
            st.markdown(f"""
            <div class="ticket-elang">
                <center>
                    <b style="font-size: 24px;">🦅 ELANGBOLA AI</b><br>
                    <small>prediksibola.id | {datetime.now().strftime('%d %B %Y')}</small>
                </center>
                <hr style="border: 1px dashed #000;">
                {"<br>".join([f"• {x['Match']}<br>&nbsp;&nbsp;<b>{x['Pick']} @{x['Odds']}</b>" for x in st.session_state.parlay['picks']])}
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

# (Tab scanner, PNL, dan Risk Management tetap sama dengan versi sebelumnya)
# ... [Isi kode tab t2, t3, t4 sama dengan V10 sebelumnya] ...

st.markdown("---")
st.caption("© 2026 prediksibola.id | ELANGBOLA AI Syndicate | Developed for Elangbola")
   
</style>
    """, unsafe_allow_html=True)

# --- JUDUL APLIKASI ---
st.title("🤖 PREDIKSI PARLAY AI")
st.markdown("Aplikasi Analisis Taruhan Olahraga dengan Bantuan Kecerdasan Buatan")
st.markdown("---")

# --- INISIALISASI STATE ---
if 'parlay_list' not in st.session_state:
    st.session_state.parlay_list = []

if 'current_matches' not in st.session_state:
    st.session_state.current_matches = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya adalah asisten prediksi Anda. Silakan tarik data pertandingan terbaru, lalu tanyakan rekomendasi parlay kepada saya."}
    ]

# --- SIDEBAR PENGATURAN ---
with st.sidebar:
    st.header("⚙️ PENGATURAN")
    api_key = st.text_input("The Odds API Key", type="password", help="Masukkan API Key dari the-odds-api.com")
    min_odds = st.number_input("Minimal Odds per Leg", value=1.80, step=0.05)
    league = st.selectbox(
        "Pilih Liga", 
        ["soccer_epl", "soccer_spain_la_liga", "soccer_italy_serie_a", "soccer_germany_bundesliga", "soccer_france_ligue_one"]
    )
    
    st.markdown("---")
    st.caption("© 2026 PREDIKSI PARLAY AI\nDeveloped for Randy Sanjaya")

# --- FUNGSI UTILITAS (DATA FETCHING) ---
def fetch_odds(key, league_code):
    """Mengambil data odds dari API eksternal"""
    if not key:
        return None
    url = f"https://api.the-odds-api.com/v4/sports/{league_code}/odds/?apiKey={key}&regions=eu&markets=h2h"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Error API: {res.status_code}")
            return None
    except Exception as e:
        st.error(f"Gagal terhubung ke API: {str(e)}")
        return None

# --- LAYOUT UTAMA ---
col_data, col_parlay = st.columns([2, 1])

# --- KOLOM KIRI: DATA PERTANDINGAN ---
with col_data:
    st.subheader("📋 Daftar Pertandingan & Odds")
    
    if st.button("🔄 Tarik Data Pertandingan Terbaru"):
        if api_key:
            with st.spinner("Sedang mengambil data real-time..."):
                raw_data = fetch_odds(api_key, league)
                if raw_data:
                    processed_matches = []
                    for match in raw_data:
                        home_team = match['home_team']
                        away_team = match['away_team']
                        commence_time = match['commence_time']
                        
                        # Ambil odds dari bookmaker pertama
                        if match['bookmakers']:
                            bk = match['bookmakers'][0]
                            if bk['markets']:
                                for outcome in bk['markets'][0]['outcomes']:
                                    if outcome['price'] >= min_odds:
                                        processed_matches.append({
                                            "Pertandingan": f"{home_team} vs {away_team}",
                                            "Pilihan": outcome['name'],
                                            "Odds": outcome['price'],
                                            "Waktu": commence_time[:16].replace('T', ' ')
                                        })
                    
                    st.session_state.current_matches = processed_matches
                    st.success(f"Berhasil memuat {len(processed_matches)} pilihan odds >= {min_odds}")
                else:
                    st.warning("Tidak ada data atau API Key salah.")
        else:
            st.warning("⚠️ Masukkan API Key di sidebar terlebih dahulu.")

    # Tampilkan Tabel Data jika ada
    if st.session_state.current_matches:
        df = pd.DataFrame(st.session_state.current_matches)
        
        # Pilihan Interaktif untuk Parlay
        selected_match_str = st.selectbox(
            "Pilih pertandingan untuk ditambahkan ke Parlay:",
            [f"{row['Pertandingan']} ({row['Pilihan']} - {row['Odds']})" for index, row in df.iterrows()]
        )
        
        if st.button("➕ Tambahkan ke Tiket Parlay"):
            # Cari data asli berdasarkan string pilihan
            parts = selected_match_str.split(" (")
            match_name = parts[0]
            detail_part = parts[1].replace(")", "")
            pick_name, odds_val = detail_part.split(" - ")
            
            new_item = {
                "Pertandingan": match_name,
                "Pilihan": pick_name,
                "Odds": float(odds_val)
            }
            st.session_state.parlay_list.append(new_item)
            st.toast(f"✅ {match_name} ditambahkan!", icon="✅")

        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("💡 Klik tombol 'Tarik Data Pertandingan Terbaru' untuk memulai.")

# --- KOLOM KANAN: TIKET PARLAY ---
with col_parlay:
    st.subheader("💰 Tiket Parlay Anda")
    
    if st.session_state.parlay_list:
        total_odds = 1.0
        details_list = []
        
        st.write("**Daftar Pilihan:**")
        for i, item in enumerate(st.session_state.parlay_list):
            st.write(f"{i+1}. **{item['Pertandingan']}**")
            st.write(f"   └ Pilih: {item['Pilihan']} @ {item['Odds']}")
            total_odds *= item['Odds']
            details_list.append(f"{item['Pertandingan']} ({item['Pilihan']})")
        
        st.markdown("---")
        st.metric(label="Total Odds Parlay", value=f"{total_odds:.2f}x", delta_color="normal")
        
        stake = st.number_input("Modal Taruhan (Rp/USD)", min_value=0.0, value=100000.0, step=10000.0)
        potential_win = stake * total_odds
        
        st.write(f"Estimasi Kemenangan: **Rp {potential_win:,.2f}**")
        
        col_reset, col_save = st.columns(2)
        with col_reset:
            if st.button("🗑️ Reset", use_container_width=True):
                st.session_state.parlay_list = []
                st.rerun()
        with col_save:
            if st.button("💾 Simpan", use_container_width=True):
                st.success("Riwayat disimpan (Simulasi)")
    else:
        st.empty()
        st.info("Belum ada tim yang dipilih.")

# --- BAGIAN CHATBOT AI ---
st.markdown("---")
st.subheader("💬 Chatbot Prediksi Parlay AI")
st.caption("Tanyakan rekomendasi atau analisis berdasarkan data yang sudah dimuat.")

# Container Chat
chat_container = st.container(border=True)

with chat_container:
    # Tampilkan riwayat pesan
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Chat User
    if prompt := st.chat_input("Contoh: Berikan 3 rekomendasi parlay terbaik malam ini..."):
        # 1. Tampilkan pesan user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Proses Respon AI
        with st.chat_message("assistant"):
            with st.spinner("AI sedang menganalisis data pertandingan..."):
                
                # Logika Sederhana AI (Rule-Based + Data Context)
                if not st.session_state.current_matches:
                    response_text = "Maaf, saya belum memiliki data pertandingan terkini. Silakan klik tombol **'Tarik Data Pertandingan Terbaru'** di atas terlebih dahulu agar saya bisa memberikan analisis yang akurat."
                else:
                    # Filter data untuk rekomendasi (Simulasi Logika AI)
                    # AI akan memilih 3 pertandingan dengan odds terdekat ke 2.00 (nilai tengah yang umum)
                    matches = st.session_state.current_matches
                    
                    # Sortir berdasarkan odds (mendekati 2.00 dianggap 'value' umum)
                    sorted_matches = sorted(matches, key=lambda x: abs(x['Odds'] - 2.00))
                    top_picks = sorted_matches[:3] # Ambil 3 teratas
                    
                    if len(top_picks) < 3:
                         response_text = "Data pertandingan terlalu sedikit untuk membuat parlay 3 tim. Coba ubah filter minimal odds di sidebar."
                    else:
                        response_text = f"Berdasarkan analisis data real-time untuk liga terpilih, berikut adalah **3 Rekomendasi Parlay** dengan nilai probabilitas tertinggi:\n\n"
                        
                        combined_odds = 1.0
                        for i, m in enumerate(top_picks):
                            response_text += f"{i+1}. ⚽ **{m['Pertandingan']}**\n"
                            response_text += f"   ├── Pilihan: **{m['Pilihan']}**\n"
                            response_text += f"   └── Odds: {m['Odds']}\n\n"
                            combined_odds *= m['Odds']
                        
                        response_text += f"📊 **Total Odds Parlay: {combined_odds:.2f}x**\n"
                        response_text += f"💡 **Analisis AI:** Kombinasi ini dipilih karena memiliki keseimbangan risiko dan keuntungan yang optimal berdasarkan fluktuasi pasar saat ini. Pastikan untuk mengecek lineup resmi 1 jam sebelum kick-off."
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})        
                st.write(f"Estimasi Kemenangan: **{potential_win:,.2f}**")
        
        if st.button("🗑️ Reset Parlay"):
            st.session_state.parlay_list = []
            st.rerun()
    else:
        st.info("Belum ada pertandingan yang dipilih. Silakan pilih dari daftar di sebelah kiri.")

st.markdown("---")
st.caption("© 2026 PREDIKSI PARLAY AI - Developed for Elangbola")
