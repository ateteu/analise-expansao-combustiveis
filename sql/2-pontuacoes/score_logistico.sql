CREATE OR REPLACE TABLE score_logistico AS

-- Resumo das métricas:

-- score_logistico : 
    -- Score baseado na distância até a base mais próxima;
    -- valores próximos de 1 indicam atendimento eficiente

WITH 
    referencia AS (
        SELECT
            l.id_municipio,
            l.dist_base_atendimento_km

        FROM metricas_logisticas l

        INNER JOIN municipios_atendidos a
            ON l.id_municipio = a.id_municipio
        
        WHERE a.status_atendimento = 'atendido'
    ),

    distancia_referencia AS (
        -- Calcula a distância de referência município-base
        -- com base nos municípios atendidos (percentil 90%)
        SELECT
            quantile_cont(
                dist_base_atendimento_km,
                0.90
            ) AS distancia_referencia_km

        FROM referencia
    )

SELECT
    l.*,
    d.distancia_referencia_km,

    (
        1.0 
        / 
        (1.0 + (l.dist_base_atendimento_km  / d.distancia_referencia_km))
    ) AS score_logistico

FROM metricas_logisticas l
CROSS JOIN distancia_referencia d
