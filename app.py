# app.py, run with 'streamlit run app.py'
import pandas as pd
import streamlit as st
#from streamlit_gsheets import GSheetsConnection

# Create a connection object.
#conn = st.connection("gsheets", type=GSheetsConnection)

#df = conn.read()

# Print results.
#for row in df.itertuples():
#    st.write(f"Giorno: {row.Data}")

df = pd.read_csv("laptops.csv")  # read a CSV file inside
# df = pd.read_excel(...)  # will work for Excel files

st.title("Visualizzazione dati laptop")  # add a title
st.subheader("Anteprima dei dati")
st.dataframe(df)

st.subheader("Statistiche descrittive")
st.write(df.describe())

st.subheader("GPU - Prezzo")
st.scatter_chart(df, x="GPU", y="Final Price")

st.write('I love Laptops!')