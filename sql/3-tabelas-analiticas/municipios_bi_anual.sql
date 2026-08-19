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
    f.combustivel_por_veiculo_leve,

    -- Métricas e medidas econômicas
    de.vab_total,
    de.vab_agropecuaria,
    de.vab_industria,
    de.vab_servicos,
    de.atividade_1,
    de.atividade_2,
    de.atividade_3,
    de.pib,
    de.pib_per_capita,
    me.pib_per_capita_relativo,
    me.populacao,
    me.contribuicao_agro,
    me.contribuicao_industria,
    me.contribuicao_servicos

FROM 
    scores s 

LEFT JOIN metricas_vendas v 
    ON s.id_municipio = v.id_municipio 
    AND s.ano = v.ano 

LEFT JOIN metricas_frota f 
    ON s.id_municipio = f.id_municipio 
    AND s.ano = f.ano 

LEFT JOIN metricas_economicas me 
    ON s.id_municipio = me.id_municipio 
    AND s.ano = me.ano 

LEFT JOIN dados_economicos de 
    ON s.id_municipio = de.id_municipio 
    AND s.ano = de.ano 
