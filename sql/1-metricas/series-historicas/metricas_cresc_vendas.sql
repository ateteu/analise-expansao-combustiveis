CREATE OR REPLACE TABLE metricas_crescimento_vendas AS

-- Resumo das métricas:

-- cresc_linear_vol_vendido : Inclinação da regressão linear do volume vendido (2015–2024)
-- cagr_vol_vendido_m3_3a   : CAGR do volume vendido entre 2021 e 2024
-- cagr_vol_vendido_m3_9a   : CAGR do volume vendido entre 2015 e 2024

WITH base AS (
    SELECT *
    FROM metricas_vendas
    WHERE ano <= 2024
)

SELECT
    id_municipio,

    REGR_SLOPE(vol_vendido_total_m3, ano) AS cresc_linear_vol_vendido

    POWER(
        (
            -- Volume total vendido pelo município em 2024
            MAX(CASE WHEN ano = 2024 THEN volume_total_m3 END)
            /
            -- Volume total vendido pelo município em 2021
            MAX(CASE WHEN ano = 2021 THEN volume_total_m3 END)
        ),
        (1.0 / 3)
    ) - 1 AS cagr_vol_vendido_3a,

    POWER(
        (
            -- Volume total vendido pelo município em 2024
            MAX(CASE WHEN ano = 2024 THEN volume_total_m3 END)
            /
            -- Volume total vendido pelo município em 2015
            MAX(CASE WHEN ano = 2015 THEN volume_total_m3 END)
        ),
        (1.0 / 9)
    ) - 1 AS cagr_vol_vendido_9a

FROM base
GROUP BY id_municipio
