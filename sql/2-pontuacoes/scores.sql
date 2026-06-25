CREATE OR REPLACE TABLE scores AS

----------------------------------------------------------------------------------
-- Resumo das métricas:

-- score_logistico_norm : Score baseado na distância até a base mais próxima
-- score_economico_norm : Score de qualificação econômica do município
-- score_demanda_norm   : Score de potencial de consumo do município
-- score_final_norm     : Score consolidado de atratividade do município
----------------------------------------------------------------------------------

WITH 
    scores_individuais AS (
        SELECT
            l.id_municipio,
            e.ano,
            ----------------------------------------------------------------
            -- SCORE LOGÍSTICO [0,1]
            (
                1.0 
                / 
                (1.0 + (l.dist_base_atendimento_km  / l.dist_referencia_km))
            ) AS score_logistico_norm,
            ----------------------------------------------------------------
            -- SCORE ECONÔMICO [0,1]
            (
                (
                    COALESCE(0.40 * e.pib_pc_relativo_norm, 0)
                    +
                    COALESCE(0.35 * e.contribuicao_industria_norm, 0)
                    +
                    COALESCE(0.25 * e.contribuicao_servicos_norm, 0)
                )
                /
                NULLIF(
                    (CASE WHEN e.pib_pc_relativo_norm IS NOT NULL THEN 0.40 ELSE 0 END)
                    +
                    (CASE WHEN e.contribuicao_industria_norm IS NOT NULL THEN 0.35 ELSE 0 END)
                    +
                    (CASE WHEN e.contribuicao_servicos_norm IS NOT NULL THEN 0.25 ELSE 0 END),
                    0
                )
            ) AS score_economico_norm,
            ----------------------------------------------------------------
            -- SCORE DEMANDA [0,1]
            (
                0.5 * dv.vol_vendido_total_m3_norm
                +
                0.3 * df.combustivel_por_veiculo_norm
                +
                0.2 * df.diesel_por_veiculo_pesado_norm
            )
            AS score_demanda_norm
        
        -- Econômicas
        FROM metricas_economicas e

        -- Demanda
        JOIN metricas_frota df
            ON e.id_municipio = df.id_municipio
            AND e.ano = df.ano

        -- Demanda
        JOIN metricas_vendas dv
            ON e.id_municipio = dv.id_municipio
            AND e.ano = dv.ano

        -- Logísticas
        JOIN metricas_logisticas l
            ON e.id_municipio = l.id_municipio
    ),

    score_base AS (
        SELECT
            *,

            -- Calcula o score final com base nos scores anteriores e pesos
            -- Pesos inicialmente em 1; ajustar depois
            (
                1 * score_logistico_norm
                +
                1 * score_economico_norm
                +
                1 * score_demanda_norm
            ) AS score_final

        FROM scores_individuais
    )

SELECT
    *,
    (
        -- Normaliza o score final, para ficar entre 0 e 1
        (score_final - MIN(score_final) OVER())
        /
        NULLIF(
            (MAX(score_final) OVER() - MIN(score_final) OVER()),
            0
        )
        
    ) AS score_final_norm

FROM score_base
