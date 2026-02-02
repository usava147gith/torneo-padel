import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from .logiche.logica_draft12 import solve_draft12


def calcola_metriche(df_cal, names):
    """Ritorna df_compagni, df_avversari."""
    n = len(names)
    compagni = np.zeros((n, n), dtype=int)
    avversari = np.zeros((n, n), dtype=int)

    name_to_idx = {name: i for i, name in enumerate(names)}

    for _, row in df_cal.iterrows():
        a1, a2 = row["Coppia A"].split(" & ")
        b1, b2 = row["Coppia B"].split(" & ")

        i1, i2 = name_to_idx[a1], name_to_idx[a2]
        j1, j2 = name_to_idx[b1], name_to_idx[b2]

        # Compagni
        compagni[i1, i2] += 1
        compagni[i2, i1] += 1
        compagni[j1, j2] += 1
        compagni[j2, j1] += 1

        # Avversari
        for x in [i1, i2]:
            for y in [j1, j2]:
                avversari[x, y] += 1
                avversari[y, x] += 1

    df_compagni = pd.DataFrame(compagni, index=names, columns=names)
    df_avversari = pd.DataFrame(avversari, index=names, columns=names)
    return df_compagni, df_avversari


def calcola_classifica(df_cal, names):
    """Classifica basata sui game vinti (X-Y → X punti a A, Y a B)."""
    classifica = {
        nome: {
            "Punti": 0,
            "Game_vinti": 0,
            "Game_persi": 0,
            "Diff_game": 0,
            "Partite_giocate": 0,
        }
        for nome in names
    }

    for _, row in df_cal.iterrows():
        risultato = row.get("Risultato", "")
        if not risultato:
            continue

        try:
            ga, gb = map(int, risultato.replace(" ", "").split("-"))
        except Exception:
            # risultato non valido, lo saltiamo
            continue

        a1, a2 = row["Coppia A"].split(" & ")
        b1, b2 = row["Coppia B"].split(" & ")

        # Coppia A
        for p in [a1, a2]:
            classifica[p]["Punti"] += ga
            classifica[p]["Game_vinti"] += ga
            classifica[p]["Game_persi"] += gb
            classifica[p]["Partite_giocate"] += 1

        # Coppia B
        for p in [b1, b2]:
            classifica[p]["Punti"] += gb
            classifica[p]["Game_vinti"] += gb
            classifica[p]["Game_persi"] += ga
            classifica[p]["Partite_giocate"] += 1

    for p in classifica:
        classifica[p]["Diff_game"] = (
            classifica[p]["Game_vinti"] - classifica[p]["Game_persi"]
        )

    df_classifica = pd.DataFrame.from_dict(classifica, orient="index")
    df_classifica.index.name = "Giocatore"
    df_classifica = df_classifica.sort_values(
        by=["Punti", "Diff_game", "Game_vinti"], ascending=False
    )
    return df_classifica


def run():
    st.header("Draft 12 giocatori")
    st.markdown("Inserisci i nomi dei 12 giocatori.")

    giocatori = []
    col1, col2 = st.columns(2)

    with col1:
        for i in range(1, 7):
            giocatori.append(
                st.text_input(
                    f"Giocatore {i}",
                    value=f"G{i}",
                    key=f"draft12_g{i}",
                )
            )

    with col2:
        for i in range(7, 13):
            giocatori.append(
                st.text_input(
                    f"Giocatore {i}",
                    value=f"G{i}",
                    key=f"draft12_g{i}",
                )
            )

    genera = st.button("Genera calendario draft 12", key="draft12_genera")

    if not genera:
        return

    with st.spinner("Calcolo del calendario in corso..."):
        try:
            df_cal = solve_draft12(giocatori)
        except Exception as e:
            st.error("Errore durante la generazione del calendario draft 12.")
            st.code(str(e))
            return

    st.success("Calendario generato!")
    st.subheader("Calendario")

    # Colonna risultati (vuota all'inizio)
    if "draft12_risultati" not in st.session_state:
        st.session_state.draft12_risultati = [""] * len(df_cal)

    # UI per inserire i risultati
    st.markdown("### Inserisci i risultati (formato es. 5-0)")
    for i in range(len(df_cal)):
        partita_label = (
            f"Turno {df_cal.loc[i, 'Turno']} - Campo {df_cal.loc[i, 'Campo']}: "
            f"{df_cal.loc[i, 'Coppia A']} vs {df_cal.loc[i, 'Coppia B']}"
        )
        st.session_state.draft12_risultati[i] = st.text_input(
            partita_label,
            value=st.session_state.draft12_risultati[i],
            key=f"draft12_ris_{i}",
        )

    df_cal["Risultato"] = st.session_state.draft12_risultati
    st.dataframe(df_cal, use_container_width=True)

    # METRICHE
    st.markdown("### Metriche torneo")
    df_compagni, df_avversari = calcola_metriche(df_cal, giocatori)

    st.markdown("#### Matrice compagni (quante volte hanno giocato insieme)")
    st.dataframe(df_compagni, use_container_width=True)

    st.markdown("#### Matrice avversari (quante volte si sono affrontati)")
    st.dataframe(df_avversari, use_container_width=True)

    # CLASSIFICA
    st.markdown("### Classifica (basata sui game vinti)")
    df_classifica = calcola_classifica(df_cal, giocatori)
    st.dataframe(df_classifica, use_container_width=True)

    # EXPORT EXCEL
    st.markdown("### Esporta in Excel")

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_cal.to_excel(writer, sheet_name="Calendario", index=False)
        df_compagni.to_excel(writer, sheet_name="Compagni")
        df_avversari.to_excel(writer, sheet_name="Avversari")
        df_classifica.to_excel(writer, sheet_name="Classifica")

    st.download_button(
        label="Scarica Excel draft 12 completo",
        data=output.getvalue(),
        file_name="draft12_completo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="draft12_download",
    )
