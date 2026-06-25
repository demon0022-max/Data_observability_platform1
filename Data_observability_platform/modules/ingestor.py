from sqlalchemy import create_engine
import pandas as pd
def load_file(file):
    name = file.name
    if name.endswith(".csv"):
        return pd.read_csv(file)
    if name.endswith(".json"):
        return pd.read_json(file)
    if name.endswith(".xlsx"):
        return pd.read_excel(file)
def load_database():
    connection = "postgresql+psycopg2://postgres:2006@localhost:5432/ai_data_platform"
    engine = create_engine(connection)
    # ✅ FIX (use raw_connection)
    conn = engine.raw_connection()
    df = pd.read_sql("SELECT * FROM data_table", conn)
    conn.close()
    return df
