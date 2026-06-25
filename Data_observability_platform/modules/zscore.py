
import pandas as pd

def zscore_detect(df):

    numeric = df.select_dtypes(include="number")

    z = (numeric - numeric.mean()) / numeric.std()

    anomalies = (abs(z) > 3)

    return df[anomalies.any(axis=1)]
