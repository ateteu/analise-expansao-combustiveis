-- Essa tabela unifica os dados estruturais e geográficos de dimensão da entidade município

CREATE OR REPLACE TABLE dimensao_municipio AS

SELECT DISTINCT
    m.*,

    c.latitude,
    c.longitude,

    -- Divide os municípios em 3 categorias: 
    -- atendidos, não atendidos e fora do escopo de análise (fora do Sudeste)
    CASE 
        WHEN a.id_municipio IS NOT NULL
            THEN 'atendido'

        WHEN m.id_uf IN ('31', '32', '33', '35')
            THEN 'nao_atendido'

        ELSE 'fora_do_escopo'
    
    END AS status_atendimento

FROM municipios m

LEFT JOIN coordenadas_municipios c
    ON m.id_municipio = c.id_municipio

LEFT JOIN municipios_atendidos a
    ON m.id_municipio = a.id_municipio;
