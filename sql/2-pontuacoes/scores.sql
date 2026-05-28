CREATE OR REPLACE TABLE scores AS

-- Resumo das métricas:

-- score_logistico: 
    -- Score baseado na distância até a base mais próxima;
    -- valores próximos de 1 indicam atendimento eficiente

-- score_economico:
    -- Score de qualificação econômica do município;
    -- combina renda relativa e perfil produtivo (indústria e serviços) em escala normalizada

-- score_demanda:
    -- Score de potencial de consumo do município;
    -- combina tamanho do mercado e intensidade de consumo de combustíveis

-- score_final:
    -- Score consolidado de atratividade do município;
    -- combina demanda, perfil econômico e viabilidade logística

WITH 
    scores_individuais AS (
        SELECT
            l.id_municipio,
            e.ano,
            ----------------------------------------------------------------
            -- SCORE LOGÍSTICO
            -- Valor já naturalmente entre 0 e 1
            (
                1.0 
                / 
                (1.0 + (l.dist_base_atendimento_km  / l.dist_referencia_km))
            ) AS score_logistico_norm,
            ----------------------------------------------------------------
            -- SCORE ECONÔMICO
            -- Valor já naturalmente entre 0 e 1
            (
                0.4 * e.pib_pc_relativo_norm
                +
                0.35 * e.contribuicao_industria_norm
                +
                0.25 * e.contribuicao_servicos_norm
            ) AS score_economico_norm,
            ----------------------------------------------------------------
            -- SCORE DEMANDA
            - Valor já naturalmente entre 0 e 1
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
