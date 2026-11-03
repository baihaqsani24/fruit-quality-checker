import json                                      # baca model_info.json
from pathlib import Path                         # atur path file
import numpy as np                               # olah array gambar
import streamlit as st                           # library web app
import tensorflow as tf                          # muat model
from PIL import Image, ImageOps                  # buka & rapikan gambar

BASE_DIR = Path(__file__).parent                 # folder deployment/

@st.cache_resource                               # model dimuat satu kali, tidak diulang setiap klik
def load_model():
    return tf.keras.models.load_model(BASE_DIR / "model_best.keras")

@st.cache_data                                   # info model dibaca sekali
def load_info():
    with open(BASE_DIR / "model_info.json") as f:
        return json.load(f)

def siapkan_gambar(img, img_size):               # preprocessing sama persis dengan training
    img = ImageOps.exif_transpose(img)           # luruskan orientasi foto HP
    img = img.convert("RGB").resize(img_size)    # 3 channel + resize 224×224
    arr = np.array(img) / 255.0                  # scaling 0–1
    return np.expand_dims(arr, axis=0)           # tambah dimensi batch → (1, 224, 224, 3)

def run():
    st.title("Fruit Quality Checker")
    st.write("Upload foto buah untuk mengetahui apakah buah masih **segar (fresh)** "
             "atau sudah **busuk (rotten)**.")

    model = load_model()                         # ambil model (dari cache)
    info  = load_info()                          # ambil info: nama class, ukuran, threshold

    file = st.file_uploader("Upload foto buah", type=["jpg", "jpeg", "png"])   # tombol upload
    if file is not None:                         # jalankan hanya jika ada file yang di-upload
        img = Image.open(file)                   # buka file upload sebagai gambar
        st.image(img, caption="Foto yang di-upload", width=300)

        x = siapkan_gambar(img, tuple(info["img_size"]))            # preprocessing
        prob = float(model.predict(x, verbose=0)[0][0])             # peluang rotten
        label = info["class_names"][int(prob > info["threshold"])]  # angka → label teks
        keyakinan = prob if label == "rotten" else 1 - prob         # keyakinan terhadap label yang dipilih

        if label == "rotten":                                                    # buah diprediksi busuk
            st.error("**Buah busuk**: Perlu dilakukan penyortiran.")
        else:                                                                    # buah diprediksi segar
            st.success("**Buah dengan kondisi fresh**: Buah bisa dijual.")

        st.write(f"Keyakinan model: **{keyakinan:.0%}**")                         # tampilkan persentase keyakinan
        st.progress(keyakinan)                                                     # bar keyakinan 0–1
        st.caption("Catatan: model dilatih dengan foto bergaya studio dari internet. "
            "Untuk keputusan akhir, tetap lakukan pengecekan visual, terutama "
            "jika keyakinan model rendah.")                               