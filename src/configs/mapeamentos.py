# Este arquivo contém mapeamentos utilizados nos códigos.

# Um mapa define correspondência entre valores ou códigos, não estrutura.
# Ele responde:
# - como converter um valor em outro
# - como traduzir categorias
# - como enriquecer dados

# =========================================================
# GERAIS
# =========================================================

MAPA_UF_SIGLA = {
    "RO": "11", "AC": "12", "AM": "13", "RR": "14", "PA": "15", "AP": "16", "TO": "17",
    "MA": "21", "PI": "22", "CE": "23", "RN": "24", "PB": "25", "PE": "26", "AL": "27","SE": "28","BA": "29",
    "MG": "31", "ES": "32", "RJ": "33", "SP": "35",
    "PR": "41", "SC": "42", "RS": "43",
    "MS": "50", "MT": "51", "GO": "52", "DF": "53",
}
SIGLAS_UF = {
    "Acre"                 : "AC",
    "Alagoas"              : "AL",
    "Amapá"                : "AP",
    "Amazonas"             : "AM",
    "Bahia"                : "BA",
    "Ceará"                : "CE",
    "Distrito Federal"     : "DF",
    "Espírito Santo"       : "ES",
    "Goiás"                : "GO",
    "Maranhão"             : "MA",
    "Mato Grosso"          : "MT",
    "Mato Grosso do Sul"   : "MS",
    "Minas Gerais"         : "MG",
    "Pará"                 : "PA",
    "Paraíba"              : "PB",
    "Paraná"               : "PR",
    "Pernambuco"           : "PE",
    "Piauí"                : "PI",
    "Rio de Janeiro"       : "RJ",
    "Rio Grande do Norte"  : "RN",
    "Rio Grande do Sul"    : "RS",
    "Rondônia"             : "RO",
    "Roraima"              : "RR",
    "Santa Catarina"       : "SC",
    "São Paulo"            : "SP",
    "Sergipe"              : "SE",
    "Tocantins"            : "TO",
}

# =========================================================
# VENDAS DE COMBUSTÍVEIS - ANP
# =========================================================

MAPA_VENDAS = {
    "ANO"           : "ano",
    "UF"            : "uf",
    "GRANDE REGIÃO" : "nome_grande_regiao",
    "PRODUTO"       : "tipo_combustivel",
    "CÓDIGO IBGE"   : "id_municipio",
    "MUNICÍPIO"     : "nome_municipio", 
    "VENDAS"        : "vol_vendido_m3",
}

# =========================================================
# CODIGOS DE MUNICIPIOS, UFS E REGIÕES - IBGE
# =========================================================

MAPA_CODIGOS_IBGE = {
    "UF"                                   : "id_uf",
    "Nome_UF"                              : "nome_uf",
    "Região Geográfica Intermediária"      : "id_regiao_intermediaria",
    "Nome Região Geográfica Intermediária" : "nome_regiao_intermediaria",
    "Região Geográfica Imediata"           : "id_regiao_imediata",
    "Nome Região Geográfica Imediata"      : "nome_regiao_imediata",
    "Código Município Completo"            : "id_municipio",
    "Nome_Município"                       : "nome_municipio"
}

# =========================================================
# DADOS ECONÔMICOS - IBGE
# =========================================================

MAPA_DADOS_ECONOMICOS = {
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

# =========================================================
# FROTA - SENATRAN
# =========================================================

CORRECOES_MUNICIPIOS = {
    ("BA", "LAGEDO DO TABOCAL")              : "LAJEDO DO TABOCAL",
    ("BA", "SANTA TERESINHA")                : "SANTA TEREZINHA",
    ("GO", "BOM JESUS")                      : "BOM JESUS DE GOIAS",
    ("MG", "AMPARO DA SERRA")                : "AMPARO DO SERRA",
    ("MG", "BARAO D0 MONTE ALTO")            : "BARAO DO MONTE ALTO",
    ("MG", "BRASOPOLIS")                     : "BRAZOPOLIS",
    ("MG", "GOUVEA")                         : "GOUVEIA",
    ("MG", "QUELUZITA")                      : "QUELUZITO",
    ("MT", "POXOREO")                        : "POXOREU",
    ("MT", "SANTO ANTONIO DO LEVERGER")      : "SANTO ANTONIO DE LEVERGER",
    ("MT", "VILA BELA DA SANTISSIMA TRINDA") : "VILA BELA DA SANTISSIMA TRINDADE",
    ("PA", "ELDORADO DOS CARAJAS")           : "ELDORADO DO CARAJAS",
    ("PA", "SANTA ISABEL DO PARA")           : "SANTA IZABEL DO PARA",
    ("PB", "CAMPO DE SANTANA")               : "TACIMA",
    ("PB", "SANTAREM")                       : "JOCA CLAUDINO",
    ("PB", "SAO DOMINGOS DE POMBAL")         : "SAO DOMINGOS",
    ("PE", "BELEM DE SAO FRANCISCO")         : "BELEM DO SAO FRANCISCO",
    ("PE", "IGUARACI")                       : "IGUARACY",
    ("PE", "LAGOA DO ITAENGA")               : "LAGOA DE ITAENGA",
    ("PI", "SAO FRANCISCO DE ASSIS DO PIAU") : "SAO FRANCISCO DE ASSIS DO PIAUI",
    ("PR", "BELA VISTA DO CAROBA")           : "BELA VISTA DA CAROBA",
    ("PR", "MUNHOZ DE MELLO")                : "MUNHOZ DE MELO",
    ("PR", "PINHAL DO SAO BENTO")            : "PINHAL DE SAO BENTO",
    ("PR", "SANTA CRUZ DO MONTE CASTELO")    : "SANTA CRUZ DE MONTE CASTELO",
    ("RJ", "ARMACAO DE BUZIOS")              : "ARMACAO DOS BUZIOS",
    ("RJ", "PARATI")                         : "PARATY",
    ("RJ", "TRAJANO DE MORAIS")              : "TRAJANO DE MORAES",
    ("RN", "ASSU")                           : "ACU",
    ("RN", "BOA SAUDE")                      : "JANUARIO CICCO",
    ("RN", "LAGOA DANTA")                    : "LAGOA D ANTA",
    ("RO", "NOVA DO MAMORE")                 : "NOVA MAMORE",
    ("RS", "SANTANA DO LIVRAMENTO")          : "SANT ANA DO LIVRAMENTO",
    ("SC", "BALNEARIO DE PICARRAS")          : "BALNEARIO PICARRAS",
    ("SC", "LAGEADO GRANDE")                 : "LAJEADO GRANDE",
    ("SC", "PRESIDENTE CASTELO BRANCO")      : "PRESIDENTE CASTELLO BRANCO",
    ("SC", "SAO LOURENCO D OESTE")           : "SAO LOURENCO DO OESTE",
    ("SC", "SAO MIGUEL D OESTE")             : "SAO MIGUEL DO OESTE",
    ("SE", "AMPARO DE SAO FRANCISCO")        : "AMPARO DO SAO FRANCISCO",
    ("SP", "EMBU")                           : "EMBU DAS ARTES",
    ("TO", "COUTO DE MAGALHAES")             : "COUTO MAGALHAES",
    ("TO", "FORTALEZA DO TABOCAO")           : "TABOCAO",
    ("TO", "SAO VALERIO DA NATIVIDADE")      : "SAO VALERIO",
}


# =========================================================
# COORDENADAS - GITHUB/KELVINS
# =========================================================

MAPA_COORD_MUNICIPIOS = {
    "codigo_ibge" : "id_municipio",
    "latitude"    : "latitude",
    "longitude"   : "longitude",
}
