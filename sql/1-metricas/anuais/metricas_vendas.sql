CREATE OR REPLACE TABLE metricas_demanda AS

-- Resumo das métricas:

-- vol_vendido_total_m3  : Soma anual dos volumes de diesel, etanol e gasolina C
-- pct_diesel            : Participação do diesel no volume total vendido
-- pct_combustivel_leve  : Participação de etanol + gasolina no volume total

WITH vendas AS (
    SELECT 
        id_municipio,
        ano,

        SUM(
            CASE 
                WHEN tipo_combustivel = 'DIESEL' THEN volume_vendas_m3
                ELSE 0
            END
        ) AS vol_vendido_diesel_m3,

        SUM(
            CASE 
                WHEN tipo_combustivel = 'ETANOL' THEN volume_vendas_m3
                ELSE 0
            END
        ) AS vol_vendido_etanol_m3,

        SUM(
            CASE
                WHEN tipo_combustivel = 'GASOLINA' THEN volume_vendas_m3
                ELSE 0
            END
        ) AS vol_vendido_gasolina_m3

    FROM vendas_anp

    GROUP BY 
        id_municipio, 
        ano
)

SELECT 
    *,

    (vol_vendido_diesel_m3 + vol_vendido_etanol_m3 + vol_vendido_gasolina_m3)
    AS vol_vendido_total_m3

    (vol_vendido_diesel_m3 / vol_vendido_total_m3) 
    AS pct_diesel,

    ((vol_vendido_etanol_m3 + vol_vendido_gasolina_m3) / vol_vendido_total_m3) 
    AS pct_combustivel_leve,

FROM vendas
