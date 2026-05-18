CREATE OR REPLACE TABLE metricas_logisticas AS 

-- Resumo das métricas:

-- dist_base_principal_km   : Distância (km) do município em questão até a base principal, em betim
-- dist_base_oliveira_km    : Distância (km) do município em questão até a base em Oliveira
-- base_atendimento         : ID da base responsável (Betim ou Oliveira) pelo atendimento do município
-- dist_base_atendimento_km : Distância (km) do município em questão até a base responsável pelo atendimento do município

WITH distancias AS (
    SELECT 
        id_municipio,

        -- Distância Haversine do município selecionado até Betim:
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
        ) AS dist_base_principal_km,

        -- Distância Haversine do município selecionado até Oliveira:
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
        ) AS dist_base_oliveira_km

    FROM coordenadas_municipios
)

SELECT 
    id_municipio,
    dist_base_principal_km,
    dist_base_oliveira_km,

    LEAST(
        dist_base_principal_km,
        dist_base_oliveira_km
    ) AS dist_base_atendimento_km,

    CASE
        WHEN dist_base_principal_km <= dist_base_oliveira_km
            THEN 3106705 -- ID de Betim
        ELSE 3145604 -- ID de Oliveira
    
    END AS base_atendimento,

FROM distancias
