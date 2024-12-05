import pandas as pd
import streamlit as st

def KPI_2(Numero Medio Operatori per Run di Schedulazione, Numero Medio Giornaliero Operatori Disponibili):
    rapporto = Numero_Medio_Operatori_per_Run / Numero_Medio_Giornaliero_Operatori_Disponibili
    
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

    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file, header=None)  # Carica senza header
        st.write("Anteprima del file CSV (senza header):")
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
        data = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=None)  # Carica senza header
        st.write(f"Anteprima del foglio: {selected_sheet}")
        st.dataframe(data)

    # Aggiungi il filtro per rimuovere righe
    if isinstance(data, pd.DataFrame):  # Verifica che i dati siano un DataFrame
        # Seleziona la riga che diventerà l'header
        row_for_header = st.slider("Seleziona la riga da usare come header", 0, len(data)-1, 0)

        if row_for_header >= 0:
            # Imposta la riga selezionata come header
            data.columns = data.iloc[row_for_header]
            data = data.drop(index=row_for_header).reset_index(drop=True)

            st.write(f"DataFrame con la riga {row_for_header} come header:")
            st.dataframe(data)

        # Aggiungi il filtro per rimuovere righe
        rows_to_delete = st.slider("Seleziona quante righe vuoi eliminare", 0, len(data), 0)

        if rows_to_delete > 0:
            # Elimina le righe selezionate
            data = data.iloc[rows_to_delete:].reset_index(drop=True)
            st.write(f"Righe dopo la rimozione delle prime {rows_to_delete} righe:")
            st.dataframe(data)
        else:
            st.write("Nessuna riga eliminata.")

        # Creazione del KPI_SCHEDULAZIONE
        if "% reale Utilizzo Schedulatore" in data.columns and "Periodo" in data.columns and "Centro" in data.columns:
            data["KPI 1"] = data["% reale Utilizzo Schedulatore"] / 100
            data["KPI 2"] = KPI_2(data["Numero Medio Operatori per Run di Schedulazione"],data["Numero Medio Giornaliero Operatori Disponibili"])
            data["KPI 3"] = data["Orizzonte Medio"]
            data["KPI 4"] = data["% reale Utilizzo Schedulatore"] / 100
            data["KPI 5"] = data["% reale Utilizzo Schedulatore"] / 100
            # Seleziona e mostra solo le colonne desiderate
            st.write("KPI SCHEDULAZIONE:")
            st.dataframe(data[['Periodo', 'Centro', 'KPI 1','KPI 2', 'KPI 3', 'KPI 4', 'KPI 5']])
        else:
            st.write("Le colonne 'Periodo', 'Centro' o '% reale Utilizzo Schedulatore' non sono presenti nel file.")
else:
    st.write("Nessun file caricato")
