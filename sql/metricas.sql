CREATE OR REPLACE TABLE distancia_base_km AS 

WITH distancias AS (
    SELECT 
    ID_MUNICIPIO,

    -- Distância Haversine até Betim:
    (
        6371 * 2 * ASIN(
            SQRT(
                POWER(SIN(RADIANS(latitude - (-19.9668)) / 2), 2)
                +
                COS(RADIANS(-19.9668))
                * COS(RADIANS(latitude))
                * POWER(SIN(RADIANS(longitude - (-44.2008)) / 2), 2)
            )
        )
    ) AS distancia_betim_km,

    -- Distância Haversine até Oliveira:
    (
        6371 * 2 * ASIN(
            SQRT(
                POWER(SIN(RADIANS(latitude - (-20.6982)) / 2), 2)
                +
                COS(RADIANS(-20.6982))
                * COS(RADIANS(latitude))
                * POWER(SIN(RADIANS(longitude - (-44.8290)) / 2), 2)
            )
        )
    ) AS distancia_oliveira_km

    FROM coordenadas_municipios.csv
)

SELECT 
    ID_MUNICIPIO,
    distancia_betim_km,
    distancia_betim_km,
    LEAST(
        distancia_betim_km,
        distancia_oliveira_km
    ) AS distancia_base_km,

    CASE
        WHEN distancia_betim_km <= distancia_oliveira_km
            THEN 3106705 -- ID de Betim
        ELSE 3145604 -- ID de Oliveira
    
    END AS base_referencia

FROM distancias
