CREATE OR REPLACE TABLE metricas_economicas AS

----------------------------------------------------------------------------------
-- Resumo das métricas:

-- pib_per_capita_relativo     : Relação entre o PIB p.c municipal e o PIB p.c médio estadual
-- pib_pc_relativo_norm        : PIB per capita relativo normalizado [0,1]
-- contribuicao_agro           : Participação (%) da agropecuária no VAB total do município
-- contribuicao_industria      : Participação (%) da indústria no VAB total do município
-- contribuicao_industria_norm : Participação (%) da indústria no VAB normalizada entre [0,1]
-- contribuicao_servicos       : Participação (%) dos serviços no VAB total do município
-- contribuicao_servicos_norm  : Participação (%) dos serviços no VAB normalizada entre [0,1]
----------------------------------------------------------------------------------

WITH 
    pib_estadual AS (
        SELECT
            ano,

            SUM(pib / NULLIF(pib_per_capita, 0)) 
            AS populacao,

            (
                SUM(pib) 
                / 
                NULLIF(
                    SUM(pib / NULLIF(pib_per_capita, 0)),
                    0
                )
            ) AS pib_per_capita_estadual

        FROM pib_ibge
        GROUP BY ano
    ),

    metricas_base AS (
        SELECT
            p.id_municipio,
            p.ano,
            pe.populacao,

            CASE
                WHEN p.vab_total IS NULL THEN 0
                ELSE 1
            END AS possui_vab,

            (p.pib_per_capita / pe.pib_per_capita_estadual)
            AS pib_per_capita_relativo,

            (p.vab_agropecuaria / p.vab_total)
            AS contribuicao_agro,

            (p.vab_industria / p.vab_total)
            AS contribuicao_industria,

            (p.vab_servicos / p.vab_total)
            AS contribuicao_servicos

        FROM pib_ibge p

        LEFT JOIN pib_estadual pe 
            ON p.ano = pe.ano
    )

SELECT
    *,

    -- Normalização do PIB per capita
    (pib_per_capita_relativo - MIN(pib_per_capita_relativo) OVER())
    /
    NULLIF (
        MAX(pib_per_capita_relativo) OVER() - MIN(pib_per_capita_relativo) OVER(),
        0
    )
    AS pib_pc_relativo_norm,
    ---------------------------------------------------------------------------
    -- Normalização da contribuição da indústria
    (contribuicao_industria - MIN(contribuicao_industria) OVER())
    /
    NULLIF (
        MAX(contribuicao_industria) OVER() - MIN(contribuicao_industria) OVER(),
        0
    )
    AS contribuicao_industria_norm,
    ---------------------------------------------------------------------------
    -- Normalização da contribuição de serviços
    (contribuicao_servicos - MIN(contribuicao_servicos) OVER())
    /
    NULLIF (
        MAX(contribuicao_servicos) OVER() - MIN(contribuicao_servicos) OVER(),
        0
    )
    AS contribuicao_servicos_norm

FROM metricas_base
