CREATE OR REPLACE TABLE metricas_crescimento_frota AS

-- Resumo das métricas:

-- cresc_linear_frota : Inclinação da regressão linear da frota total (2015 - 2024)
-- cagr_frota_3a      : CAGR da frota total entre 2021 e 2024
-- cagr_frota_9a      : CAGR da frota total entre 2015 e 2024

WITH base AS (
    SELECT *
    FROM metricas_frota
    WHERE ano <= 2024
)

SELECT
    id_municipio,
    REGR_SLOPE(frota_total, ano) AS cresc_linear_frota,

    POWER(
        (
            -- Frota total do município em 2024
            MAX(CASE WHEN ano = 2024 THEN frota_total END)
            /
            -- Frota total do município em 2021
            MAX(CASE WHEN ano = 2021 THEN frota_total END)
        ),
        (1.0 / 3)
    ) - 1 AS cagr_frota_3a,

    POWER(
        (
            -- Frota total do município em 2024
            MAX(CASE WHEN ano = 2024 THEN frota_total END)
            /
            -- Frota total do município em 2015
            MAX(CASE WHEN ano = 2015 THEN frota_total END)
        ),
        (1.0 / 9)
    ) - 1 AS cagr_frota_9a

FROM base
GROUP BY id_municipio
