import sqlite3
from pathlib import Path
import pandas as pd

def save_to_sqlite_and_parquet(df: pd.DataFrame, db_path: str = "data/f1_history.sqlite", parquet_path: str = "data/driver_standings.parquet"):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Guardar en SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql("driver_standings", conn, if_exists="replace", index=False)
    conn.close()
    
    # 2. Guardar en Apache Parquet
    df.to_parquet(parquet_path, index=False, engine="pyarrow")
    print(f"✓ Guardado en SQLite: {db_path} ({len(df)} registros)")
    print(f"✓ Exportado a Parquet: {parquet_path}")
