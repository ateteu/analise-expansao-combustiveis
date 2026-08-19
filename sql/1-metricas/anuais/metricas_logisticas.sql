CREATE OR REPLACE TABLE metricas_logisticas AS 

----------------------------------------------------------------------------------
-- Resumo das métricas:

-- dist_base_principal_km   : Distância (km) do município até a base principal, em betim
-- dist_base_oliveira_km    : Distância (km) do município até a base em Oliveira
-- dist_base_atendimento_km : Distância (km) do município até a base responsável pelo atendimento do município
-- dist_referencia_km       : Limite empírico de operação aceitável (distância base-município)
-- base_atendimento         : ID da base responsável (Betim ou Oliveira) pelo atendimento do município
----------------------------------------------------------------------------------

WITH 
    base AS (
        SELECT 
            id_municipio,

            -- Distância Haversine do município selecionado até Betim:
            (6371 * 2 * ASIN(
                SQRT(
                    POWER(SIN(RADIANS(latitude - (-19.9668)) / 2), 2)
                    +
                    COS(RADIANS(-19.9668))
                    * COS(RADIANS(latitude))
                    * POWER(SIN(RADIANS(longitude - (-44.2008)) / 2), 2)
                )
            )) AS dist_base_principal_km,

            -- Distância Haversine do município selecionado até Oliveira:
            (6371 * 2 * ASIN(
                SQRT(
                    POWER(SIN(RADIANS(latitude - (-20.6982)) / 2), 2)
                    +
                    COS(RADIANS(-20.6982))
                    * COS(RADIANS(latitude))
                    * POWER(SIN(RADIANS(longitude - (-44.8290)) / 2), 2)
                )
            )) AS dist_base_oliveira_km

        FROM coordenadas_municipios
    ),
    ---------------------------------------------------------------------
    dist_municipio_base AS (
        SELECT 
            *,

            LEAST(
                dist_base_principal_km,
                dist_base_oliveira_km
            ) AS dist_base_atendimento_km

        FROM base
    ),
    ---------------------------------------------------------------------
    municipios AS (
        SELECT
            d.id_municipio,
            d.dist_base_atendimento_km

        FROM dist_municipio_base d

        INNER JOIN municipios_atendidos a
            ON d.id_municipio = a.id_municipio
        
        WHERE a.atendido = TRUE
    ),
    ---------------------------------------------------------------------
    dist_referencia AS (
        SELECT
            -- Calcula a distância de referência município-base
            -- com base nos municípios atendidos (percentil 90%)
            quantile_cont(
                dist_base_atendimento_km,
                0.90
            ) AS dist_referencia_km

        FROM municipios
    )

SELECT 
    d.*,

    CASE
        WHEN d.dist_base_principal_km <= d.dist_base_oliveira_km
            THEN 3106705 -- ID de Betim
        ELSE 3145604     -- ID de Oliveira
    END AS base_atendimento,

    dr.dist_referencia_km

FROM dist_municipio_base d
CROSS JOIN dist_referencia dr
