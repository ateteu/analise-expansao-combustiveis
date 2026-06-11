
CREATE TABLE refinaria (
    nome_refinaria VARCHAR(100),
    id_refinaria   VARCHAR(2) NOT NULL,
    latitude       DECIMAL(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude      DECIMAL(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),

    PRIMARY KEY (id_refinaria)
)

CREATE TABLE base_logistica (
    nome_base    VARCHAR(100),
    id_base      VARCHAR(2) NOT NULL,
    id_refinaria VARCHAR(2),
    latitude     DECIMAL(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude    DECIMAL(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),

    PRIMARY KEY (id_base),
    FOREIGN KEY (id_refinaria) REFERENCES refinaria(id_refinaria)
)

CREATE TABLE uf (
    nome_uf VARCHAR(50),
    id_uf   VARCHAR(2) NOT NULL,

    PRIMARY KEY (id_uf)
)

CREATE TABLE regiao_intermediaria (
    nome_regiao_intermediaria VARCHAR(100),
    id_regiao_intermediaria   VARCHAR(4) NOT NULL,
    id_uf                     VARCHAR(2),

    PRIMARY KEY (id_regiao_intermediaria),
    FOREIGN KEY (id_uf) REFERENCES uf(id_uf)
)

CREATE TABLE regiao_imediata (
    nome_regiao_imediata    VARCHAR(100),
    id_regiao_imediata      VARCHAR(6) NOT NULL,
    id_regiao_intermediaria VARCHAR(4),

    PRIMARY KEY (id_regiao_imediata),
    FOREIGN KEY (id_regiao_intermediaria) REFERENCES regiao_intermediaria(id_regiao_intermediaria)
)

CREATE TABLE municipio (
    nome_municipio      VARCHAR(100),
    id_municipio        VARCHAR(7) NOT NULL,
    id_regiao_imediata  VARCHAR(6),
    flag_atendimento    INTEGER CHECK (flag_atendimento IN (0, 1, 2)),
    id_base_atendimento VARCHAR(2),
    latitude            DECIMAL(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude           DECIMAL(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),

    PRIMARY KEY (id_municipio),
    FOREIGN KEY (id_regiao_imediata)  REFERENCES regiao_imediata(id_regiao_imediata),
    FOREIGN KEY (id_base_atendimento) REFERENCES base_logistica(id_base)
)

CREATE TABLE dados_economicos (
    ano            INTEGER NOT NULL CHECK (ano BETWEEN 2000 AND 2026),
    id_municipio   VARCHAR(7) NOT NULL,
    pib            DECIMAL(18,3) CHECK (pib >= 0),
    pib_per_capita DECIMAL(18,3) CHECK (pib_per_capita >= 0),
    vab_total      DECIMAL(18,3) CHECK (vab_total >= 0),
    vab_agro       DECIMAL(18,3) CHECK (vab_agro >= 0),
    vab_industria  DECIMAL(18,3) CHECK (vab_industria >= 0),
    vab_servicos   DECIMAL(18,3) CHECK (vab_servicos >= 0),
    atividade_1    VARCHAR(500),
    atividade_2    VARCHAR(500),
    atividade_3    VARCHAR(500),

    PRIMARY KEY (ano, id_municipio),
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
)

CREATE TABLE frota_veiculos (
    ano             INTEGER NOT NULL CHECK (ano BETWEEN 2000 AND 2026),
    id_municipio    VARCHAR(7) NOT NULL,
    automovel       INTEGER NOT NULL CHECK (automovel >= 0),
    bonde           INTEGER NOT NULL CHECK (bonde >= 0),
    caminhao        INTEGER NOT NULL CHECK (caminhao >= 0),
    caminhao_trator INTEGER NOT NULL CHECK (caminhao_trator >= 0),
    caminhonete     INTEGER NOT NULL CHECK (caminhonete >= 0),
    camioneta       INTEGER NOT NULL CHECK (camioneta >= 0),
    chassi_plataf   INTEGER NOT NULL CHECK (chassi_plataf >= 0),
    ciclomotor      INTEGER NOT NULL CHECK (ciclomotor >= 0),
    micro_onibus    INTEGER NOT NULL CHECK (micro_onibus >= 0),
    motocicleta     INTEGER NOT NULL CHECK (motocicleta >= 0),
    motoneta        INTEGER NOT NULL CHECK (motoneta >= 0),
    onibus          INTEGER NOT NULL CHECK (onibus >= 0),
    quadriciclo     INTEGER NOT NULL CHECK (quadriciclo >= 0),
    reboque         INTEGER NOT NULL CHECK (reboque >= 0),
    semirreboque    INTEGER NOT NULL CHECK (semirreboque >= 0),
    sidecar         INTEGER NOT NULL CHECK (sidecar >= 0),
    outros          INTEGER NOT NULL CHECK (outros>= 0),
    trator_esteiras INTEGER NOT NULL CHECK (trator_esteiras >= 0),
    trator_rodas    INTEGER NOT NULL CHECK (trator_rodas >= 0),
    triciclo        INTEGER NOT NULL CHECK (triciclo >= 0),
    utilitario      INTEGER NOT NULL CHECK (utilitario >= 0),
    total           INTEGER NOT NULL CHECK (
        total = 
          automovel
        + bonde 
        + caminhao 
        + caminhao_trator 
        + caminhonete
        + camioneta
        + chassi_plataf
        + ciclomotor
        + micro_onibus
        + motocicleta
        + motoneta
        + onibus
        + quadriciclo
        + reboque
        + semirreboque
        + sidecar
        + outros
        + trator_esteiras
        + trator_rodas
        + triciclo
        + utilitario
    ),

    PRIMARY KEY (ano, id_municipio),
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
)

CREATE TABLE combustivel (
    nome_combustivel VARCHAR(100) NOT NULL UNIQUE,
    id_combustivel   VARCHAR(2) NOT NULL,
    pct_biodiesel    DECIMAL(5,3) CHECK (pct_biodiesel BETWEEN 0 AND 100),

    PRIMARY KEY (id_combustivel)
)

CREATE TABLE vendas_combustivel (
    ano            INTEGER NOT NULL CHECK (ano BETWEEN 2000 AND 2026),
    id_municipio   VARCHAR(7) NOT NULL,
    id_combustivel VARCHAR(2) NOT NULL,
    vol_vendido_m3 DECIMAL(18,3) CHECK (vol_vendido_m3 >= 0),

    PRIMARY KEY (ano, id_municipio, id_combustivel),
    FOREIGN KEY (id_municipio)   REFERENCES municipio(id_municipio),
    FOREIGN KEY (id_combustivel) REFERENCES combustivel(id_combustivel)
)
