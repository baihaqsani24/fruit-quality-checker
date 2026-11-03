import streamlit as st          # library web app
import eda                      # modul halaman EDA (eda.py)
import prediction               # modul halaman prediksi (prediction.py)

st.set_page_config(page_title="Fruit Quality Checker",   # judul tab browser
                   page_icon="🍎",                         # ikon tab
                   layout="centered")                      # tata letak halaman

page = st.sidebar.selectbox("Pilih Halaman", ["Prediksi", "EDA"])   # menu navigasi di sidebar

if page == "Prediksi":          # kalau user memilih Prediksi
    prediction.run()            # jalankan fungsi run() di prediction.py
else:                           # selain itu (EDA)
    eda.run()                   # jalankan fungsi run() di eda.py