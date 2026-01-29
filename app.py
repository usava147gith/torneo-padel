import streamlit as st

st.set_page_config(
    page_title="Tornei Padel",
    page_icon="🎾",
    layout="wide"
)

st.title("🏆 Generatore Tornei Padel")
st.write("Se vedi questo testo, Streamlit sta funzionando.")

from tornei.torneo_squadre import run as run_torneo_squadre
from tornei.draft12 import run as run_draft12
from tornei.draft16 import run as run_draft16
from tornei.draft16_misto import run as run_draft16_misto

st.sidebar.title("🎾 Generatore Tornei Padel")
scelta = st.sidebar.radio(
    "Tipo di torneo",
    [
        "Torneo a squadre",
        "Draft 12 giocatori",
        "Draft 16 giocatori",
        "Draft misto 16 giocatori"
    ]
)

if scelta == "Torneo a squadre":
    run_torneo_squadre()
elif scelta == "Draft 12 giocatori":
    run_draft12()
elif scelta == "Draft 16 giocatori":
    run_draft16()
elif scelta == "Draft misto 16 giocatori":
    run_draft16_misto()
