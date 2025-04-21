import streamlit as st
import pandas as pd
import random
import time
from random import randrange

st.title("Compatibilità inverter")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

url_map = {
    "Pannelli": "https://docs.google.com/spreadsheets/d/14WfndX8cj9YejXvBTuQP-GoXpiuMLRv7ptXCFA3MTY8/export?format=csv&gid=100113349",
    "Inverter": "https://docs.google.com/spreadsheets/d/14WfndX8cj9YejXvBTuQP-GoXpiuMLRv7ptXCFA3MTY8/export?format=csv&gid=2099613343",
    "Batterie": "https://docs.google.com/spreadsheets/d/14WfndX8cj9YejXvBTuQP-GoXpiuMLRv7ptXCFA3MTY8/export?format=csv&gid=633719834",
}

def parse_float(value):
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return None  # oppure np.nan se stai lavorando con pandas


#Converte i valori di una colonna da stringa con virgola a float, gestendo eventuali errori o valori nulli.
def clean_numeric_column(df, colname):
    return df[colname].apply(lambda x: parse_float(x))

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

df_panels = load_data(url_map["Pannelli"])
df_inverters = load_data(url_map["Inverter"])

st.header("⚡ Selezione del Modulo Fotovoltaico")
# Costruisci una colonna con identificatore univoco leggibile
df_panels["identifier"] = df_panels.apply(
    lambda row: f"{row['Company Name']} - {row['Series Name']} - {row['Model Name']} - {row['Model ID']}",
    axis=1
)
# Selectbox con tutti i pannelli unici
chosen_panel_str = st.selectbox("Scegli il pannello:", df_panels["identifier"])
# Recupera i dati del pannello scelto
panel_data = df_panels[df_panels["identifier"] == chosen_panel_str].squeeze()

st.markdown("### ℹ️ Dettagli pannello selezionato")
st.write(panel_data)

# === Inserimento numero moduli
n_modules = st.number_input("🔢 Inserisci il numero di moduli:", min_value=1, max_value=100, step=1)

# Recupero dati pannello scelto
v_mpp = parse_float(panel_data["Voltage at Maximum Power, Vmpp (V) At STC"])
v_oc = parse_float(panel_data["Open Circuit Voltage, Voc (V) At STC"])
i_sc = parse_float(panel_data["Short Circuit Current, Isc (A) At STC"])
k_vt_percentage = panel_data["Temperature coefficient of Voc (%/°C)"]
k_vt = float(k_vt_percentage.replace(",", "."))/100
noct_str = panel_data["Temperature (°C) At NOCT"]
try:
    noct = float(noct_str.split("±")[0])
except Exception as e:
    st.error(f"Errore nella conversione: {e}")
 

# === Calcoli
if st.button("🔍 Calcola combinazioni con inverter compatibili"):
    st.markdown("## 🧮 Calcoli in corso...")

    ambience_t_min = 1.0
    ambience_t_max = 30.0

    #Calcolo T max e T min del modulo
    module_t_min = ambience_t_min + ((noct - 20)*1.25)
    module_t_max = ambience_t_max + ((noct - 20)*0.125)
    #Controlli
    if module_t_max<module_t_min:
        st.error("Errore nei calcoli: temperatura massima del modulo < temperatura minima del modulo")  

    #Calcolo Vmpp min e Voc max del modulo
    module_v_min = v_mpp - k_vt*(25 - module_t_min)*v_mpp
    module_v_max = v_oc - k_vt*(25 - module_t_max)*v_oc
    #Controlli 
    if module_v_max<module_v_min:
        st.error("Errore nei calcoli: tensione massima del modulo < tensione minima del modulo")

    #Calcolo Vmpp min e Voc max
    v_mpp_min = module_v_min*n_modules
    v_oc_max = module_v_max*n_modules

    #st.write("Dati ottenuti: ")
    #st.write(f"📦 Potenza totale impianto: **{potenza_totale} W**")

    # Elimina inverter con valori nulli nelle colonne necessarie
    df_inverter_clean = df_inverters.dropna(subset=["Min. DC Voltage to Start Feed In (V)", "Max. DC Voltage (V)", "Max. DC Current (A)"])

    columns_to_clean = [
    "Min. DC Voltage to Start Feed In (V)", 
    "Max. DC Voltage (V)", 
    "Max. DC Current (A)"
    ]

    for col in columns_to_clean:
        df_inverter_clean[col] = clean_numeric_column(df_inverter_clean, col)


    # Filtro inverter compatibili
    compat_inverters = df_inverter_clean[
        (df_inverter_clean["Min. DC Voltage to Start Feed In (V)"] <= v_mpp_min) &
        (df_inverter_clean["Max. DC Voltage (V)"] >= v_oc_max) &
        (df_inverter_clean["Max. DC Current (A)"] >= i_sc)
    ]


    if not compat_inverters.empty:
        st.success("✅ Inverter compatibili trovati!")
        st.dataframe(compat_inverters)
    else:
        st.warning("⚠️ Nessun inverter compatibile trovato")



# ---------- SEZIONE CHATBOT ---------
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

