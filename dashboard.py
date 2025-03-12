import streamlit as st
import pandas as pd

# Carica il DataFrame iniziale solo una volta
if "dff" not in st.session_state:
    st.session_state.dff = pd.read_csv("laptops.csv")

df = pd.read_csv("laptops.csv")  # Carica il DataFrame

# Estrai valori unici dalle colonne
brands = df["Brand"].unique().tolist()
statuses = df["Status"].unique().tolist()
rams = sorted(df["RAM"].unique().tolist())
storages = sorted(df["Storage"].unique().tolist())

# Definisci le fasce di prezzo predefinite
price_ranges = {
    "0 - 100": (0, 100),
    "100 - 300": (100, 300),
    "300 - 500": (300, 500),
    "500 - 1000": (500, 1000),
    "1000 - 2000": (1000, 2000),
    "2000 - MAX": (2000, df["Final Price"].max())
}

# Sidebar per i filtri
selectbox_marca = st.sidebar.selectbox('Scegli una marca', brands)
selectbox_stato = st.sidebar.selectbox('In che stato vuoi che sia?', statuses)
selectbox_ram = st.sidebar.selectbox('Quanta RAM minima?', rams)
selectbox_storages = st.sidebar.selectbox('Quanta ROM minima?', storages)

# Selectbox per la fascia di prezzo
selected_range = st.sidebar.selectbox("Seleziona fascia di prezzo", list(price_ranges.keys()))
min_price, max_price = price_ranges[selected_range]

# Bottone per applicare il filtro
if st.sidebar.button('Filtra'):
    st.session_state.dff = df[
        (df["Brand"] == selectbox_marca) &
        (df["Status"] == selectbox_stato) &
        (df["RAM"] >= selectbox_ram) &
        (df["Storage"] >= selectbox_storages) &
        (df["Final Price"].between(min_price, max_price))
    ]

# Mostra il DataFrame aggiornato
st.dataframe(st.session_state.dff)
