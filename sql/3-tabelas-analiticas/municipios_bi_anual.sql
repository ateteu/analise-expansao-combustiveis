-- Consolida métricas anuais e scores utilizados nas análises comparativas dos municípios.

CREATE OR REPLACE TABLE municipios_bi_anual AS

SELECT
    s.ano,
    s.id_municipio,

    -- Scores
    s.score_logistico_norm, 
    s.score_economico_norm, 
    s.score_demanda_norm,   
    s.score_final_norm,

    -- Métricas de vendas
    v.vol_vendido_total_m3,
    v.vol_vendido_diesel_m3, 
    v.vol_vendido_etanol_m3, 
    v.vol_vendido_gasolina_m3, 
    v.pct_diesel,
    v.pct_combustivel_leve,

    -- Métricas de frota
    f.frota_pesada,
    f.frota_leve,
    f.combustivel_por_veiculo,
    f.diesel_por_veiculo_pesado,
    f.combustivel_leve_por_veiculo,

    -- Métricas e medidas econômicas
    e.pib_per_capita_relativo,
    e.contribuicao_agro,
    e.contribuicao_industria,
    e.contribuicao_servicos,
    p.vab_total,
    p.vab_agro,
    p.vab_industria,
    p.vab_servicos,
    p.atividade_1,
    p.atividade_2,
    p.atividade_3

FROM 
    scores s 

LEFT JOIN metricas_vendas v 
    ON s.id_municipio = v.id_municipio 
    AND s.ano = v.ano 

LEFT JOIN metricas_frota f 
    ON s.id_municipio = f.id_municipio 
    AND s.ano = f.ano 

LEFT JOIN metricas_economicas e 
    ON s.id_municipio = e.id_municipio 
    AND s.ano = e.ano 

LEFT JOIN pib_ibge p 
    ON s.id_municipio = p.id_municipio 
    AND s.ano = p.ano 

ORDER BY ano, id_municipio
