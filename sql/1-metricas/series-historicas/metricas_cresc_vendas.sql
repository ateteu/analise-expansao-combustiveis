CREATE OR REPLACE TABLE metricas_crescimento_vendas AS

----------------------------------------------------------------------------------
-- Resumo das métricas:

-- cresc_linear_vol_vendido : Crescimento linear do volume vendido (2015-2024)
-- cagr_vol_vendido_m3_3a   : CAGR do volume vendido entre 2021 e 2024
-- cagr_vol_vendido_m3_9a   : CAGR do volume vendido entre 2015 e 2024
----------------------------------------------------------------------------------

-- CAGR (Compound Annual Growth Rate): 

-- Representa a taxa média anual de crescimento necessária para que uma variável 
-- evolua do valor inicial até o valor final do período, considerando crescimento 
-- acumulado ano após ano (efeito composto).


-- Crescimento linear: 

-- Representa a variação média anual de uma variável ao longo do tempo, 
-- estimada por regressão linear.
----------------------------------------------------------------------------------

WITH base AS (
    SELECT *
    FROM metricas_vendas
    WHERE ano <= 2024
)

SELECT
    id_municipio,

    REGR_SLOPE(vol_vendido_total_m3, ano) AS cresc_linear_vol_vendido,

    ------------------------------------------------------------------------------
    -- Calcula o CAGR do volume total vendido de combustível num período de 3 anos
    POWER(
        (
            -- Volume total vendido pelo município em 2024
            MAX(CASE WHEN ano = 2024 THEN vol_vendido_total_m3 END)
            /
            -- Volume total vendido pelo município em 2021
            MAX(CASE WHEN ano = 2021 THEN vol_vendido_total_m3 END)
        ),
        (1.0 / 3)
    ) - 1 
    AS cagr_vol_vendido_3a,

    ------------------------------------------------------------------------------
    -- Calcula o CAGR do volume total vendido de combustível num período de 9 anos
    POWER(
        (
            -- Volume total vendido pelo município em 2024
            MAX(CASE WHEN ano = 2024 THEN vol_vendido_total_m3 END)
            /
            -- Volume total vendido pelo município em 2015
            MAX(CASE WHEN ano = 2015 THEN vol_vendido_total_m3 END)
        ),
        (1.0 / 9)
    ) - 1 
    AS cagr_vol_vendido_9a

FROM base
GROUP BY id_municipio
