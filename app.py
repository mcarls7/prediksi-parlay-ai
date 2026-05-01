import streamlit as st
import pandas as pd

# Pastikan fungsi fetch_odds dan save_to_history diimpor jika Anda menggunakan file terpisah
# from utils import fetch_odds 
# from database import save_to_history

st.set_page_config(page_title="PREDIKSI PARLAY AI", layout="wide")

st.title("🤖 PREDIKSI PARLAY AI")

# --- Bagian yang Anda edit di screenshot (Daftar Pilihan Parlay) ---
if 'parlay_list' not in st.session_state:
    st.session_state.parlay_list = []

col_parlay = st.container() # Menggunakan container agar rapi

with col_parlay:
    st.subheader("💰 Tiket Parlay Anda")

    if st.session_state.parlay_list:
        total_odds = 1.0
        details = []

        st.write("**Daftar Pilihan:**")
        for item in st.session_state.parlay_list:
            # Baris ini yang sebelumnya error karena terpotong
            st.write(f"✅ {item['Pertandingan']} ({item['Pilihan']}) @ {item['Odds']}")
            total_odds *= item['Odds']
            details.append(f"{item['Pertandingan']}@{item['Odds']}")

        st.markdown("---")
        st.metric("Total Odds", f"{total_odds:.2f}x")

        stake = st.number_input("Modal Taruhan (Rp/$)", min_value=0.0, value=10000.0)
        potential_win = stake * total_odds
        st.write(f"Estimasi Kemenangan: **{potential_win:,.2f}**")
        
        if st.button("🗑️ Reset Parlay"):
            st.session_state.parlay_list = []
            st.rerun()
    else:
        st.info("Belum ada pertandingan yang dipilih. Silakan pilih dari daftar di sebelah kiri.")

st.markdown("---")
st.caption("© 2026 PREDIKSI PARLAY AI - Developed for Randy Sanjaya")
