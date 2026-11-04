import argparse
from tqdm import tqdm
import pandas as pd
from src.client import get_season_standings
from src.transformer import parse_driver_standings
from src.database import save_to_sqlite_and_parquet

def main():
    parser = argparse.ArgumentParser(description="F1 Championship History ETL Pipeline")
    parser.add_argument("--start", type=int, default=2019, help="Año de inicio de extracción")
    parser.add_argument("--end", type=int, default=2024, help="Año final de extracción")
    args = parser.parse_args()

    print(f"🚀 Iniciando pipeline ETL Jolpica-F1 (Temporadas {args.start} a {args.end})...")
    all_records = []
    
    for season in tqdm(range(args.start, args.end + 1), desc="Descargando temporadas"):
        try:
            raw = get_season_standings(season)
            records = parse_driver_standings(raw)
            all_records.extend(records)
        except Exception as e:
            print(f"\n⚠️ Error en temporada {season}: {e}")
            
    if not all_records:
        print("❌ No se obtuvieron registros.")
        return

    df = pd.DataFrame(all_records)
    print(f"\n✨ Extracción completa: {len(df)} filas procesadas.")
    save_to_sqlite_and_parquet(df)
    
    print("\n🏁 Top 5 Campeones del período extraído:")
    champions = df[df['position'] == 1][['season', 'driver_name', 'constructor', 'wins', 'points']]
    print(champions.to_string(index=False))

if __name__ == "__main__":
    main()
