import streamlit as st
import pandas as pd
import random
import time
from random import randrange

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

url_map = {
    "Pannelli": "https://docs.google.com/spreadsheets/d/14WfndX8cj9YejXvBTuQP-GoXpiuMLRv7ptXCFA3MTY8/export?format=csv&gid=100113349",
    "Inverter": "https://docs.google.com/spreadsheets/d/14WfndX8cj9YejXvBTuQP-GoXpiuMLRv7ptXCFA3MTY8/export?format=csv&gid=2099613343",
    "Batterie": "https://docs.google.com/spreadsheets/d/14WfndX8cj9YejXvBTuQP-GoXpiuMLRv7ptXCFA3MTY8/export?format=csv&gid=633719834",
}


st.markdown("""
    <style>
        .st-emotion-cache-janbn0 {
            margin-left: 60%;
        }
    

        .st-emotion-cache-4oy321{
            background-color: rgba(38, 39, 48, 0.5);
            margin-right: 50%;
        }
    </style>
    """,
    unsafe_allow_html=True
)



# Carica il DataFrame iniziale solo una volta
#if "dff" not in st.session_state:
#    st.session_state.dff = pd.read_csv("laptops.csv")
#     st.session_state.dff = pd.read_csv(url)

#df = pd.read_csv("laptops.csv")  # Carica il DataFrame


# Estrai valori unici dalle colonne
#brands = df["Brand"].unique().tolist()
#statuses = df["Status"].unique().tolist()
#rams = sorted(df["RAM"].unique().tolist())
#storages = sorted(df["Storage"].unique().tolist())

# Definisci le fasce di prezzo predefinite
#price_ranges = {
#    "0 - 100": (0, 100),
#    "100 - 300": (100, 300),
#    "300 - 500": (300, 500),
#    "500 - 1000": (500, 1000),
#    "1000 - 2000": (1000, 2000),
#    "2000 - MAX": (2000, df["Final Price"].max())
#}

# Sidebar per i filtri
#selectbox_marca = st.sidebar.selectbox('Scegli una marca', brands)
#selectbox_stato = st.sidebar.selectbox('In che stato vuoi che sia?', statuses)
#selectbox_ram = st.sidebar.selectbox('Quanta RAM minima?', rams)
#selectbox_storages = st.sidebar.selectbox('Quanta ROM minima?', storages)

# Selectbox per la fascia di prezzo
#selected_range = st.sidebar.selectbox("Seleziona fascia di prezzo", list(price_ranges.keys()))
#min_price, max_price = price_ranges[selected_range]

# Bottone per applicare il filtro
#if st.sidebar.button('Filtra'):
#    st.session_state.dff = df[
#        (df["Brand"] == selectbox_marca) &
#        (df["Status"] == selectbox_stato) &
#        (df["RAM"] >= selectbox_ram) &
#        (df["Storage"] >= selectbox_storages) &
#        (df["Final Price"].between(min_price, max_price))
#    ]

# bottone per resettare i filtri
#if st.sidebar.button('Resetta i filtri'):
#    st.session_state.dff = df


st.header("Impianti fotovoltaici - selezione componenti")
chosen_sheet = st.selectbox("Scegli la categoria da visualizzare:", list(url_map.keys()))

st.markdown('---')
df = load_data(url_map[chosen_sheet])
st.subheader(f"📋 {chosen_sheet}")
st.dataframe(df)


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Ciao! Come posso aiutarti oggi?",
            "Benvenuto nella chatbox! C'è qualcosa con cui posso aiutarti?",
            "🤖 C-I-A-O ! Dimmi, di cosa hai bisogno?",
            "⚠ chatbot ancora in produzione ⚠",
        ]
    )
    for word in list(response):
        yield word + ""
        time.sleep(randrange(2)/10)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Fammi una domanda..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

