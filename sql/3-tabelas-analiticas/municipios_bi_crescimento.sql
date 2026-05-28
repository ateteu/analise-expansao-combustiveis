-- Consolida indicadores históricos de crescimento e informações logísticas dos municípios.

CREATE OR REPLACE TABLE municipios_bi_crescimento AS

WITH score_medio AS (
    SELECT 
        id_municipio,
        AVG(score_final_norm) AS score_final_medio
    
    FROM scores
    GROUP BY id_municipio
)

SELECT
    v.id_municipio,

    v.cresc_linear_vol_vendido,
    v.cagr_vol_vendido_3a,
    v.cagr_vol_vendido_9a,

    f.cresc_linear_frota, 
    f.cagr_frota_3a, 
    f.cagr_frota_9a,

    l.base_atendimento,
    l.dist_base_atendimento_km,
    l.dist_referencia_km,

    s.score_final_medio

FROM 
    metricas_crescimento_vendas v

LEFT JOIN metricas_crescimento_frota f
    ON v.id_municipio = f.id_municipio

LEFT JOIN metricas_logisticas l 
    ON v.id_municipio = l.id_municipio 

LEFT JOIN score_medio s
    ON v.id_municipio = s.id_municipio
