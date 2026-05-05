# Este arquivo contém esquemas do tipo:
# [coluna original] -> [nova coluna]

ESQUEMA_PIB = {
    "Ano"                                                  : "ANO",
    "Sigla da Unidade da Federação"                        : "UF",
    "Código do Município"                                  : "ID_MUNICIPIO",
    "Nome do Município"                                    : "MUNICIPIO",
    "Código da Região Geográfica Imediata"                 : "ID_RG_IMEDIATA",
    "Nome da Região Geográfica Imediata"                   : "RG_IMEDIATA",
    "Código da Região Geográfica Intermediária"            : "ID_RG_INTERMEDIARIA",
    "Nome da Região Geográfica Intermediária"              : "RG_INTERMEDIARIA",


    "Valor adicionado bruto da Agropecuária, " \
    "\na preços correntes\n(R$ 1.000)"                     : "VAB_AGROPECUARIA",


    "Valor adicionado bruto da Indústria,"     \
    "\na preços correntes\n(R$ 1.000)"                     : "VAB_INDUSTRIA",


    "Valor adicionado bruto dos Serviços,"              \
    "\na preços correntes \n"                           \
    "- exceto Administração, defesa, educação e saúde " \
    "públicas e seguridade social\n(R$ 1.000)"             : "VAB_SERVICOS",

    "Valor adicionado bruto da Administração, " \
    "defesa, educação e saúde públicas e "      \
    "seguridade social, \na preços correntes\n(R$ 1.000)"  : "VAB_ADMINISTRACAO_PUBLICA",


    "Valor adicionado bruto total, "     \
    "\na preços correntes\n(R$ 1.000)"                     : "VAB_TOTAL",


    "Produto Interno Bruto, "            \
    "\na preços correntes\n(R$ 1.000)"                     : "PIB",


    "Produto Interno Bruto per capita, " \
    "\na preços correntes\n(R$ 1,00)"                      : "PIB_PER_CAPITA",


    "Atividade com maior valor adicionado bruto"           : "ATIVIDADE_1",
    "Atividade com segundo maior valor adicionado bruto"   : "ATIVIDADE_2",
    "Atividade com terceiro maior valor adicionado bruto"  : "ATIVIDADE_3",
}


ESQUEMA_DOMINIO_IBGE = {
    "Nome_UF"                              : "UF",
    "Região Geográfica Intermediária"      : "ID_RG_INTERMEDIARIA",
    "Nome Região Geográfica Intermediária" : "RG_INTERMEDIARIA",
    "Região Geográfica Imediata"           : "ID_RG_IMEDIATA",
    "Nome Região Geográfica Imediata"      : "RG_IMEDIATA",
    "Código Município Completo"            : "ID_MUNICIPIO",
    "Nome_Município"                       : "MUNICIPIO"
}
