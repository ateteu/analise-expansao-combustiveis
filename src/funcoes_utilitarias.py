import pandas as pd
import re
from pathlib import Path


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

        return pd.read_excel(caminho, skiprows=linhas_a_pular, sheet_name=planilha_frota, engine="xlrd")
    
    elif caminho.suffix == ".xlsx":
        return pd.read_excel(caminho, skiprows=linhas_a_pular, engine="openpyxl")
    
    else:
        raise ValueError(f"Formato não suportado: {caminho.name}")


def verificar_se_existem_colunas_essenciais(df: pd.DataFrame, arquivo: Path):

    obrigatorias = ["UF", "MUNICIPIO"]

    for coluna in obrigatorias:
        if coluna not in df.columns:
            raise ValueError(f"Coluna '{coluna}' ausente em {arquivo.name}")


def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
    )
    return df


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    # remove linhas sem UF
    df = df[df["UF"].notna()]

    # remove cabeçalho duplicado
    df = df[df["UF"] != "UF"]

    # mantém apenas UF válida (2 letras)
    df = df[
        df["UF"].astype(str).str.len() == 2
    ]

    # remove linhas completamente vazias
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


def carregar_codigos_ibge(caminho: Path) -> pd.DataFrame:
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
        "Minas Gerais"   : "MG", 
        "São Paulo"      : "SP",
        "Rio de Janeiro" : "RJ", 
        "Espírito Santo" : "ES"
        # Adicionar mais estados se necessário
    }
    df["UF"] = df["UF"].str.strip().map(siglas)
    df["MUNICIPIO"] = df["MUNICIPIO"].str.strip().str.upper()
    df["ID_MUNICIPIO"] = df["ID_MUNICIPIO"].astype(str).str.strip()
    
    return df


def adicionar_codigo_ibge(df: pd.DataFrame, df_ibge: pd.DataFrame) -> pd.DataFrame:
    df["MUNICIPIO"] = df["MUNICIPIO"].str.strip().str.upper()
    df["UF"] = df["UF"].str.strip().str.upper()
    
    df = df.merge(df_ibge, on=["UF", "MUNICIPIO"], how="left")
    
    # Alerta se ficou algum município sem código
    sem_codigo = df[df["ID_MUNICIPIO"].isna()]["MUNICIPIO"].unique()
    if len(sem_codigo) > 0:
        print(f"⚠️  {len(sem_codigo)} municípios sem código IBGE encontrados!")
    
    return df
