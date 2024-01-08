import streamlit as st
import numpy as np
import pandas as pd

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True



    st.write("## Input Nilai Kriteria")

    c1 = st.number_input("Nilai C1", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c2 = st.number_input("Nilai C2", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c3 = st.number_input("Nilai C3", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c4 = st.number_input("Nilai C4", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c5 = st.number_input("Nilai C5", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

    if st.button("Simpan", type='primary', on_click=click_button):
        simpanData(c1,c2,c3,c4,c5)
    

def simpanData(c1,c2,c3,c4,c5):
    if 'nilai_kriteria' not in st.session_state:
        st.session_state.nilai_kriteria = np.array([[c1,c2,c3,c4,c5]])
    else:
        dataLama = st.session_state.nilai_kriteria
        dataBaru = np.append(dataLama, [[c1,c2,c3,c4,c5]], axis=0)
        st.session_state.nilai_kriteria = dataBaru