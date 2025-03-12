import streamlit as st
import pandas as pd

df = pd.read_csv("laptops.csv") ## dataframe con dati laptop

st.dataframe(df)

brands = df["Brand"].unique().tolist() ## estrai valori unici di brand dal dataframe

selectbox_marca = st.sidebar.selectbox('Scegli una marca',brands)