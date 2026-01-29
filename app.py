import streamlit as st

# ---------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tornei Padel",
    page_icon="🎾",
    layout="wide"
)

# ---------------------------------------------------------
# IMPORT MODULI
# ---------------------------------------------------------
from tornei.torneo_squadre import run as run_torneo_squadre
from tornei.draft12 import run as run_draft12
from tornei.draft16 import run as run_draft16
from tornei.draft16_misto import run as run_draft16_misto

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🎾 Generatore Tornei Padel")
st.sidebar.markdown("Seleziona il tipo di torneo da generare")

scelta = st.sidebar.radio(
    "Tipo di torneo",
    [
        "Torneo a squadre",
        "Draft 12 giocatori",
        "Draft 16 giocatori",
        "Draft misto 16 giocatori"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Creato da UgoSavarese • Versione 1.0")

# ---------------------------------------------------------
# CONTENUTO PRINCIPALE
# ---------------------------------------------------------
st.title("🏆 Generatore Tornei Padel")
st.markdown("Benvenuto! Scegli il tipo di torneo dalla barra laterale per iniziare.")

if scelta == "Torneo a squadre":
    run_torneo_squadre()

elif scelta == "Draft 12 giocatori":
    run_draft12()

elif scelta == "Draft 16 giocatori":
    run_draft16()

elif scelta == "Draft misto 16 giocatori":
    run_draft16_misto()
