import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
def show_dashboard(df):
    if df is None:
        st.warning("No data loaded")
        return
    st.subheader("Dataset Overview")
    st.write(df.describe())
    numeric = df.select_dtypes(include="number")
    if len(numeric.columns) > 0:
        column = st.selectbox("Select Column", numeric.columns)
        chart_type = st.selectbox(
            "Chart Type",
            ["Normal Chart", "Show Anomalies"]
        )
        if chart_type == "Normal Chart":
            st.bar_chart(df[column])
        if chart_type == "Show Anomalies":
            if "iso_anomaly" in df.columns:
                normal = df[df["iso_anomaly"] == 1]
                anomaly = df[df["iso_anomaly"] == -1]
                fig, ax = plt.subplots()
                ax.scatter(normal.index, normal[column], label="Normal")
                ax.scatter(anomaly.index, anomaly[column], label="Anomaly")
                ax.set_title("Anomaly Detection Visualization")
                ax.legend()
                st.pyplot(fig)
                st.write("Detected Anomalies")
                st.dataframe(anomaly)
            else:
                st.warning("Run Isolation Forest first to detect anomalies")