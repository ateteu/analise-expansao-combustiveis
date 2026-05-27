-- Consolida métricas anuais e scores utilizados nas análises comparativas dos municípios.

CREATE OR REPLACE TABLE municipios_bi_anual AS

SELECT
    s.ano,
    s.id_municipio,

    s.score_logistico, -- usar a versão normalizada, depois de atualizar
    s.score_economico, -- usar a versão normalizada, depois de atualizar
    s.score_demanda,   -- usar a versão normalizada, depois de atualizar
    s.score_final_norm,

    v.vol_vendido_total_m3_norm, -- uso a versao normalizada ou a normal?
    v.vol_vendido_diesel_m3,     -- uso a versao normalizada ou a normal?
    v.vol_vendido_etanol_m3,     -- uso a versao normalizada ou a normal?
    v.vol_vendido_gasolina_m3,   -- uso a versao normalizada ou a normal?
    v.pct_diesel,
    v.pct_combustivel_leve,

    f.frota_pesada,
    f.frota_leve,
    f.combustivel_por_veiculo_norm,
    f.diesel_por_veiculo_pesado_norm,
    f.combustivel_leve_por_veiculo, -- fazer uma versão normalizada para usar aqui; atualizar o nome também

    e.pib_pc_relativo_norm,
    e.contribuicao_industria_norm,
    e.contribuicao_servicos_norm

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

ORDER BY ano, id_municipio
