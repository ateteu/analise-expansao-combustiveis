CREATE OR REPLACE TABLE metricas_demanda AS

-- Resumo das métricas:

-- vol_vendido_total_m3            : Soma anual dos volumes de diesel, etanol e gasolina C
-- pct_diesel                      : Participação do diesel no volume total vendido
-- pct_combustivel_leve            : Participação de etanol + gasolina no volume total
-- combustivel_por_veiculo_m3      : Volume total vendido dividido pela frota total
-- diesel_por_veiculo_pesado_m3    : Volume de diesel dividido pela frota pesada
-- combustivel_leve_por_veiculo_m3 : Volume de combustíveis leves dividido pela frota leve
-- crescimento_linear_volume       : Inclinação da regressão linear do volume vendido (2015–2024)
-- cagr_vol_vendido_m3_3a          : CAGR do volume vendido entre 2021 e 2024
-- cagr_vol_vendido_m3_9a          : CAGR do volume vendido entre 2015 e 2024
-- crescimento_linear_frota        : Inclinação da regressão linear da frota total (2015–2024)
-- cagr_frota_3a                   : CAGR da frota total entre 2021 e 2024
-- cagr_frota_9a                   : CAGR da frota total entre 2015 e 2024

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

    vendas_total AS (
        SELECT
            id_municipio,
            ano,

            vol_vendido_diesel_m3,
            vol_vendido_etanol_m3,
            vol_vendido_gasolina_m3,

            (vol_vendido_diesel_m3 + vol_vendido_etanol_m3 + vol_vendido_gasolina_m3)
            AS vol_vendido_total_m3

        FROM vendas
    ),

    serie AS (
        SELECT
            id_municipio,

            MAX(
                CASE
                    WHEN ano = 2015 THEN vol_vendido_total_m3
                END
            ) AS vol_vendido_2015_m3,

            MAX(
                CASE 
                    WHEN ano = 2021 THEN vol_vendido_total_m3 
                END
            ) AS vol_vendido_2021_m3,

            MAX(
                CASE
                    WHEN ano = 2024 THEN vol_vendido_total_m3
                END
            ) AS vol_vendido_2024_m3,

            REGR_SLOPE(vol_vendido_total_m3, ano) AS crescimento_linear_volume
        
        FROM vendas_total
        GROUP BY id_municipio
    )

SELECT 
    *,

    (v.vol_vendido_diesel_m3 / s.vol_vendido_total_m3) 
    AS pct_diesel,

    ((v.vol_vendido_etanol_m3 + v.vol_vendido_gasolina_m3) / s.vol_vendido_total_m3) 
    AS pct_combustivel_leve,

    (POWER((s.vol_vendido_2024_m3 / s.vol_vendido_2015_m3), (1.0/9)) - 1)
    AS cagr_vol_vendido_m3_9a,

    (POWER((s.vol_vendido_2024_m3 / s.vol_vendido_2021_m3), (1.0/3)) - 1)
    AS cagr_vol_vendido_m3_3a,

FROM vendas v
LEFT JOIN serie s
    ON v.id_municipio = s.id_municipio
