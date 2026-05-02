import pandas as pd
import re
from pathlib import Path
import unicodedata


def extrair_ano_do_nome_arquivo(nome_arquivo: Path) -> int:

    numeros_encontrados = re.findall(r'\d{2,4}', nome_arquivo)

    if not numeros_encontrados:
        raise ValueError(
            f"Nenhum número encontrado no nome do arquivo: {nome_arquivo}"
        )

    anos_validos = []

    # Primeiro tenta anos com 4 dígitos
    for valor in numeros_encontrados:
        if len(valor) == 4:
            ano = int(valor)
            if 2015 <= ano <= 2025: return ano

    # Se falhar acima, tenta anos com 2 dígitos
    for valor in numeros_encontrados:
        if len(valor) == 2:
            ano = int("20" + valor)
            if 2015 <= ano <= 2025: return ano
    
    # Nenhum dos casos acima
    raise ValueError(f"Nenhum ano válido encontrado: {nome_arquivo}")


def encontrar_linha_cabecalho(df_bruto: pd.DataFrame) -> int:

    for indice, linha in df_bruto.iterrows():
        valores = linha.astype(str).str.upper()

        if (
            valores.str.contains("UF", na=False).any() and
            valores.str.contains("MUNIC", na=False).any() and
            valores.str.contains("TOTAL", na=False).any()
        ):
            return indice
    
    raise ValueError("Cabeçalho não encontrado")


def ler_arquivo_bruto(caminho: Path) -> pd.DataFrame:

    if caminho.suffix == ".xls":
        # Arquivo de 2015 tem duas abas; a útil é "JUL_2015"
        planilha_frota = "JUL_2015" if "15" in caminho.name else 0

        return pd.read_excel(caminho, sheet_name=planilha_frota, header=None, engine="xlrd")
    
    elif caminho.suffix == ".xlsx":
        return pd.read_excel(caminho, header=None, engine="openpyxl")
    
    else:
        raise ValueError(f"Formato não suportado: {caminho.name}")


def ler_arquivo(caminho: Path, linhas_a_pular: int) -> pd.DataFrame:

    if caminho.suffix == ".xls":
        # Arquivo de 2015 tem duas abas; a útil é "JUL_2015"
        planilha_frota = "JUL_2015" if "15" in caminho.name else 0

        return pd.read_excel(
            caminho, 
            skiprows=linhas_a_pular, 
            sheet_name=planilha_frota, 
            engine="xlrd"
        )
    
    elif caminho.suffix == ".xlsx":
        return pd.read_excel(
            caminho, 
            skiprows=linhas_a_pular, 
            engine="openpyxl"
        )
    
    else:
        raise ValueError(f"Formato não suportado: {caminho.name}")


def verificar_se_existem_colunas_essenciais(df: pd.DataFrame, arquivo: Path):

    obrigatorias = ["UF", "MUNICIPIO"]

    for coluna in obrigatorias:
        if coluna not in df.columns:
            raise ValueError(f"Coluna '{coluna}' ausente em {arquivo.name}")


def padronizar_cabecalho_colunas(df: pd.DataFrame) -> pd.DataFrame:

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
    )
    return df


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:

    # Remove linhas sem UF
    df = df[
        df["UF"].notna()
    ]

    # Remove cabeçalho duplicado
    df = df[
        df["UF"] != "UF"
    ]

    # Mantém apenas linhas com UF válida (2 letras)
    df = df[
        df["UF"]
        .astype(str)
        .str.len() == 2
    ]

    # Remove linhas completamente vazias
    df = df.dropna(how="all")

    return df


def criar_coluna_ano(df: pd.DataFrame, ano: int) -> pd.DataFrame:

    df["ANO"] = ano
    cols = ["ANO"] + [c for c in df.columns if c != "ANO"]
    df = df[cols]

    return df


def concatenar_dfs_e_ordenar(dfs: list, ) -> pd.DataFrame:

    df = pd.concat(
        dfs, 
        ignore_index = True
    )

    df = df.sort_values(
        ["ANO", "UF", "MUNICIPIO"]
    )

    return df


def salvar_como_csv(df: pd.DataFrame, pasta_saida: str, nome_arquivo: str):

    caminho_saida = pasta_saida / nome_arquivo

    df.to_csv(
        caminho_saida, 
        index = False
    )
    print(f"\nArquivo final salvo em: {caminho_saida}")


def remover_acentos(texto):

    if pd.isna(texto): return texto
    
    return ''.join(
        # Separa acentos e simplifica caracteres compatíveis
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )


def normalizar_texto(texto):

    if pd.isna(texto):
        return texto

    # Remove acentos
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))

    # Maiúsculo + strip
    texto = texto.upper().strip()

    # Remove pontuação (mantém letras/números/espaço)
    texto = re.sub(r"[^\w\s]", " ", texto)

    # Remove espaços duplicados
    texto = re.sub(r"\s+", " ", texto)

    return texto


def padronizar_uf_e_municipio(df: pd.DataFrame) -> pd.DataFrame:

    df["MUNICIPIO"] = (
        df["MUNICIPIO"]
        .apply(normalizar_texto)
    )
    df["UF"] = (
        df["UF"]
        .str.strip()
        .str.upper()
    )
    return df


def carregar_e_padronizar_codigos_ibge(caminho: Path) -> pd.DataFrame:

    df = pd.read_excel(
        caminho,
        skiprows=6,    # Cabeçalho na linha 7, índice 6
        engine="xlrd", # Arquivo é um ".xls"
        usecols=[
            "Nome_UF", 
            "Código Município Completo", 
            "Nome_Município"
        ]
    )
    df.columns = ["UF", "ID_MUNICIPIO", "MUNICIPIO"]
    
    # Nome_UF vem por extenso: mapear pra sigla
    siglas = {
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

    # Troca os nomes completos de UF pelas siglas
    df["UF"] = (
        df["UF"]
        .str.strip()
        .map(siglas)
    )

    # Coloca o nome dos municípios em maiúsculo
    df["MUNICIPIO"] = (
        df["MUNICIPIO"]
        .apply(normalizar_texto)
    )

    # Padroniza o id dos municípios (cod. IBGE)
    df["ID_MUNICIPIO"] = (
        df["ID_MUNICIPIO"]
        .astype(str)
        .str.strip()
    )
    
    return df


def corrigir_municipios(df: pd.DataFrame) -> pd.DataFrame:

    correcoes = {
        ("BA", "LAGEDO DO TABOCAL")              : "LAJEDO DO TABOCAL",
        ("BA", "SANTA TERESINHA")                : "SANTA TEREZINHA",
        ("GO", "BOM JESUS")                      : "BOM JESUS DE GOIAS",
        ("MG", "AMPARO DA SERRA")                : "AMPARO DO SERRA",
        ("MG", "BARAO D0 MONTE ALTO")            : "BARAO DO MONTE ALTO",
        ("MG", "GOUVEA")                         : "GOUVEIA",
        ("MG", "QUELUZITA")                      : "QUELUZITO",
        ("MT", "POXOREO")                        : "POXOREU",
        ("MT", "SANTO ANTONIO DO LEVERGER")      : "SANTO ANTONIO DE LEVERGER",
        ("MT", "VILA BELA DA SANTISSIMA TRINDA") : "VILA BELA DA SANTISSIMA TRINDADE",
        ("PA", "ELDORADO DOS CARAJAS")           : "ELDORADO DO CARAJAS",
        ("PA", "SANTA ISABEL DO PARA")           : "SANTA IZABEL DO PARA",
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
        ("RN", "LAGOA DANTA")                    : "LAGOA D ANTA",
        ("RO", "NOVA DO MAMORE")                 : "NOVA MAMORE",
        ("RS", "SANTANA DO LIVRAMENTO")          : "SANT ANA DO LIVRAMENTO",
        ("SC", "BALNEARIO DE PICARRAS")          : "BALNEARIO PICARRAS",
        ("SC", "LAGEADO GRANDE")                 : "LAJEADO GRANDE",
        ("SC", "PRESIDENTE CASTELO BRANCO")      : "PRESIDENTE CASTELLO BRANCO",
        ("SC", "SAO LOURENCO D OESTE")           : "SAO LOURENCO DO OESTE",
        ("SC", "SAO MIGUEL D OESTE")             : "SAO MIGUEL DO OESTE",
        ("SE", "AMPARO DE SAO FRANCISCO")        : "AMPARO DO SAO FRANCISCO",
        ("TO", "COUTO DE MAGALHAES")             : "COUTO MAGALHAES",
    }

    df["MUNICIPIO"] = df.apply(
        lambda r: correcoes.get((r["UF"], r["MUNICIPIO"]), r["MUNICIPIO"]),
        axis=1
    )

    return df


def adicionar_codigo_ibge(df: pd.DataFrame, df_ibge: pd.DataFrame) -> pd.DataFrame:

    df = padronizar_uf_e_municipio(df)

    # Remove linhas sem município informado
    df = df[df["MUNICIPIO"] != "MUNICIPIO NAO INFORMADO"]

    df = corrigir_municipios(df)
    
    df = df.merge(
        df_ibge, 
        on=["UF", "MUNICIPIO"], 
        how="left"
    )

    # Caso o município não esteja mapeado pelo IBGE, cria o label NAO_MAPEADO
    df["STATUS_MUNICIPIO"] = df["ID_MUNICIPIO"].apply(
        lambda x: "OK" if pd.notna(x) else "NAO_MAPEADO"
    )
    
    # Alerta se ficou algum município sem código
    sem_codigo = df[df["ID_MUNICIPIO"].isna()]["MUNICIPIO"].unique()

    if len(sem_codigo) > 0:
        print(f"⚠️  {len(sem_codigo)} municípios sem código IBGE encontrados!")
    
    df_cidades_sem_codigo = (
        df[df["ID_MUNICIPIO"].isna()][["UF", "MUNICIPIO"]]
        .drop_duplicates()
        .sort_values(["UF", "MUNICIPIO"])
    )

    print(df_cidades_sem_codigo)

    return df
