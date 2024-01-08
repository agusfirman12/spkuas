import streamlit as st
import numpy as np
import pandas as pd

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


import math


def normalization(matrix):
    # Transpose Decision Matrix
    matrix = matrix.transpose()
    row_values = []
    norm_matrix = []

    for i in range(matrix.shape[0]): # Looping per baris (kriteria)
        # Menghitung sum tiap x_{ij}^2
        sum_row = sum([pow(x,2) for x in matrix[i]])

        for j in range(matrix[i].shape[0]): # Looping per kolom (alternatif)
            # membangi nilai asli x_{ij} dengan hasil akar
            r_value = matrix[i][j] / math.sqrt(sum_row)

            # Masukkan hasil normalisasi ke list tiap baris
            row_values.append(r_value)

        #Masukkan hasil normalisasi per baris ke matrix normalisasi
        norm_matrix.append(row_values)

        #Kosongkan list normalisasi perbaris
        row_values = []

    # Ubah dalam bentuk numpy array
    norm_matrix = np.asarray(norm_matrix)

    # Return dalam bentuk transporse agar kembali ke format awal
    return norm_matrix.transpose()


# Fungsi untuk kalkulasi matrix terbobot. Paramter yang diperlukan adalah nilai ternormalisasi dan bobot
# Untuk mempermudah perhitungan, lakukan operasi transpose pada matrix ternormalisasi.
# Ingat! Kriteria adalah baris, alternatif adalah kolom setelah proses transpose
def weighted_normalization(n_matrix, c_weights):
    # Buat salinan nilai ternormalisasi dan transpose
    norm_weighted = n_matrix.transpose()

    for i in range(c_weights.shape[0]): # Looping tiap kriteria
        # Kalkulasi normalisasi terbobot
        norm_weighted[i] = [r * c_weights[i] for r in norm_weighted[i]]

    # Ubah ke bentuk numpy array
    norm_weighted = np.asarray(norm_weighted)

    # Return ke dalam format matrix semula
    return norm_weighted.transpose()


# Implementasi Menghitung Nilai Optimasi
def optimize_value(w_matrix, label):
    y_values = []

    for i in range(w_matrix.shape[0]):
        max_val = []
        min_val = []

        for j in range(w_matrix[i].shape[0]):
            # Hitung benefit
            if label[j] == 1:
                max_val.append(w_matrix[i][j])
            # Hitung cost
            else:
                min_val.append(w_matrix[i][j])

        y = sum(max_val) - sum(min_val)
        y_values.append(y)

    return np.asarray(y_values)

def ranking(vector):
    temp = vector.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(vector))

    return len(vector) - ranks


def run():
    st.set_page_config(
        page_title="Implementasi MOORA",
        page_icon="👋",
    )

    st.write("# Implementasi Metode MOORA")
    st.write("Dikembangkan oleh Mohamad Agus Firmansah.")
    st.write("## Studi Kasus")
    st.write(" PT. ABC adalah perusahaan yang bergerak di bidang consumer good yang akan menginvestasikan sisa usahanya dalam satu tahun Beberapa alternatif investasi akan diidentifikasi. Pemilihan alternatif terbaik ditujukan selain untuk keperluan investasi, juga dalam rangka meningkatkan kinerja perusahaan ke depan")
    st.write("Ada 5 kriteria yang dijadikan acuan dalam pengambilan keputusan, yaitu:")
    st.write("C1 = Harga (Cost), :n C2 = Nilai investasi 10 tahun ke depan (Benefit), :c C3 = Daya dukung terhadap produktivitas perusahaan (Benefit) :n(1: kurang mendukung, 2: Cukup mendukung, 3: mendukung, 4: sangat mendukung ), :c C4 = Prioritas Kebutuhan (Cost) :n(1: kurang prioritas, 2: Cukup prioritas, 3: prioritas, 4: sangat prioritas ), :c C5 = Ketersediaan atau kemudahan (Benefit) :n(1: kurang mudah diperoleh, 2: Cukup mudah diperoleh, 3: sangat mudah diperoleh )") 
    st.write("Pengambilan keputusan memberikan bobot preferensi sebagai C1 = 20%, C2 = 15%, C3 = 30%, C4 = 25%, dan C5 = 10%")

    st.divider()

    st.write("## Input Nilai Bobot, Nilai Label dan Nilai Kriteria")

    # Mendefinisikan Bobot Kriteria
    c_weights = st.text_input("Masukkan Bobot Kriteria (pisahkan dengan koma)", 0.0)
    if c_weights is not None:
        c_weights = np.array([float(weight) for weight in c_weights.split(',')])

    label = st.text_input("Masukkan Label cost(0),benefit(1) - (pisahkan dengan koma)", 0)
    if label is not None:
        label = np.array([int(label) for label in label.split(',')])

    c1 = st.number_input("Nilai C1", min_value=0, max_value=100000000, value=0, step=1)
    c2 = st.number_input("Nilai C2", min_value=0, max_value=100000000, value=0, step=1)
    c3 = st.number_input("Nilai C3", min_value=0, max_value=1000, value=0, step=1)
    c4 = st.number_input("Nilai C4", min_value=0, max_value=1000, value=0, step=1)
    c5 = st.number_input("Nilai C5", min_value=0, max_value=1000, value=0, step=1)

    if st.button("Simpan", type='primary', on_click=click_button):
        simpanData(c1,c2,c3,c4,c5)

    if st.session_state.clicked:
        data = st.session_state.nilai_kriteria
        df = pd.DataFrame(data, columns=('C1','C2','C3','C4','C5'))
        st.dataframe(df)

        if st.button("Proses"):
            prosesData(c_weights,label)

def simpanData(c1,c2,c3,c4,c5):
    if 'nilai_kriteria' not in st.session_state:
        st.session_state.nilai_kriteria = np.array([[c1,c2,c3,c4,c5]])
    else:
        dataLama = st.session_state.nilai_kriteria
        dataBaru = np.append(dataLama, [[c1,c2,c3,c4,c5]], axis=0)
        st.session_state.nilai_kriteria = dataBaru



def prosesData(c_weights, label):
    init_matrix = st.session_state.nilai_kriteria

    n_matrix = normalization(init_matrix)
    w_matrix = weighted_normalization(n_matrix, c_weights)
    result = optimize_value(w_matrix, label)
    peringkatAkhir = ranking(result)


    st.write("Hasil Normalisasi:")
    st.text(n_matrix)

    st.write("Hasil Pembobotan:")
    st.text(w_matrix)

    st.write("Perhitungan Fungsi Normalisasi:")
    st.text(result)

    st.write("Perankingan:")
    st.text(peringkatAkhir)


if __name__ == "__main__":
    run()