# Este arquivo contém listas com nomes de colunas e linhas


ORDEM_LINHAS = [
    "ano",
    "id_municipio",
]

# =================================================
# VENDAS COMBUSTÍVEIS - ANP
# =================================================

COLUNAS_CRITICAS_VENDAS = [
    "ano",
    "id_municipio",
    "tipo_combustivel",
    "vol_vendido_m3",
]
COLUNAS_IDENTIFICADORAS = [
    "ano",
    "id_municipio",
    "tipo_combustivel",
]
COLUNAS_IDENTIFICADORAS_FINAIS = [
    "ano",
    "id_municipio",
    "id_combustivel",
]
COLUNAS_SAIDA_VENDAS = [
    "ano", 
    "id_municipio", 
    "id_combustivel", 
    "vol_vendido_m3",
]

# =================================================
# DADOS ECONÔMICOS - IBGE
# =================================================

ORDEM_COL_DADOS_ECONOMICOS = [
    "ano",
    "id_municipio",
    "pib",
    "pib_per_capita",
    "vab_total",
]
COLUNAS_NUM_DADOS_ECONOMICOS = [
    "vab_agropecuaria",
    "vab_industria",
    "vab_servicos",
    "vab_adm_publica",
    "vab_total",
    "pib",
    "pib_per_capita",
]
COLUNAS_VAB_COMPONENTES = [
    "vab_agropecuaria", 
    "vab_industria", 
    "vab_servicos", 
    "vab_adm_publica",
]
COLUNAS_CRITICAS_DADOS_ECONOMICOS = [
    "ano", 
    "id_municipio", 
    "vab_total", 
    "pib", 
    "pib_per_capita",
]

# =================================================
# MUNICÍPIOS - IBGE
# =================================================



# =================================================
# COORD. MUNICÍPIOS - GITHUB/KELVINS
# =================================================

COLUNAS_CRITICAS_COORD_MUNICIPIOS = [
    "id_municipio",
    "latitude",
    "longitude",
]

# =================================================
# FROTA - SENATRAN
# =================================================

PRIMEIRAS_COL_SENATRAN = ORDEM_LINHAS
COLUNAS_CRITICAS_FROTA = [
    "ano", 
    "uf", 
    "municipio"
]
COLUNAS_IDENTIFICADORAS_FROTA = [
    "ano", 
    "id_municipio"
]
COLUNAS_INT_FROTA = [
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
COLUNAS_SAIDA_FROTA = [
    "ano", 
    "id_municipio"
] + COLUNAS_INT_FROTA

# COMPONENTES_FROTA = COLUNAS_INT_FROTA exceto "total"
COMPONENTES_FROTA = [
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
