import pandas as pd

def root_cause_analysis(df):

    numeric = df.select_dtypes(include="number")
    mean = numeric.mean()
    std = numeric.std()
    z_scores = (numeric - mean) / std
    anomaly_columns = {}
    for col in numeric.columns:
        anomaly_count = (abs(z_scores[col]) > 3).sum()
        anomaly_columns[col] = int(anomaly_count)
    sorted_causes = sorted(
        anomaly_columns.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_causes
