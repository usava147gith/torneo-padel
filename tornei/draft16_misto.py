import streamlit as st
import pandas as pd
from io import BytesIO
from .logiche.logica_draft16_misto import build_schedule

def run():
    st.header("Draft misto 16 giocatori")

    st.markdown("Inserisci i nomi di 8 uomini e 8 donne.")

    st.subheader("Uomini")
    uomini = []
    col1, col2 = st.columns(2)
    with col1:
        for i in range(1, 5):
            uomini.append(st.text_input(f"Uomo {i}", value=f"U{i}"))
    with col2:
        for i in range(5, 9):
            uomini.append(st.text_input(f"Uomo {i}", value=f"U{i}"))

    st.subheader("Donne")
    donne = []
    col3, col4 = st.columns(2)
    with col3:
        for i in range(1, 5):
            donne.append(st.text_input(f"Donna {i}", value=f"D{i}"))
    with col4:
        for i in range(5, 9):
            donne.append(st.text_input(f"Donna {i}", value=f"D{i}"))

    if st.button("Genera calendario draft misto 16"):
        df_cal = build_schedule(uomini, donne)

        st.success("Calendario generato!")
        st.subheader("Calendario")
        st.dataframe(df_cal)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_cal.to_excel(writer, sheet_name="Calendario", index=False)

        st.download_button(
            label="Scarica Excel draft misto 16",
            data=output.getvalue(),
            file_name="draft16_misto.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
