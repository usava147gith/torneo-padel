import streamlit as st

# ---------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tornei Padel",
    page_icon="icons/padel_icon.png",
    layout="wide"
)

# ---------------------------------------------------------
# CSS PERSONALIZZATO
# ---------------------------------------------------------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
    label, .stTextInput label, .stSelectbox label {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #333 !important;
    }
    input[type="text"], input[type="number"] {
        font-size: 1.1rem !important;
        padding: 8px 10px !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        font-size: 1.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .dataframe th {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        background-color: #f2f2f2 !important;
        padding: 12px !important;
        text-align: center !important;
    }
    .dataframe td {
        font-size: 1.1rem !important;
        padding: 10px !important;
        text-align: center !important;
    }
    .dataframe {
        border-collapse: separate !important;
        border-spacing: 0 8px !important;
    }
    .dataframe tbody tr {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
    }
    .dataframe tbody tr:hover {
        background-color: #fafafa !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PWA
# ---------------------------------------------------------
st.markdown("""
<link rel="manifest" href="manifest.json">
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register("service-worker.js");
    });
}
</script>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ONBOARDING INIZIALE (VERSIONE SICURA)
# ---------------------------------------------------------
if "onboarding_done" not in st.session_state:
    st.session_state.onboarding_done = False

if not st.session_state.onboarding_done:

    st.markdown("""
    <div class="fade-in" style="
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        max-width: 400px;
        margin: 4rem auto;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    ">
        <div style="font-size: 64px; margin-bottom: 1rem; color: #34C759;">🎾</div>
        <h2 style="margin-bottom: 0.5rem;">Benvenuto in Tornei Padel</h2>
        <p style="font-size: 17px; color: #6E6E73;">
            Organizza tornei, crea squadre e genera partite in modo semplice e veloce.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Inizia"):
        st.session_state.onboarding_done = True
        st.rerun()

    st.stop()

# ---------------------------------------------------------
# CSS ESTERNO (styles.css)
# ---------------------------------------------------------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------
# IMPORT FUNZIONI TORNEI
# ---------------------------------------------------------
from tornei.torneo_squadre import run as run_torneo_squadre
from tornei.draft12 import run as run_draft12
from tornei.draft16 import run as run_draft16
from tornei.draft16_misto import run as run_draft16_misto
from tornei.campionato16 import run as run_campionato16

# ---------------------------------------------------------
# SIDEBAR iOS STYLE
# ---------------------------------------------------------
st.sidebar.title("🎾Tornei Padel")
st.sidebar.markdown("Seleziona il tipo di torneo")

scelta = st.sidebar.radio(
    "Seleziona un torneo",
    [
        "Torneo a squadre",
        "Draft 12 giocatori",
        "Draft 16 giocatori",
        "Draft misto 16 giocatori",
        "Torneo 16 squadre (Campionato)"
    ],
    label_visibility="collapsed"
)



st.sidebar.markdown("---")
st.sidebar.info("V1.0 by UgoSavarese")


# ---------------------------------------------------------
# ROUTING TORNEI
# ---------------------------------------------------------

if scelta == "Torneo a squadre":
    run_torneo_squadre()

elif scelta == "Draft 12 giocatori":
    run_draft12()

elif scelta == "Draft 16 giocatori":
    run_draft16()

elif scelta == "Draft misto 16 giocatori":
    run_draft16_misto()
    
elif scelta == "Torneo 16 squadre (Campionato)":
    run_campionato16()


# ---------------------------------------------------------
# HOME PAGE (solo se nessun torneo è selezionato)
# ---------------------------------------------------------
else:
    st.title("🏆 Generatore Tornei Padel")
    st.markdown("Benvenuto! Scegli il tipo di torneo dalla barra laterale.")

    st.markdown("### Seleziona un torneo")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="mobile-card fade-in">
            <div class="mobile-card-icon">👥</div>
            <div class="mobile-card-title">Torneo a squadre</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="mobile-card fade-in">
            <div class="mobile-card-icon">🔢</div>
            <div class="mobile-card-title">Draft 12</div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="mobile-card fade-in">
            <div class="mobile-card-icon">🎯</div>
            <div class="mobile-card-title">Draft 16</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="mobile-card fade-in">
            <div class="mobile-card-icon">♀♂</div>
            <div class="mobile-card-title">Draft misto</div>
        </div>
        """, unsafe_allow_html=True)

