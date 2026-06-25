def profile_data(df):
    report = {}
    report["rows"] = df.shape[0]
    report["columns"] = df.shape[1]
    report["null_values"] = df.isnull().sum().to_dict()
    report["duplicates"] = int(df.duplicated().sum())
    return report
def data_quality_score(df):
    total_cells = df.size
    null_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    quality = 100 - ((null_cells + duplicate_rows) / total_cells * 100)
    return round(quality,2)
