import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataPilot AI", page_icon="⚡", layout="wide")

st.sidebar.title("⚡ DataPilot AI")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Insights"],
    key="main_nav"
)

st.title("⚡ DataPilot AI")
st.write("Upload a CSV or Excel file to begin analysis.")

file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    rows, cols = df.shape
    missing = int(df.isnull().sum().sum())

    if page == "Dashboard":
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", rows)
        c2.metric("Columns", cols)
        c3.metric("Missing", missing)

        st.dataframe(df, use_container_width=True)

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:
            col = st.selectbox("Column", numeric_cols, key="chart_col")
            fig = px.histogram(df, x=col)
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Insights":
        st.subheader("Insights")
        st.write(f"Rows: {rows}")
        st.write(f"Columns: {cols}")
        st.write(f"Missing Values: {missing}")