import streamlit as st
import pandas as pd

df = pd.read_csv("laptops.csv") ## dataframe con dati laptop

st.dataframe(df)

brands = df["Brand"].unique().tolist() ## estrai valori unici di brand dal dataframe

statuses = df["Status"].unique().tolist() ## estrai valori unici di stato

rams = sorted(df["RAM"].unique().tolist()) ## estrai valori unici di ram

storages = sorted(df["Storage"].unique().tolist()) ## estrai valori unici di storage

prices = sorted(df["Final Price"].unique().tolist()) ## estrai prezzi unici


selectbox_marca = st.sidebar.selectbox('Scegli una marca',brands)

selectbox_stato = st.sidebar.selectbox('In che stato vuoi che sia?',statuses)

selectbox_ram = st.sidebar.selectbox('Quanta RAM minima?',rams)

selectbox_storages = st.sidebar.selectbox('Quanta ROM minima?',storages)

selectbox_prices = st.sidebar.selectbox('Prezzo massimo?',prices)
