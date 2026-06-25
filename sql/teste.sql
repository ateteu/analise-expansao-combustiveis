CREATE OR REPLACE TABLE teste AS

SELECT
    COUNT(*) total,
    COUNT(vol_vendido_total_m3_norm) vendas,
    COUNT(combustivel_por_veiculo_norm) combustivel,
    COUNT(diesel_por_veiculo_pesado_norm) diesel
FROM (
    SELECT
        dv.vol_vendido_total_m3_norm,
        df.combustivel_por_veiculo_norm,
        df.diesel_por_veiculo_pesado_norm
    FROM metricas_vendas dv
    JOIN metricas_frota df
        ON dv.id_municipio = df.id_municipio
        AND dv.ano = df.ano
);