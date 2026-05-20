CREATE OR REPLACE TABLE metricas_vendas AS

-- Resumo das métricas:

-- vol_vendido_total_m3      : Soma anual dos volumes vendidos de diesel, etanol e gasolina C
-- vol_vendido_total_m3_norm : Volume total de combustível vendido pelo município normalizado entre 0 e 1
-- pct_diesel                : Participação do diesel no volume total vendido
-- pct_combustivel_leve      : Participação de etanol + gasolina no volume total

WITH 
    vendas AS (
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
    ),

    metricas_base_vendas AS (
        SELECT 
            *,

            (vol_vendido_diesel_m3 + vol_vendido_etanol_m3 + vol_vendido_gasolina_m3)
            AS vol_vendido_total_m3,

            (
                vol_vendido_diesel_m3 
                / 
                NULLIF(
                    vol_vendido_diesel_m3 + vol_vendido_etanol_m3 + vol_vendido_gasolina_m3,
                    0
                )
            ) 
            AS pct_diesel,

            (
                (vol_vendido_etanol_m3 + vol_vendido_gasolina_m3) 
                / 
                NULLIF(
                    vol_vendido_diesel_m3 + vol_vendido_etanol_m3 + vol_vendido_gasolina_m3, 
                    0
                )
            ) 
            AS pct_combustivel_leve

        FROM vendas
    )

SELECT
    *,

    -- Normaliza o volume total (m3) de combustível vendido
    (vol_vendido_total_m3 - MIN(vol_vendido_total_m3) OVER())
    /
    NULLIF (
        MAX(vol_vendido_total_m3) OVER() - MIN(vol_vendido_total_m3) OVER(),
        0
    )
    AS vol_vendido_total_m3_norm

FROM metricas_base_vendas
