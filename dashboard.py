import streamlit as st
import pandas as pd

df = pd.read_csv("laptops.csv") ## dataframe con dati laptop

st.dataframe(df)