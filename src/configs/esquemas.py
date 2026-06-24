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

ESQUEMA_TABELA_IBGE = {
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
# DADOS ECONÔMICOS - IBGE
# =========================================================

ESQUEMA_DADOS_ECONOMICOS = {
    "Ano",
    "Código do Município",

    "Valor adicionado bruto da Agropecuária, " \
    "\na preços correntes\n(R$ 1.000)",

    "Valor adicionado bruto da Indústria,"     \
    "\na preços correntes\n(R$ 1.000)",

    "Valor adicionado bruto dos Serviços,"              \
    "\na preços correntes \n"                           \
    "- exceto Administração, defesa, educação e saúde " \
    "públicas e seguridade social\n(R$ 1.000)",

    "Valor adicionado bruto da Administração, " \
    "defesa, educação e saúde públicas e "      \
    "seguridade social, \na preços correntes\n(R$ 1.000)",

    "Valor adicionado bruto total, "     \
    "\na preços correntes\n(R$ 1.000)",

    "Produto Interno Bruto, "            \
    "\na preços correntes\n(R$ 1.000)",

    "Produto Interno Bruto per capita, " \
    "\na preços correntes\n(R$ 1,00)",

    "Atividade com maior valor adicionado bruto",
    "Atividade com segundo maior valor adicionado bruto",
    "Atividade com terceiro maior valor adicionado bruto",
}
