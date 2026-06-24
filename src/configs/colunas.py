# Este arquivo contém listas com nomes de colunas e linhas


ORDEM_LINHAS = [
    "ano",
    "id_municipio",
]

# =================================================
# FROTA - SENATRAN
# =================================================

PRIMEIRAS_COL_SENATRAN = ORDEM_LINHAS
COLUNAS_INT_SENATRAN = [
    "total",
    "automovel",
    "bonde",
    "caminhao",
    "caminhao_trator",
    "caminhonete",
    "camioneta",
    "chassi_plataf",
    "ciclomotor",
    "micro_onibus",
    "motocicleta",
    "motoneta",
    "onibus",
    "quadriciclo",
    "reboque",
    "semi_reboque",
    "side_car",
    "outros",
    "trator_estei",
    "trator_rodas",
    "triciclo",
    "utilitario",
]
COLUNAS_STR_SENATRAN = [
    "uf",
    "id_municipio",
    "municipio",
]

# =================================================
# VENDAS COMBUSTÍVEIS - ANP
# =================================================

COLUNAS_CRITICAS_VENDAS = [
    "ano",
    "id_municipio",
    "tipo_combustivel",
    "volume_vendido_m3",
]
COLUNAS_IDENTIFICADORAS = [
    "ano",
    "id_municipio",
    "tipo_combustivel",
]
COLUNAS_SAIDA_VENDAS = [
    "ano", 
    "id_municipio", 
    "id_combustivel", 
    "volume_vendas_m3",
]

# =================================================
# DADOS ECONÔMICOS - IBGE
# =================================================

ORDEM_COL_PIB = [
    "ano",
    "id_municipio",
    "pib",
    "pib_per_capita",
    "vab_total",
]
COLUNAS_NUM_PIB = [
    "vab_agropecuaria",
    "vab_industria",
    "vab_servicos",
    "vab_adm_publica",
    "vab_total",
    "pib",
    "pib_per_capita",
]
COLUNAS_STR_PIB = [
    "id_municipio",
    "atividade_1",
    "atividade_2",
    "atividade_3",
]

# =================================================
# COORD. MUNICÍPIOS - GITHUB/KELVINS
# =================================================

COLUNAS_CRITICAS_COORD_MUNICIPIOS = [
    "id_municipio",
    "latitude",
    "longitude",
]
