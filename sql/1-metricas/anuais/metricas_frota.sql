CREATE OR REPLACE TABLE metricas_frota AS

----------------------------------------------------------------------------------
-- Resumo das métricas:

-- combustivel_por_veiculo        : Volume total vendido dividido pela frota total
-- combustivel_por_veiculo_norm   : Valor de combustível por veículo (total) normalizado [0,1]
-- diesel_por_veiculo_pesado      : Volume de diesel dividido pela frota pesada
-- diesel_por_veiculo_pesado_norm : Valor de diesel por veículo pesado normalizado entre [0,1]
-- combustivel_por_veiculo_leve   : Volume de combustíveis leves dividido pela frota leve
----------------------------------------------------------------------------------

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
    ),

    metricas_base_frota AS (
        SELECT 
            f.*,

            (v.vol_vendido_total_m3 / NULLIF(f.frota_total, 0))
            AS combustivel_por_veiculo,

            (v.vol_vendido_diesel_m3 / NULLIF(f.frota_pesada, 0)) 
            AS diesel_por_veiculo_pesado,

            ((v.vol_vendido_etanol_m3 + v.vol_vendido_gasolina_m3) / NULLIF(f.frota_leve, 0)) 
            AS combustivel_por_veiculo_leve

        FROM frota f 

        LEFT JOIN vendas v 
            ON f.id_municipio = v.id_municipio 
            AND f.ano = v.ano
    )

SELECT
    *,

    -- Normaliza o valor de combusível por veículo (total)
    (combustivel_por_veiculo - MIN(combustivel_por_veiculo) OVER())
    /
    NULLIF (
        MAX(combustivel_por_veiculo) OVER() - MIN(combustivel_por_veiculo) OVER(),
        0
    )
    AS combustivel_por_veiculo_norm,


    -- Normaliza o valor de diesel por veículo pesado
    (diesel_por_veiculo_pesado - MIN(diesel_por_veiculo_pesado) OVER())
    /
    NULLIF (
        MAX(diesel_por_veiculo_pesado) OVER() - MIN(diesel_por_veiculo_pesado) OVER(),
        0
    )
    AS diesel_por_veiculo_pesado_norm

FROM metricas_base_frota
