CREATE OR REPLACE TABLE metricas_economicas AS

-- Resumo das métricas:

-- pib_per_capita_relativo : Relação entre o PIB per capita municipal e o PIB per capita médio estadual
-- contribuicao_agro       : Participação (%) da agropecuária no VAB total do município
-- contribuicao_industria  : Participação (%) da indústria no VAB total do município
-- contribuicao_servicos   : Participação (%) dos serviços no VAB total do município


WITH pib_estadual AS (
    SELECT
        ano,
        SUM(pib_total) / SUM(populacao) AS pib_per_capita_estadual

    FROM pib_ibge
    GROUP BY ano
)

SELECT
    p.id_municipio,
    p.ano,

    p.pib_per_capita / e.pib_per_capita_estadual
    AS pib_per_capita_relativo,

    p.vab_agro / p.vab_total
    AS contribuicao_agro,

    p.vab_industria / p.vab_total
    AS contribuicao_industria,

    p.vab_servicos / p.vab_total
    AS contribuicao_servicos

FROM pib_ibge p

LEFT JOIN pib_estadual e
    ON p.ano = e.ano
