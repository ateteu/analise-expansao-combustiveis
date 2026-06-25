from configs.colunas import COLUNAS_INT_FROTA

# Este arquivo contém esquemas utilizados nos códigos.

# Um esquema define estrutura de dados.
# Ele responde:
# - quais colunas existem
# - como elas devem ser chamadas internamente
# - qual forma final o DataFrame deve ter

# =========================================================
# COORD MUNICÍPIOS - GITHUB/KELVINS
# =========================================================

ESQUEMA_ORIGINAL_COORD_MUNICIPIOS = {
    "codigo_ibge",
    "nome",
    "latitude",
    "longitude",
    "capital",
    "codigo_uf",
    "siafi_id",
    "ddd",
    "fuso_horario"
}

# =========================================================
# VENDAS DE COMBUSTÍVEIS - ANP
# =========================================================

ESQUEMA_ORIGINAL_VENDAS = {
    "ANO",
    "UF",
    "GRANDE REGIÃO",
    "PRODUTO",
    "CÓDIGO IBGE",
    "MUNICÍPIO",
    "VENDAS"
}

# =========================================================
# CODIGOS DE MUNICIPIOS, UFS E REGIÕES - IBGE
# =========================================================

ESQUEMA_CODIGOS_IBGE = {
    "UF",
    "Nome_UF",
    "Região Geográfica Intermediária",
    "Nome Região Geográfica Intermediária",
    "Região Geográfica Imediata",
    "Nome Região Geográfica Imediata",
    "Código Município Completo",
    "Nome_Município",
}

# =========================================================
# DADOS DE FROTA - SENATRAN
# =========================================================

ESQUEMA_FROTA = {"uf", "municipio"} | set(COLUNAS_INT_FROTA)
