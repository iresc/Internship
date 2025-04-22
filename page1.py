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


st.header("Impianti fotovoltaici - selezione componenti")
chosen_sheet = st.selectbox("Scegli la categoria da visualizzare:", list(url_map.keys()))

st.markdown('---')
df = load_data(url_map[chosen_sheet])
st.subheader(f"📋 {chosen_sheet}")
st.dataframe(df)



# ----------- SEZIONE CHATBOT -----------
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