from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
import streamlit as st

def lof_detect(df):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        st.warning("No numeric columns available")
        return df

    # remove columns with all NaN values
    numeric = numeric.dropna(axis=1, how="all")

    # fill missing values
    numeric = numeric.fillna(numeric.mean())

    # adjust neighbors automatically
    n_neighbors = min(20, len(numeric) - 1)

    model = LocalOutlierFactor(n_neighbors=n_neighbors)

    preds = model.fit_predict(numeric)

    df["lof_anomaly"] = preds

    return df













'''from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
import streamlit as st

def lof_detect(df):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        st.warning("No numeric columns available")
        return df

    # handle missing values
    numeric = numeric.fillna(numeric.mean())

    model = LocalOutlierFactor(n_neighbors=20)

    preds = model.fit_predict(numeric)

    df["lof_anomaly"] = preds

    return df'''