import pandas as pd
from pathlib import Path
from utils import normalizar_texto


# ---------------------------------------------------------------------------
# Mapeamento de nomes de UF por extenso → sigla
# ---------------------------------------------------------------------------
_SIGLAS_UF = {
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
    "Tocantins"            : "TO"
}

# ---------------------------------------------------------------------------
# Correções de nomes de municípios que divergem entre bases
# Chave: (UF, nome_normalizado_na_base_origem)
# Valor: nome_normalizado_conforme_IBGE
# ---------------------------------------------------------------------------
_CORRECOES_MUNICIPIOS = {
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


def carregar_e_padronizar_codigos(caminho: Path) -> pd.DataFrame:
    """
    Lê a tabela de códigos IBGE de municípios e retorna um DataFrame
    padronizado com siglas de UF, nomes normalizados e IDs das regiões.
    """
    df = pd.read_excel(
        caminho,
        skiprows=6,   # cabeçalho na linha 7 (índice 6)
        engine="xlrd",
        usecols=[
            "Nome_UF",
            "Região Geográfica Intermediária",
            "Nome Região Geográfica Intermediária",
            "Região Geográfica Imediata",
            "Nome Região Geográfica Imediata",
            "Código Município Completo",
            "Nome_Município",
        ],
    )

    df.columns = [
        "UF",
        "ID_RG_INTERMEDIARIA",
        "RG_INTERMEDIARIA",
        "ID_RG_IMEDIATA",
        "RG_IMEDIATA",
        "ID_MUNICIPIO",
        "MUNICIPIO",
    ]

    # Nome por extenso → sigla
    df["UF"] = df["UF"].str.strip().map(_SIGLAS_UF)

    # Normaliza textos
    for col in ["MUNICIPIO", "RG_IMEDIATA", "RG_INTERMEDIARIA"]:
        df[col] = df[col].apply(normalizar_texto)

    # IDs como string
    for col in ["ID_MUNICIPIO", "ID_RG_IMEDIATA", "ID_RG_INTERMEDIARIA"]:
        df[col] = df[col].astype(str).str.strip()

    return df


def corrigir_municipios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige nomes de municípios que divergem entre a base de origem
    e a nomenclatura oficial do IBGE.
    """
    df["MUNICIPIO"] = df.apply(
        lambda r: _CORRECOES_MUNICIPIOS.get((r["UF"], r["MUNICIPIO"]), r["MUNICIPIO"]),
        axis=1,
    )
    return df


def adicionar_codigo_ibge(df: pd.DataFrame, df_ibge: pd.DataFrame) -> pd.DataFrame:
    """
    Faz o merge do DataFrame com a tabela IBGE usando UF + MUNICIPIO como chave.
    Emite alerta com os municípios que não encontrarem correspondência.
    """
    # Remove registros sem município informado
    df = df[df["MUNICIPIO"] != "MUNICIPIO NAO INFORMADO"].copy()

    df = corrigir_municipios(df)
    df = df.merge(df_ibge, on=["UF", "MUNICIPIO"], how="left")

    sem_codigo = df[
        df["ID_MUNICIPIO"].isna()
    ][["UF", "MUNICIPIO"]].drop_duplicates()

    if not sem_codigo.empty:
        print(f"\n⚠️  {len(sem_codigo)} município(s) sem código IBGE:")
        print(sem_codigo.sort_values(["UF", "MUNICIPIO"]).to_string(index=False))

    return df
