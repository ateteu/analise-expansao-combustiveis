# Este arquivo contém esquemas utilizados nos códigos.

# Um esquema define estrutura de dados.
# Ele responde:
# - quais colunas existem
# - como elas devem ser chamadas internamente
# - qual forma final o DataFrame deve ter


ESQUEMA_PIB = {
    "Ano"                                                  : "ano",
    "Código do Município"                                  : "id_municipio",


    "Valor adicionado bruto da Agropecuária, " \
    "\na preços correntes\n(R$ 1.000)"                     : "vab_agropecuaria",


    "Valor adicionado bruto da Indústria,"     \
    "\na preços correntes\n(R$ 1.000)"                     : "vab_industria",


    "Valor adicionado bruto dos Serviços,"              \
    "\na preços correntes \n"                           \
    "- exceto Administração, defesa, educação e saúde " \
    "públicas e seguridade social\n(R$ 1.000)"             : "vab_servicos",

    "Valor adicionado bruto da Administração, " \
    "defesa, educação e saúde públicas e "      \
    "seguridade social, \na preços correntes\n(R$ 1.000)"  : "vab_adm_publica",


    "Valor adicionado bruto total, "     \
    "\na preços correntes\n(R$ 1.000)"                     : "vab_total",


    "Produto Interno Bruto, "            \
    "\na preços correntes\n(R$ 1.000)"                     : "pib",


    "Produto Interno Bruto per capita, " \
    "\na preços correntes\n(R$ 1,00)"                      : "pib_per_capita",


    "Atividade com maior valor adicionado bruto"           : "atividade_1",
    "Atividade com segundo maior valor adicionado bruto"   : "atividade_2",
    "Atividade com terceiro maior valor adicionado bruto"  : "atividade_3",
}


ESQUEMA_DOMINIO_IBGE = {
    "Nome_UF"                       : "uf",
    "Código Município Completo"     : "id_municipio",
    "Nome_Município"                : "municipio"
}


ESQUEMA_VENDAS_ANP = {
    "ANO"         : "ano",
    "UF"          : "uf",
    "CÓDIGO IBGE" : "id_municipio",
    "PRODUTO"     : "tipo_combustivel",
    "VENDAS"      : "volume_vendido_m3"
}

ESQUEMA_TABELA_IBGE = {
    "UF"                                   : "id_uf",
    "Nome_UF"                              : "nome_uf",
    "Região Geográfica Intermediária"      : "id_reg_intermediaria",
    "Nome Região Geográfica Intermediária" : "nome_reg_intermediaria",
    "Região Geográfica Imediata"           : "id_reg_imediata",
    "Nome Região Geográfica Imediata"      : "nome_reg_imediata",
    "Código Município Completo"            : "id_municipio",
    "Nome_Município"                       : "nome_municipio"
}
