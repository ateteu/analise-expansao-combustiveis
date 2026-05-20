CREATE OR REPLACE TABLE score_logistico AS

-- Resumo das métricas:

-- score_logistico : 
    -- Score baseado na distância até a base mais próxima;
    -- valores próximos de 1 indicam atendimento eficiente

SELECT
    id_municipio,

    (
        1.0 
        / 
        (1.0 + (dist_base_atendimento_km  / dist_referencia_km))
    ) AS score_logistico

FROM metricas_logisticas
