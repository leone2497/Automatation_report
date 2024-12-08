import pandas as pd
import streamlit as st

Sbarramento= {'KPI':[1,2,3,4,5],
              'Peso':[0.35,0.1,0.15,0.15,0.25],
              'Soglia inferiore':[0.45,0.25,2,0.55,2],
              'Soglia superiore':[0.6,0.5,4,0.75,5],
              'Sbarramento':[0.25,0.15,1.5,0.4,10]
    }



# Function for KPI_2 calculation
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

# Title
st.title("Qualità di schedulazione")

# Step 1: File upload and preprocessing
st.header("Step 1: Caricamento e Preprocessing del File")
uploaded_file = st.file_uploader("Carica un file", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.write("Nome del file:", uploaded_file.name)

    # File loading
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file, header=None)
    elif uploaded_file.name.endswith('.xlsx'):
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        selected_sheet = st.selectbox("Seleziona un foglio", sheet_names)
        data = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=None)
    else:
        st.write("Formato file non supportato.")
        data = None

    if data is not None:
        st.write("Anteprima del file caricato:")
        st.dataframe(data)

        # Header selection
        row_for_header = st.slider("Seleziona la riga da usare come header", 0, len(data) - 1, 0)
        if row_for_header >= 0:
            data.columns = data.iloc[row_for_header]
            data = data.drop(index=row_for_header).reset_index(drop=True)
            st.write(f"DataFrame aggiornato con la riga {row_for_header} come header:")
            st.dataframe(data)

        # Row deletion
        rows_to_delete = st.slider("Seleziona quante righe vuoi eliminare", 0, len(data), 0)
        if rows_to_delete > 0:
            data = data.iloc[rows_to_delete:].reset_index(drop=True)
            st.write(f"DataFrame dopo la rimozione delle prime {rows_to_delete} righe:")
            st.dataframe(data)

        # Save the preprocessed data in a session state for later steps
        st.session_state["preprocessed_data"] = data

# Step 2: KPI calculation and controls
if "preprocessed_data" in st.session_state:
    st.header("Step 2: Calcolo KPI e Validazione")
    data = st.session_state["preprocessed_data"]

    required_columns = [
        "Periodo", "Centro", "% reale Utilizzo Schedulatore",
        "Numero Medio Operatori per Run di Schedulazione",
        "Numero Medio Giornaliero Operatori Disponibili",
        "Orizzonte Medio"
    ]

    # Validate if required columns exist
    if all(col in data.columns for col in required_columns):
        # KPI calculations
        data["KPI 1"] = data["% reale Utilizzo Schedulatore"] / 100
        data["KPI 2"] = data.apply(KPI_2, axis=1)
        data["KPI 3"] = data["Orizzonte Medio"]
        data["KPI 4"] = data["% Media Odl Validi e Schedulati"] / 100 
        data["KPI 5"] = data["Numero Run"] / 21 

        # Display calculated KPIs
        st.write("KPI SCHEDULAZIONE:")
        st.dataframe(data[["Periodo", "Centro", "KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5"]])
    else:
        st.write("Il file caricato non contiene tutte le colonne richieste:")
        st.write(", ".join(required_columns))
