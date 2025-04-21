import streamlit as st
import pandas as pd
from random import randrange

pg = st.navigation([st.Page("page1.py", title="Consulta il catalogo"), st.Page("page2.py", title="Compatibilità inverter")])
pg.run()
