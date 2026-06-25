
def detect_drift(old_df,new_df):

    drift_report = {}

    for col in old_df.select_dtypes(include="number").columns:

        old_mean = old_df[col].mean()
        new_mean = new_df[col].mean()

        drift = abs(old_mean - new_mean)

        drift_report[col] = drift

    return drift_report
