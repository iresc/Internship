import streamlit as st
import pandas as pd

df = pd.read_csv("laptops.csv") ## dataframe con dati laptop

st.dataframe(df)

brands = df["Brand"].unique().tolist() ## estrai valori unici di brand dal dataframe

statuses = df["Status"].unique().tolist() ## estrai valori unici di stato

rams = df["Ram"].unique().tolist() ## estrai valori unici di ram

storages = df["Storage"].unique().tolist() ## estrai valori unici di storage


selectbox_marca = st.sidebar.selectbox('Scegli una marca',brands)

selectbox_stato = st.sidebar.selectbox('In che stato vuoi che sia?',statuses)

selectbox_ram = st.sidebar.selectbox('Quanta RAM minima?',rams)

selectbox_storages = st.sidebar.selectbox('Quanta ROM minima?',storages)

