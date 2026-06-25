-- Este arquivo contém algumas perguntas investigativas que ajudam a extrair insights dos dados


-- PERGUNTA_1
-- Municípios economicamente mais fortes apresentam maior consumo de combustíveis?

SELECT
    d.nome_municipio,
    b.id_municipio,
    b.pib_per_capita,
    b.vol_vendido_total_m3

FROM municipios_bi_anual b

JOIN dimensao_municipio d
    ON b.id_municipio = d.id_municipio

WHERE b.ano = 2023;


-- PERGUNTA_2
-- Municípios com maior frota pesada consomem proporcionalmente mais diesel?

SELECT
    d.nome_municipio,
    b.id_municipio,
    b.frota_pesada,
    b.pct_diesel

FROM municipios_bi_anual b

JOIN dimensao_municipio d
    ON b.id_municipio = d.id_municipio

WHERE b.ano = 2023;


-- PERGUNTA_3
-- Os municípios mais distantes das bases logísticas apresentam menor atratividade?


SELECT
    d.nome_municipio,
    c.id_municipio,
    c.dist_base_atendimento_km,
    c.score_final_medio

FROM municipios_bi_crescimento c

JOIN dimensao_municipio d
    ON c.id_municipio = d.id_municipio;


-- PERGUNTA_4
-- Quais municípios tiveram maior crescimento de vendas nos últimos anos?

SELECT
    d.nome_municipio,
    c.cagr_vol_vendido_3a,
    c.id_municipio

FROM municipios_bi_crescimento c

JOIN dimensao_municipio d
    ON c.id_municipio = d.id_municipio

ORDER BY c.cagr_vol_vendido_3a DESC

LIMIT 20;


-- PERGUNTA_5
-- Quais municípios possuem alto score mas ainda não são atendidos?

SELECT
    d.nome_municipio,
    d.status_atendimento,
    b.score_final_norm
FROM municipios_bi_anual b

JOIN dimensao_municipio d
    ON b.id_municipio = d.id_municipio

WHERE b.ano = 2023
    AND d.status_atendimento = 'nao_atendido'

ORDER BY b.score_final_norm DESC
LIMIT 20;
