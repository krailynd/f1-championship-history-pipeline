import time
import requests

BASE_URL = "http://api.jolpi.ca/ergast/f1"

def fetch_with_retry(url: str, params: dict = None, max_retries: int = 4, delay: float = 1.0) -> dict:
    """Realiza peticiones GET con reintentos exponenciales para tolerar rate limits y microcortes."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=12)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code in (429, 500, 502, 503):
                wait = delay * (2 ** attempt)
                time.sleep(wait)
            else:
                resp.raise_for_status()
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay * (2 ** attempt))
    raise RuntimeError(f"Fallo al consultar URL después de {max_retries} intentos: {url}")

def get_season_standings(season: int) -> dict:
    """Descarga los standings finales de pilotos de una temporada específica."""
    url = f"{BASE_URL}/{season}/driverstandings.json"
    data = fetch_with_retry(url)
    return data
