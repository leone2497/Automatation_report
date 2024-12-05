import pandas as pd
import streamlit as st

st.title("Qualità di schedulazione")
uploaded_file = st.file_uploader("Carica un file", type=["csv", "txt", "xlsx"])

# Controllo se un file è stato caricato
if uploaded_file is not None:
    st.write("Nome del file:", uploaded_file.name)

    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
        st.write("Anteprima del file CSV:")
        st.dataframe(data)

    elif uploaded_file.name.endswith('.txt'):
        # Leggi file di testo
        content = uploaded_file.read().decode("utf-8")
        st.write("Contenuto del file:")
        st.text(content)

    elif uploaded_file.name.endswith('.xlsx'):
        # Leggi i nomi dei fogli nell'Excel
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names

        # Crea un menu a tendina per selezionare il foglio
        selected_sheet = st.selectbox("Seleziona un foglio", sheet_names)

        # Leggi il foglio selezionato
        data = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        st.write(f"Anteprima del foglio: {selected_sheet}")
        st.dataframe(data)

else:
    st.write("Nessun file caricato")
