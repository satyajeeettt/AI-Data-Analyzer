import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DataPilot AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 DataPilot AI")
st.caption("Your AI Copilot for Data Analysis")

st.sidebar.header("📂 Controls")

file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if file:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.sidebar.success("✅ File Loaded Successfully")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("📋 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Summary Statistics")

    try:
        st.dataframe(df.describe(), use_container_width=True)
    except:
        st.warning("No numeric columns available.")

    st.subheader("🔍 Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isnull().sum().values
    })

    st.dataframe(missing_df, use_container_width=True)

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        st.subheader("📈 Interactive Visualization")

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Histogram", "Box Plot"]
        )

        selected_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        if chart_type == "Histogram":
            fig = px.histogram(df, x=selected_col)
        else:
            fig = px.box(df, y=selected_col)

        st.plotly_chart(fig, use_container_width=True)

    if len(numeric_cols) > 1:

        st.subheader("🔥 Correlation Heatmap")

        corr_matrix = df[numeric_cols].corr()

        heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto"
        )

        st.plotly_chart(
            heatmap,
            use_container_width=True
        )

    st.subheader("🤖 AI Insights")

    if st.button("Generate Insights"):

        st.success("Analysis Completed")

        st.write(
            f"📌 Dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
        )

        missing_count = int(df.isnull().sum().sum())

        st.write(
            f"📌 Total Missing Values: {missing_count}"
        )

        if len(numeric_cols) > 1:

            corr = df[numeric_cols].corr()

            strongest_corr = (
                corr.unstack()
                .sort_values(ascending=False)
            )

            strongest_corr = strongest_corr[
                strongest_corr < 1
            ]

            if len(strongest_corr) > 0:

                col_a = strongest_corr.index[0][0]
                col_b = strongest_corr.index[0][1]

                st.write(
                    f"📌 Strongest relationship found between {col_a} and {col_b}."
                )

        st.write("### 💡 Recommendations")

        st.write("✅ Clean missing values before advanced analysis.")
        st.write("✅ Focus on highly correlated features.")
        st.write("✅ Analyze trends and outliers.")
        st.write("✅ Collect more data for better predictions.")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Dataset",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )