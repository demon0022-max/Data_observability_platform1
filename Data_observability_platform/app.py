import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  
from modules.ingestor import load_file, load_database
from modules.profiler import profile_data, data_quality_score
from modules.zscore import zscore_detect
from modules.isolation import isolation_forest_detect
from modules.lof import lof_detect
from modules.drift import detect_drift
from modules.dashboard import show_dashboard
from modules.rca import root_cause_analysis
st.title("Data Observability Platform")
menu = st.sidebar.selectbox("Menu",[
"Upload File",
"Load Database",
"Dashboard",
"Profile Data",
"ZScore Detection",
"Isolation Forest",
"LOF Detection",
"Root Cause Analysis",
"Data Drift"
])
if "data" not in st.session_state:
    st.session_state.data = None
if menu == "Upload File":
    file = st.file_uploader("Upload dataset", type=["csv","json","xlsx"])
    if file:
        df = load_file(file)
        st.session_state.data = df
        st.dataframe(df.head())
if menu == "Load Database":
    df = load_database()
    st.session_state.data = df
    st.dataframe(df.head())
if menu == "Dashboard":
    show_dashboard(st.session_state.data)
if menu == "Profile Data":
    if st.session_state.data is not None:
        df = st.session_state.data
        st.subheader("Dataset Profile")
        st.write(profile_data(df))
        score = data_quality_score(df)
        st.metric("Data Quality Score", f"{score}%")
        z_df = zscore_detect(df.copy())
        iso_df = isolation_forest_detect(df.copy())
        lof_df = lof_detect(df.copy())
        z_anomalies = z_df["zscore_anomaly"].sum() if "zscore_anomaly" in z_df.columns else 0
        iso_anomalies = (iso_df["iso_anomaly"] == -1).sum()
        lof_anomalies = (lof_df["lof_anomaly"] == -1).sum()
        st.subheader("Anomaly Detection Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Z-Score", z_anomalies)
        col2.metric("Isolation Forest", iso_anomalies)
        col3.metric("LOF", lof_anomalies)
        chart_data = pd.DataFrame({
            "Model": ["Z-Score","Isolation Forest","LOF"],
            "Anomalies":[z_anomalies, iso_anomalies, lof_anomalies]
        })
        st.subheader("Model Comparison Chart")
        st.bar_chart(chart_data.set_index("Model"))
    else:
        st.warning("Load data first")
if menu == "ZScore Detection":
    if st.session_state.data is not None:
        st.dataframe(zscore_detect(st.session_state.data))
if menu == "Isolation Forest":
    if st.session_state.data is not None:
        df = isolation_forest_detect(st.session_state.data)
        st.dataframe(df)
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column for visualization", numeric_cols)
            normal = df[df["iso_anomaly"] == 1]
            anomaly = df[df["iso_anomaly"] == -1]
            st.subheader("Anomaly Points")
            if not anomaly.empty:
                selected_index = st.selectbox(
                    "Select anomaly to highlight",
                     anomaly.index.tolist()
                )
                selected_row = anomaly.loc[selected_index]
                st.dataframe(anomaly)
                fig, ax = plt.subplots()
                ax.scatter(normal.index, normal[col], label="Normal")
                ax.scatter(anomaly.index, anomaly[col], label="Anomaly")
                ax.scatter(
                    selected_index,
                    selected_row[col],
                    s=200,
                    color="red",
                    edgecolors="black",
                    label="Selected"
                )
                ax.set_xlabel("Index")
                ax.set_ylabel(col)
                ax.legend()
                st.pyplot(fig)
            else:
                st.warning("No anomalies detected")
        else:
            st.warning("No numeric columns available")
if menu == "LOF Detection":
    if st.session_state.data is not None:
        df = lof_detect(st.session_state.data)
        st.dataframe(df)
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column for visualization", numeric_cols)
            st.subheader("LOF Anomaly Visualization")
            normal = df[df["lof_anomaly"] == 1]
            anomaly = df[df["lof_anomaly"] == -1]
            st.line_chart(df[col])
            st.write("Anomaly Points")
            st.dataframe(anomaly)
if menu == "Root Cause Analysis":
    if st.session_state.data is not None:
        causes = root_cause_analysis(st.session_state.data)
        st.subheader("Root Cause Columns")
        for col, count in causes:
            st.write(f"{col} → {count} anomalies detected")
    else:
        st.warning("Load data first")
if menu == "Data Drift":
    old_file = st.file_uploader("Upload reference dataset")
    new_file = st.file_uploader("Upload new dataset")
    if old_file and new_file:
        old_df = pd.read_csv(old_file)
        new_df = pd.read_csv(new_file)
        st.write(detect_drift(old_df, new_df))