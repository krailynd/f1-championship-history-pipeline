-- ====================================================================
-- F1 Championship History — Consultas Analíticas de Negocio y Deporte
-- ====================================================================

-- 1. Dominio de Constructores: Campeonatos ganados por equipo
SELECT 
    constructor, 
    COUNT(*) AS titulos_mundiales,
    SUM(wins) AS victorias_totales,
    ROUND(AVG(points), 2) AS promedio_puntos_temporada
FROM driver_standings
WHERE position = 1
GROUP BY constructor
ORDER BY titulos_mundiales DESC, victorias_totales DESC;

-- 2. Tasa de Efectividad: Pilotos con mayor ratio de victorias por temporada
SELECT 
    driver_name,
    COUNT(DISTINCT season) AS temporadas_disputadas,
    SUM(wins) AS victorias_acumuladas,
    SUM(points) AS puntos_totales,
    ROUND(CAST(SUM(wins) AS FLOAT) / COUNT(DISTINCT season), 2) AS victorias_por_temporada
FROM driver_standings
GROUP BY driver_name
HAVING victorias_acumuladas > 0
ORDER BY victorias_por_temporada DESC;

-- 3. Brecha de Puntos entre el Campeón (P1) y el Subcampeón (P2)
WITH P1 AS (
    SELECT season, driver_name AS campeon, points AS puntos_p1
    FROM driver_standings WHERE position = 1
),
P2 AS (
    SELECT season, driver_name AS subcampeon, points AS puntos_p2
    FROM driver_standings WHERE position = 2
)
SELECT 
    P1.season,
    P1.campeon,
    P1.puntos_p1,
    P2.subcampeon,
    P2.puntos_p2,
    ROUND(P1.puntos_p1 - P2.puntos_p2, 1) AS brecha_de_puntos,
    ROUND(((P1.puntos_p1 - P2.puntos_p2) / P1.puntos_p1) * 100, 2) AS margen_porcentual_dominio
FROM P1
JOIN P2 ON P1.season = P2.season
ORDER BY P1.season DESC;
