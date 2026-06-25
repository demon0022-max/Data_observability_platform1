from sklearn.ensemble import IsolationForest
from modules.alerts import send_email_alert
def isolation_forest_detect(df):
    numeric = df.select_dtypes(include="number")
    model = IsolationForest(contamination=0.05, random_state=42)
    preds = model.fit_predict(numeric)
    df["iso_anomaly"] = preds
    anomalies = df[df["iso_anomaly"] == -1]
    if len(anomalies) > 0:
        send_email_alert(f"{len(anomalies)} anomalies detected in dataset")
    return df
