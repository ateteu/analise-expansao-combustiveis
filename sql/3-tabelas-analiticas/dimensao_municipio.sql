-- Essa tabela unifica os dados estruturais e geográficos de dimensão da entidade município

CREATE OR REPLACE TABLE dimensao_municipio AS

SELECT DISTINCT
    ibge.id_municipio,
    ibge.nome_municipio,

    ibge.id_uf,
    ibge.nome_uf,

    ibge.id_regiao_imediata,
    ibge.nome_regiao_imediata,
    
    ibge.id_regiao_intermediaria,
    ibge.nome_regiao_intermediaria,

    coord.latitude,
    coord.longitude

FROM
    pib_ibge ibge

LEFT JOIN coordenadas_municipios coord
    ON ibge.cod_municipio = coord.cod_municipio;
