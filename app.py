import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Data Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyzer")

file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if file:

    df = pd.read_csv(file)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values",
                  df.isnull().sum().sum())

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.subheader("Missing Values")

    st.dataframe(
        df.isnull().sum().reset_index().rename(
            columns={
                "index": "Column",
                0: "Missing Count"
            }
        )
    )

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_cols) > 0:

        st.subheader("Interactive Chart")

        selected_col = st.selectbox(
            "Choose Column",
            numeric_cols
        )

        fig = px.histogram(
            df,
            x=selected_col
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )