import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DataPilot AI",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}
.metric-card {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🚀 DataPilot AI")
st.sidebar.markdown("### Your AI Copilot for Data Analysis")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Insights"]
)

# Header
st.title("🚀 DataPilot AI")
st.caption("Transform your data into actionable insights")

file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if file:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(df.isnull().sum().sum())

    quality_score = round(
        ((rows * cols - missing) / (rows * cols)) * 100,
        2
    )

    if page == "Dashboard":

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("📄 Rows", rows)
        col2.metric("📊 Columns", cols)
        col3.metric("⚠ Missing Values", missing)
        col4.metric("🏆 Data Quality", f"{quality_score}%")

        st.markdown("---")

        st.subheader("📋 Dataset Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Summary Statistics")

        try:
            st.dataframe(
                df.describe(),
                use_container_width=True
            )
        except:
            st.info("No numeric columns found.")

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_cols) > 0:

            st.subheader("📊 Visualization Center")

            chart_type = st.selectbox(
                "Select Chart",
                [
                    "Histogram",
                    "Box Plot",
                    "Scatter Plot",
                    "Line Chart",
                    "Pie Chart"
                ]
            )

            selected_col = st.selectbox(
                "Select Column",
                numeric_cols
            )

            if chart_type == "Histogram":
                fig = px.histogram(
                    df,
                    x=selected_col
                )

            elif chart_type == "Box Plot":
                fig = px.box(
                    df,
                    y=selected_col
                )

            elif chart_type == "Line Chart":
                fig = px.line(
                    df,
                    y=selected_col
                )

            elif chart_type == "Pie Chart":

                pie_data = (
                    df[selected_col]
                    .value_counts()
                    .head(10)
                    .reset_index()
                )

                pie_data.columns = [
                    selected_col,
                    "Count"
                ]

                fig = px.pie(
                    pie_data,
                    names=selected_col,
                    values="Count"
                )

            elif chart_type == "Scatter Plot":

                second_col = st.selectbox(
                    "Second Column",
                    numeric_cols
                )

                fig = px.scatter(
                    df,
                    x=selected_col,
                    y=second_col
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

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

    if page == "Insights":

        st.subheader("🤖 DataPilot Insights")

        st.success("Analysis Generated Successfully")

        st.write(
            f"Dataset contains **{rows} rows** and **{cols} columns**."
        )

        st.write(
            f"Total missing values detected: **{missing}**"
        )

        st.write(
            f"Data quality score: **{quality_score}%**"
        )

        if quality_score > 95:
            st.success(
                "Excellent data quality."
            )

        elif quality_score > 80:
            st.warning(
                "Good quality but cleaning recommended."
            )

        else:
            st.error(
                "Significant data cleaning required."
            )

        st.markdown("### 💡 Recommendations")

        st.write(
            "✅ Remove missing values before modeling."
        )

        st.write(
            "✅ Focus on highly correlated features."
        )

        st.write(
            "✅ Investigate outliers."
        )

        st.write(
            "✅ Build dashboards for business monitoring."
        )

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Dataset",
        csv,
        "cleaned_data.csv",
        "text/csv"
    )

else:

    st.info(
        "Upload a CSV or Excel file to begin analysis."
    )

st.markdown("---")

st.markdown(
    """
    <div class='footer'>
    🚀 DataPilot AI | Built by Satyjeet
    </div>
    """,
    unsafe_allow_html=True
)