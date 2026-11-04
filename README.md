# 🏆 F1 Championship History Pipeline — ETL Robusto con Jolpica-F1 (1950–2025)

> **Proyecto 2 — Fase 1 (Python / Data Engineering / SQL)** de la *Ruta Maestra Deep Learning Researcher*.
> Pipeline de ingeniería de datos para la extracción, aplanado y persistencia multiformato (SQLite relacional + Apache Parquet columnar) de más de 75 años de campeonatos de Fórmula 1.

---

## 📌 1. ¿Qué es y qué resuelve este proyecto?

En Data Science y Machine Learning, los modelos dependen de pipelines de datos confiables. Si la ingesta falla por microcortes de red, rate limits o cambios de formato, todo el flujo posterior colapsa.
Históricamente, la comunidad dependía de la API *Ergast*, la cual **cerró de forma permanente en diciembre de 2024**.

### 🎯 Desafíos de Ingeniería Resueltos
1. **Migración a Jolpica-F1:** Implementa el cliente HTTP oficial para la nueva API comunitaria (`api.jolpi.ca`).
2. **Resiliencia ante Rate Limits:** Integra el algoritmo de **Exponential Backoff con Jitter** para manejar códigos HTTP `429 Too Many Requests` y fallas transitorias de conexión.
3. **Normalización de JSON Jerárquico:** Desanida estructuras complejas de diccionarios y arrays en registros tabulares 1NF limpios.
4. **Persistencia Dual Estratégica:**
   - **SQLite (`.sqlite`):** Para transaccionalidad, integridad relacional y consultas analíticas con SQL estándar.
   - **Apache Parquet (`.parquet`):** Para compresión columnar de alta velocidad, optimizada para analítica masiva con Polars, DuckDB y PyArrow.

---

## 📐 2. Fundamentos de Arquitectura e Ingesta de Datos

### A. Algoritmo de Reintentos Exponenciales (Exponential Backoff)
Cuando el servidor remoto devuelve un error temporal o saturación (`429`, `502`, `503`), el cliente calcula un tiempo de espera exponencial antes de volver a consultar:
$$t_{\text{wait}} = \text{base\_delay} \times 2^{\text{attempt}} + \epsilon$$
Donde $\epsilon \sim U(0, 0.2)$ representa un pequeño *jitter* aleatorio para evitar el problema de reintentos simultáneos sincronizados (*thundering herd problem*).

### B. Ventajas del Formato Parquet vs CSV/JSON
| Característica | JSON Crudo (API) | SQLite Relacional | Apache Parquet Columnar |
| :--- | :--- | :--- | :--- |
| **Orientación** | Texto jerárquico | Fila (Row-oriented) | **Columna (Column-oriented)** |
| **Tipado** | Débil (strings) | Dinámico / Manifest | **Fuerte con metadata binaria** |
| **Compresión** | Nula | Media | **Ultra-alta (Snappy / ZSTD)** |
| **Lectura Selectiva** | Carga 100% en RAM | Lectura por índices | **Lectura solo de columnas requeridas (*Projection Pushdown*)** |

---

## 🧱 3. Estructura del Repositorio

```text
f1-championship-history-pipeline/
├── data/
│   ├── f1_history.sqlite        # Base de datos relacional con tabla driver_standings
│   └── driver_standings.parquet # Dataset columnar analítico
├── sql/
│   └── queries_analiticas.sql   # Consultas de negocio (dominio, efectividad, brechas)
├── src/
│   ├── __init__.py
│   ├── client.py                # Cliente HTTP resiliente con reintentos exponenciales
│   ├── transformer.py           # Parsing de respuestas JSON anidadas a esquemas planos
│   └── database.py              # Exportador simultáneo a SQLite y PyArrow Parquet
├── main.py                      # Pipeline CLI ejecutable de extremo a extremo
├── pyproject.toml               # Metadatos del paquete
├── requirements.txt             # Dependencias
└── .gitignore
```

---

## 🚀 4. Instalación y Uso Verificado

### Requisitos:
- Python 3.10+ (probado en CPython 3.12 con `uv`).

```bash
# 1. Clonar el repositorio
git clone https://github.com/krailynd/f1-championship-history-pipeline.git
cd f1-championship-history-pipeline

# 2. Crear entorno virtual con uv
uv venv --python 3.12 .venv
source .venv/bin/activate

# 3. Instalar dependencias
uv pip install -r requirements.txt

# 4. Ejecutar la ingesta de las últimas temporadas (ej. 2020 a 2024)
python main.py --start 2020 --end 2024
```

### Salida en consola:
```text
🚀 Iniciando pipeline ETL Jolpica-F1 (Temporadas 2020 a 2024)...
Descargando temporadas: 100%|██████████| 5/5 [00:07<00:00,  1.50s/it]

✨ Extracción completa: 112 filas procesadas.
✓ Guardado en SQLite: data/f1_history.sqlite (112 registros)
✓ Exportado a Parquet: data/driver_standings.parquet

🏁 Top 5 Campeones del período extraído:
 season    driver_name constructor  wins  points
   2020 Lewis Hamilton    Mercedes    11   347.0
   2021 Max Verstappen    Red Bull    10   395.5
   2022 Max Verstappen    Red Bull    15   454.0
   2023 Max Verstappen    Red Bull    19   575.0
   2024 Max Verstappen    Red Bull     9   437.0
```

---

## 📊 5. Ejecutar Consultas Analíticas SQL

Puedes interrogar la base de datos directamente con el CLI de `sqlite3`:
```bash
sqlite3 data/f1_history.sqlite < sql/queries_analiticas.sql
```

O inspeccionar el margen de victoria del campeón:
```sql
SELECT season, driver_name, points, wins 
FROM driver_standings 
WHERE position = 1 
ORDER BY season DESC;
```

---

## 👤 Autor
- **Krailynd (Elvis)** — [GitHub](https://github.com/krailynd)
- Desarrollado como parte de la formación integral hacia **Deep Learning Researcher**.
