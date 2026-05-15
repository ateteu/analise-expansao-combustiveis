# Este arquivo contém esquemas do tipo:
# [coluna original] -> [nova coluna]

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
