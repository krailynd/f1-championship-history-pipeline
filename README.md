# 🏆 F1 Championship History Pipeline — ETL Robusto con Jolpica-F1 (1950–2025)

> **Proyecto 2 — Fase 1 (Python / Data Engineering)** de la *Ruta Maestra Deep Learning Researcher*.
> Extracción, transformación y carga (ETL) automatizada para datos históricos del Campeonato Mundial de Fórmula 1 desde la API Jolpica-F1 (sucesor oficial de Ergast).

---

## 📌 1. Motivación y Contexto

Durante más de 15 años, la API *Ergast* fue la fuente estándar de datos históricos de F1. Sin embargo, **Ergast cerró definitivamente a finales de 2024**. 
El reemplazo oficial y mantenido por la comunidad de código abierto es **[Jolpica-F1](https://github.com/jolpica/jolpica-f1)** (`http://api.jolpi.ca/ergast/f1/`), que extiende el historial hasta las temporadas actuales con endpoints modernos y paginación rápida.

### 🎯 Objetivos de Ingeniería
1. **Consumo resiliente de API REST:** Implementar un cliente HTTP en Python con reintentos automáticos (*exponential backoff*), timeouts adaptativos y respeto estricto de rate limits.
2. **Paginación automática:** Extraer las 75+ temporadas de historia (1950 a 2025) navegando por offsets sin pérdidas de registros.
3. **Persistencia estructurada:** Normalizar los datos en esquemas limpios en **SQLite** y en formato columnar **Parquet** para consultas analíticas instantáneas.
4. **Análisis histórico:** Generar queries analíticas y visualizaciones sobre dominio por escudería y longevidad de pilotos campeones.

---

## 🧱 2. Estructura del Repositorio

```text
f1-championship-history-pipeline/
├── data/                  # Base de datos SQLite y archivos Parquet generados
├── sql/                   # Esquemas DDL y consultas analíticas de prueba
│   └── schema.sql
├── src/                   # Módulos del pipeline ETL
│   ├── __init__.py
│   ├── client.py          # Cliente HTTP con requests/httpx y exponential backoff
│   ├── transformer.py     # Limpieza y aplanado de JSON anidado a DataFrames
│   └── database.py        # Carga en SQLite y exportación a Parquet
├── main.py                # Pipeline CLI ejecutable de extremo a extremo
├── pyproject.toml         # Configuración del paquete y entorno virtual
├── requirements.txt       # Dependencias del proyecto
└── .gitignore             # Exclusión de base de datos local y artefactos
```

---

## 🛠️ 3. Tecnologías y Stack

- **Python 3.10+** (gestión rápida con `uv`)
- **HTTPX / Requests:** Cliente HTTP síncrono/asíncrono con manejo de excepciones.
- **Pandas & PyArrow:** Aplanado de JSON anidado y exportación a Apache Parquet.
- **SQLite3:** Almacenamiento relacional ligero para queries SQL inmediatas.

---

## 🚀 4. Instalación y Uso

### Instalación de dependencias:
```bash
git clone https://github.com/krailynd/f1-championship-history-pipeline.git
cd f1-championship-history-pipeline

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Ejecutar el pipeline:
```bash
# Extraer las últimas 5 temporadas por defecto (ejecución rápida de prueba)
python main.py --start 2020 --end 2024

# O extraer el historial completo (1950 a 2024)
python main.py --start 1950 --end 2024
```

---

## 📊 5. Consultas Analíticas Incluidas (SQL)

La base de datos SQLite generada permite responder de inmediato preguntas como:
- *¿Cuáles son los pilotos con mayor porcentaje de victorias sobre carreras disputadas?*
- *¿Qué constructores dominaron cada era técnica de la Fórmula 1?*
- *¿Cuál es la evolución de puntos obtenidos por temporada normalizados según el sistema de puntuación vigente?*

---

## 👤 Autor
- **Krailynd (Elvis)** — [GitHub](https://github.com/krailynd)
- Desarrollado como parte de la formación hacia **Deep Learning Researcher**.
