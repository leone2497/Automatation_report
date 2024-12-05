import pandas as pd
import streamlit as st
import itertools
st.title("Qualità di schedulazione")
uploaded_file = st.file_uploader("Carica un file", type=["csv", "txt", "xlsx"])
st.write("Nome del file:", uploaded_file.name)

    # Leggi il contenuto del file in base al tipo
    if uploaded_file.name.endswith('.csv'):
        import pandas as pd
        data = pd.read_csv(uploaded_file)
        st.write("Anteprima del file CSV:")
        st.dataframe(data)

    elif uploaded_file.name.endswith('.txt'):
        # Leggi file di testo
        content = uploaded_file.read().decode("utf-8")
        st.write("Contenuto del file:")
        st.text(content)

    elif uploaded_file.name.endswith('.xlsx'):
        import pandas as pd
        data = pd.read_excel(uploaded_file)
        st.write("Anteprima del file Excel:")
        st.dataframe(data)

else:
    st.write("Nessun file caricato")
