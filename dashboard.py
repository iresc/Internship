import streamlit as st
import pandas as pd

if "df" not in st.session_state:
    st.session_state.df = pd.read_csv("laptops.csv")


# Sidebar per i filtri
brands = st.session_state.df["Brand"].unique().tolist()
statuses = st.session_state.df["Status"].unique().tolist()
rams = sorted(st.session_state.df["RAM"].unique().tolist())
storages = sorted(st.session_state.df["Storage"].unique().tolist())
prices = sorted(st.session_state.df["Final Price"].unique().tolist())

# Creazione dei widget di selezione
selectbox_marca = st.sidebar.selectbox('Scegli una marca', brands)
selectbox_stato = st.sidebar.selectbox('In che stato vuoi che sia?', statuses)
selectbox_ram = st.sidebar.selectbox('Quanta RAM minima?', rams)
selectbox_storages = st.sidebar.selectbox('Quanta ROM minima?', storages)
add_slider = st.sidebar.slider('Seleziona range di prezzo', 0.0, max(prices), (0.0, 3500.0), key='range_prezzo')


if st.sidebar.button('Filtra'):
    st.session_state.df = st.session_state.df[
        (st.session_state.df["Brand"] == selectbox_marca) &
        (st.session_state.df["Status"] == selectbox_stato) &
        (st.session_state.df["RAM"] >= selectbox_ram) &
        (st.session_state.df["Storage"] >= selectbox_storages) &
        (st.session_state.df["Final Price"].between(add_slider[0], add_slider[1]))
    ]

# Mostra il DataFrame aggiornato
st.dataframe(st.session_state.df)
   