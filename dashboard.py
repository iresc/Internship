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

if st.sidebar.button('Resetta i filtri'):
    st.session_state.dff = df


st.header('Trova il laptop più adatto alle tue esigenze')
st.markdown('---')
# Mostra il DataFrame aggiornato
st.dataframe(st.session_state.dff)

if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False

# Pulsante per aprire/chiudere la finestra del chatbot
if st.button('Conversa con il Chatbot'):
    st.session_state.show_chatbot = not st.session_state.show_chatbot  # Inverte lo stato

# Aggiungi il chatbot solo se la variabile è True
if st.session_state.show_chatbot:
    st.markdown("""
        <div id="chatbot" style="position: fixed; bottom: 20px; right: 20px; width: 300px; height: 400px; border: 2px solid #ccc; background-color: rgb(14, 17, 23); border-radius: 8px; display: flex; flex-direction: column;">
            <div style="flex: 1; padding: 10px; overflow-y: auto;">
                <div id="chat-content" style="max-height: 90%; overflow-y: scroll;">
                    Ciao! Come posso aiutarti?
                </div>
            </div>
            <input id="user-input" type="text" placeholder="Scrivi un messaggio..." style="border: none; padding: 10px; width: 100%; box-sizing: border-box;">
        </div>

        <script>
            // Funzione per inviare il messaggio
            function scrivi() {
                event.preventDefault(); // Previene il comportamento di invio del modulo (rende il submit non necessario)
                
                let userMessage = document.getElementById("user-input").value;
                if (userMessage.trim() !== "") {
                    let chatContent = document.getElementById("chat-content");
                    
                    // Aggiungi il messaggio dell'utente alla chat
                    chatContent.innerHTML += "<div style='margin-bottom: 10px; background-color: #f1f1f1; border-radius: 5px; padding: 5px;'>Tu: " + userMessage + "</div>";
                    
                    // Aggiungi una risposta automatica del chatbot
                    chatContent.innerHTML += "<div style='margin-bottom: 10px; background-color: #e2e2e2; border-radius: 5px; padding: 5px;'>Bot: Risposta automatica!</div>";
                    
                    // Scorri automaticamente in basso per visualizzare l'ultimo messaggio
                    chatContent.scrollTop = chatContent.scrollHeight;

                    // Pulisci il campo di input
                    document.getElementById("user-input").value = "";
                }
            }

            // Gestisci l'evento keydown per inviare il messaggio con il tasto "Enter"
            document.getElementById("user-input").addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    scrivi();  // Chiama la funzione scrivi
                }
            });
        </script>
    """, unsafe_allow_html=True)
