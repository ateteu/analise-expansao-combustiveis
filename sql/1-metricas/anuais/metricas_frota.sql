CREATE OR REPLACE TABLE metricas_frota AS

-- Resumo das métricas:

-- combustivel_por_veiculo      : Volume total vendido dividido pela frota total
-- diesel_por_veiculo_pesado    : Volume de diesel dividido pela frota pesada
-- combustivel_leve_por_veiculo : Volume de combustíveis leves dividido pela frota leve

WITH 
    frota AS (
        SELECT
            id_municipio,
            ano,
            total AS frota_total,

            (
                caminhao
                + caminhao_trator
                + micro_onibus
                + onibus
                + trator_rodas
                + trator_estei
            ) 
            AS frota_pesada,

            (
                automovel
                + motocicleta
                + motoneta
                + camioneta
                + caminhonete
                + utilitario
                + ciclomotor
                + triciclo
                + quadriciclo
            ) 
            AS frota_leve

        FROM frota_senatran
    ),

    vendas AS (
        SELECT
            id_municipio,
            ano,
            vol_vendido_total_m3,
            vol_vendido_diesel_m3,
            vol_vendido_etanol_m3,
            vol_vendido_gasolina_m3

        FROM metricas_vendas
    )

SELECT 
    *,

    (v.vol_vendido_total_m3 / NULLIF(f.frota_total, 0))
    AS combustivel_por_veiculo,

    (v.vol_vendido_diesel_m3 / NULLIF(f.frota_pesada, 0)) 
    AS diesel_por_veiculo_pesado,

    ((v.vol_vendido_etanol_m3 + v.vol_vendido_gasolina_m3) / NULLIF(f.frota_leve, 0)) 
    AS combustivel_leve_por_veiculo

FROM frota f 

LEFT JOIN vendas v 
    ON f.id_municipio = v.id_municipio 
    AND f.ano = v.ano
