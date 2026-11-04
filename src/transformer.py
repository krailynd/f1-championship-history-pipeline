import pandas as pd

def parse_driver_standings(raw_json: dict) -> list[dict]:
    """Aplana la respuesta JSON anidada de Ergast/Jolpica a registros tabulares."""
    standings_lists = raw_json.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not standings_lists:
        return []
    
    season = int(standings_lists[0].get("season", 0))
    round_num = int(standings_lists[0].get("round", 0))
    results = []
    
    for row in standings_lists[0].get("DriverStandings", []):
        driver = row.get("Driver", {})
        constructors = row.get("Constructors", [])
        constructor_name = constructors[0].get("name") if constructors else "Unknown"
        
        results.append({
            "season": season,
            "round": round_num,
            "position": int(row.get("position", 0)),
            "points": float(row.get("points", 0.0)),
            "wins": int(row.get("wins", 0)),
            "driver_id": driver.get("driverId"),
            "driver_code": driver.get("code", "N/A"),
            "driver_name": f"{driver.get('givenName', '')} {driver.get('familyName', '')}".strip(),
            "nationality": driver.get("nationality"),
            "constructor": constructor_name
        })
    return results
