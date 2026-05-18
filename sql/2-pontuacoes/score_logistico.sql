CREATE OR REPLACE TABLE score_logistico AS

WITH referencia AS (

    SELECT
        l.id_municipio,
        l.dist_base_atendimento_km

    FROM metricas_logisticas l

    INNER JOIN municipios_atendidos a
        ON l.id_municipio = a.id_municipio
)

SELECT
    quantile_cont(
        dist_base_atendimento_km,
        0.90
    ) AS distancia_referencia_km

FROM referencia