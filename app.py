import streamlit as st

st.markdown("""
<link rel="manifest" href="/manifest.json">

<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/service-worker.js");
  });
}
</script>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Tornei Padel",
    page_icon="static/favicon.png",
    layout="wide"
)

# Inietta manifest e icone
st.markdown("""
<link rel="manifest" href="static/manifest.json">
<link rel="icon" type="image/png" sizes="32x32" href="static/favicon.png">
<link rel="apple-touch-icon" href="static/icon-192.png">
<meta name="theme-color" content="#00A86B">
""", unsafe_allow_html=True)

# Import moduli
from tornei.torneo_squadre import run as run_torneo_squadre
from tornei.draft12 import run as run_draft12
from tornei.draft16 import run as run_draft16
from tornei.draft16_misto import run as run_draft16_misto

# ---------------------------------------------------------
# CONFIGURAZIONE GRAFICA
# ---------------------------------------------------------

st.set_page_config(
    page_title="Tornei Padel",
    page_icon="🎾",
    layout="wide"
)

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

if scelta is None:
    st.header("📊 Dashboard Tornei Padel")

    col1, col2, col3 = st.columns(3)
    col1.metric("Tornei disponibili", "4")
    col2.metric("Versione", "1.0")
    col3.metric("Creato da", "Ugo")

    st.markdown("### Cosa puoi fare")
    st.markdown("""
    - Generare tornei a squadre
    - Creare draft da 12 o 16 giocatori
    - Gestire draft misti
    - Esportare tutto in Excel
    - Visualizzare grafici e statistiche
    """)
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
