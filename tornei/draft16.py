import streamlit as st
import pandas as pd
from io import BytesIO
from .logiche.logica_draft16 import solve_draft16

def run():
    st.header("Draft 16 giocatori")

    st.markdown("Inserisci i nomi dei 16 giocatori.")

    giocatori = []
    col1, col2 = st.columns(2)
    with col1:
        for i in range(1, 9):
            giocatori.append(st.text_input(f"Giocatore {i}", value=f"G{i}"))
    with col2:
        for i in range(9, 17):
            giocatori.append(st.text_input(f"Giocatore {i}", value=f"G{i}"))

    if st.button("Genera calendario draft 16"):
        df_cal = solve_draft16(giocatori)

        st.success("Calendario generato!")
        st.subheader("Calendario")
        st.dataframe(df_cal)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_cal.to_excel(writer, sheet_name="Calendario", index=False)

        st.download_button(
            label="Scarica Excel draft 16",
            data=output.getvalue(),
            file_name="draft16.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
