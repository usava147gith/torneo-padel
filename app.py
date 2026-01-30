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
# DEBUG
# ---------------------------------------------------------
st.write("SAFE MODE ATTIVO — Loader e PWA disattivati")

# ---------------------------------------------------------
# IMPORT FUNZIONI TORNEI
# ---------------------------------------------------------
from tornei.torneo_squadre import run as run_torneo_squadre
from tornei.draft12 import run as run_draft12
from tornei.draft16 import run as run_draft16
from tornei.draft16_misto import run as run_draft16_misto

# ---------------------------------------------------------
# SIDEBAR iOS STYLE
# ---------------------------------------------------------
st.sidebar.title("🎾 Tornei Padel")
st.sidebar.markdown("Seleziona il tipo di torneo")

scelta = st.sidebar.radio(
    "",
    [
        "Torneo a squadre",
        "Draft 12 giocatori",
        "Draft 16 giocatori",
        "Draft misto 16 giocatori"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Creato da UgoSavarese")

# ---------------------------------------------------------
# HOME PAGE (con griglia mobile 2×2)
# ---------------------------------------------------------
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
