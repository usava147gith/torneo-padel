import streamlit as st
import pandas as pd
import json
from io import BytesIO

# ---------------------------------------------------------
# GENERAZIONE CALENDARIO ROUND ROBIN (16 SQUADRE)
# ---------------------------------------------------------
def genera_calendario_16_squadre(squadre):
    assert len(squadre) == 16, "Servono esattamente 16 squadre"

    n = 16
    giornate = []

    lista = squadre.copy()
    fissa = lista[0]
    rotanti = lista[1:]

    for turno in range(15):
        giornata = []

        left = [fissa] + rotanti[:7]
        right = rotanti[7:][::-1]

        for a, b in zip(left, right):
            giornata.append((a, b))

        rotanti = rotanti[1:] + rotanti[:1]
        giornate.append(giornata)

    return giornate


# ---------------------------------------------------------
# PUNTEGGIO
# ---------------------------------------------------------
def punti_da_risultato(ris):
    if not ris:
        return (0, 0)

    a, b = map(int, ris.split("-"))

    if a == 2 and b == 0:
        return (3, 0)
    if a == 2 and b == 1:
        return (2, 1)
    if b == 2 and a == 1:
        return (1, 2)
    if b == 2 and a == 0:
        return (0, 3)

    return (0, 0)


# ---------------------------------------------------------
# CLASSIFICA
# ---------------------------------------------------------
def calcola_classifica(giornate, risultati, squadre):
    punti = {s: 0 for s in squadre}
    set_vinti = {s: 0 for s in squadre}
    set_persi = {s: 0 for s in squadre}

    idx = 0
    for giornata in giornate:
        for a, b in giornata:
            ris = risultati[idx]
            idx += 1

            pa, pb = punti_da_risultato(ris)
            punti[a] += pa
            punti[b] += pb

            if ris:
                sa, sb = map(int, ris.split("-"))
                set_vinti[a] += sa
                set_persi[a] += sb
                set_vinti[b] += sb
                set_persi[b] += sa

    df = pd.DataFrame({
        "Squadra": squadre,
        "Punti": [punti[s] for s in squadre],
        "Set Vinti": [set_vinti[s] for s in squadre],
        "Set Persi": [set_persi[s] for s in squadre],
        "Diff Set": [set_vinti[s] - set_persi[s] for s in squadre],
    })

    return df.sort_values(by=["Punti", "Diff Set", "Set Vinti"], ascending=False)


# ---------------------------------------------------------
# UI PRINCIPALE
# ---------------------------------------------------------
def run():
    st.header("🏆 Torneo 16 Squadre — Campionato")

    # CARICAMENTO TORNEO
    uploaded = st.file_uploader("📂 Carica torneo salvato", type="json")
    if uploaded:
        data = json.load(uploaded)
        st.session_state.c16_squadre = data["squadre"]
        st.session_state.c16_giornate = data["giornate"]
        st.session_state.c16_risultati = data["risultati"]
        st.success("Torneo caricato!")

    # INSERIMENTO SQUADRE
    if "c16_squadre" not in st.session_state:
        with st.form("form_squadre"):
            squadre = []
            col1, col2 = st.columns(2)
            with col1:
                for i in range(1, 9):
                    squadre.append(st.text_input(f"Squadra {i}", f"S{i}"))
            with col2:
                for i in range(9, 17):
                    squadre.append(st.text_input(f"Squadra {i}", f"S{i}"))

            conferma = st.form_submit_button("Conferma squadre")

        if conferma:
            st.session_state.c16_squadre = squadre
            st.session_state.c16_giornate = genera_calendario_16_squadre(squadre)
            st.session_state.c16_risultati = [""] * 120
            st.rerun()

        st.stop()

    squadre = st.session_state.c16_squadre
    giornate = st.session_state.c16_giornate
    risultati = st.session_state.c16_risultati

    # RISULTATI
    st.subheader("📅 Risultati delle giornate")

    idx = 0
    for g_idx, giornata in enumerate(giornate, start=1):
        with st.expander(f"Giornata {g_idx}", expanded=False):
            for a, b in giornata:
                label = f"{a} vs {b}"
                risultati[idx] = st.selectbox(
                    label,
                    ["", "2-0", "2-1", "1-2", "0-2"],
                    index=["", "2-0", "2-1", "1-2", "0-2"].index(risultati[idx]),
                    key=f"ris_{idx}"
                )
                idx += 1

    # CLASSIFICA
    st.subheader("🏅 Classifica")
    df_classifica = calcola_classifica(giornate, risultati, squadre)
    st.dataframe(df_classifica, use_container_width=True)

    # AZIONI
    st.subheader("⚙️ Azioni torneo")
    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("🔄 Reset torneo"):
            st.session_state.clear()
            st.rerun()

    with colB:
        data = {
            "squadre": squadre,
            "giornate": giornate,
            "risultati": risultati,
        }
        st.download_button(
            "💾 Salva torneo",
            data=json.dumps(data).encode("utf-8"),
            file_name="torneo_16_squadre.json",
            mime="application/json",
        )

    with colC:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_classifica.to_excel(writer, sheet_name="Classifica", index=False)
        st.download_button(
            "📊 Esporta Excel",
            data=output.getvalue(),
            file_name="classifica_16_squadre.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
