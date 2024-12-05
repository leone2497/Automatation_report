import pandas as pd
import streamlit as st

# Funzione KPI_2
def KPI_2(row):
    """
    Calcola il KPI 2 basato sul rapporto tra operatori per run e operatori disponibili giornalmente.
    """
    rapporto = row["Numero Medio Operatori per Run di Schedulazione"] / row["Numero Medio Giornaliero Operatori Disponibili"]
    if rapporto > 1:
        return 1
    elif rapporto > 0:
        return rapporto
    else:
        return 0

st.title("Qualità di schedulazione")
uploaded_file = st.file_uploader("Carica un file", type=["csv", "txt", "xlsx"])

# Controllo se un file è stato caricato
if uploaded_file is not None:
    st.write("Nome del file:", uploaded_file.name)

    # Caricamento del file in base al tipo
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        selected_sheet = st.selectbox("Seleziona un foglio", sheet_names)
        data = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
    else:
        st.write("Formato file non supportato.")
        data = None

    if data is not None:
        st.write("Anteprima del file caricato:")
        st.dataframe(data)

        # Controlla se le colonne richieste sono presenti
        required_columns = [
            "Periodo", "Centro", "% reale Utilizzo Schedulatore", 
            "Numero Medio Operatori per Run di Schedulazione", 
            "Numero Medio Giornaliero Operatori Disponibili", 
            "Orizzonte Medio"
        ]
        if all(col in data.columns for col in required_columns):
            # Calcolo dei KPI
            data["KPI 1"] = data["% reale Utilizzo Schedulatore"] / 100
            data["KPI 2"] = data.apply(KPI_2, axis=1)
            data["KPI 3"] = data["Orizzonte Medio"]
            data["KPI 4"] = data["% reale Utilizzo Schedulatore"] / 100  # Aggiorna logica se necessario
            data["KPI 5"] = data["% reale Utilizzo Schedulatore"] / 100  # Aggiorna logica se necessario

            # Mostra il risultato
            st.write("KPI SCHEDULAZIONE:")
            st.dataframe(data[["Periodo", "Centro", "KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5"]])
        else:
            st.write("Il file caricato non contiene tutte le colonne richieste:")
            st.write(", ".join(required_columns))
else:
    st.write("Nessun file caricato.")
