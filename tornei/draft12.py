import streamlit as st
import pandas as pd
from io import BytesIO
from .logiche.logica_draft12 import solve_draft12

def run():
    st.header("Draft 12 giocatori")
    st.markdown("Inserisci i nomi dei 12 giocatori.")

    giocatori = []
    col1, col2 = st.columns(2)

    with col1:
        for i in range(1, 7):
            giocatori.append(
                st.text_input(f"Giocatore {i}", value=f"G{i}", key=f"draft12_g{i}")
            )

    with col2:
        for i in range(7, 13):
            giocatori.append(
                st.text_input(f"Giocatore {i}", value=f"G{i}", key=f"draft12_g{i}")
            )

    genera = st.button("Genera calendario draft 12")

    if genera:
        with st.spinner("Calcolo del calendario in corso..."):
            try:
                df_cal = solve_draft12(giocatori)

            except Exception as e:
                st.error("Errore durante la generazione del calendario draft 12.")
                st.code(str(e))
                return

        st.success("Calendario generato!")
        st.subheader("Calendario")
        st.dataframe(df_cal)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_cal.to_excel(writer, sheet_name="Calendario", index=False)

        st.download_button(
            label="Scarica Excel draft 12",
            data=output.getvalue(),
            file_name="draft12.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
