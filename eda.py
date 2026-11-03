from pathlib import Path                         # atur path file
import pandas as pd                              # tabel data
import matplotlib.pyplot as plt                  # grafik
import streamlit as st                           # library web app
from PIL import Image                            # buka gambar

BASE_DIR = Path(__file__).parent                 # folder deployment/

def run():
    st.title("Exploratory Data Analysis")

    # --- 1. Ringkasan dataset ---
    st.subheader("Ringkasan Dataset")
    st.write("Dataset **Fruits Quality (Fresh VS Rotten)** dari Kaggle berisi 359 gambar "
             "dengan 2 class: `fresh` dan `rotten`. Setiap gambar berukuran 640×640 piksel (RGB).")

    # --- 2. Distribusi class per split ---
    st.subheader("Distribusi Class per Split")
    distribusi = pd.DataFrame({"fresh":  [145, 24, 12],      # jumlah fresh per split
                               "rotten": [142, 24, 12]},     # jumlah rotten per split
                              index=["train", "valid", "test"])
    fig, ax = plt.subplots(figsize=(7, 4))                   # siapkan kanvas grafik
    distribusi.plot(kind="bar", ax=ax, rot=0)                # bar chart per split
    ax.set_xlabel("Split")
    ax.set_ylabel("Jumlah Gambar")
    st.pyplot(fig)                                           # tampilkan grafik di Streamlit
    st.write("Jumlah class fresh dan rotten **seimbang di setiap split**, dengan proporsi "
             "sekitar 80% train, 13% validation, dan 7% test.")                                           

    # --- 3. Contoh gambar ---
    st.subheader("Contoh Gambar")
    for label in ["fresh", "rotten"]:                        # untuk setiap class
        st.write(f"**{label}**")
        cols = st.columns(3)                                 # 3 kolom berdampingan
        for i, col in enumerate(cols, start=1):              # gambar ke-1 sampai 3
            img = Image.open(BASE_DIR / "sample_images" / f"{label}_{i}.jpg")
            col.image(img)                                   # tampilkan di kolom
    st.write("Buah **fresh** umumnya berwarna cerah dengan kulit mulus, sedangkan buah "
             "**rotten** menunjukkan perubahan warna menjadi cokelat hingga kehitaman, "
             "permukaan keriput, atau berjamur. Dataset berisi berbagai jenis buah, dan "
             "sebagian gambar fresh berlatar putih polos seperti foto studio.")