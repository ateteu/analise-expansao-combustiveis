import pandas as pd
from configs.constantes        import NOME_ABA_FROTA_2015
from configs.colunas           import COLUNAS_INT_SENATRAN
from transformadores.arquivos  import extrair_ano
from arquivos.de_excel         import ler_excel
from transformadores.texto     import normalizar_texto
from transformadores.tipos     import (
    colunas_para_string,
    colunas_para_inteiro
)


def _encontrar_linha_cabecalho(df_bruto: pd.DataFrame) -> int:
    """
    Procura a linha que contém o cabeçalho real.
    """
    for indice, linha in df_bruto.iterrows():
        valores = (
            linha
            .astype(str)
            .str.upper()
        )

        if (
            valores.str.contains("UF", na = False).any()
            and valores.str.contains("MUNIC", na = False).any()
            and valores.str.contains("TOTAL", na = False).any()
        ):
            return indice
    
    raise ValueError("Cabeçalho não encontrado no arquivo.")


def _remover_linhas_invalidas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove linhas vazias, cabeçalhos duplicados e linhas sem UF válida
    """
    df = df.dropna(how="all") # Remove linhas vazias
    df = df[df["UF"].notna()] # Remove linhas sem UF

    # Remove cabeçalho repetido
    df = df[
        df["UF"]
        .astype(str)
        .str.upper()
        != "UF"
    ]

    # Mantém apenas UFs válidas (2 chars)
    df = df[
        df["UF"]
        .astype(str)
        .str.len() == 2
    ]

    return df


def processar_arquivo_senatran(caminho):
    """
    Carrega, limpa e padroniza um arquivo de frota da SENATRAN.
    """
    # Arquivo de 2015 é o único com mais de uma aba
    ano = extrair_ano(caminho.name)
    if ano == 2015 : aba = NOME_ABA_FROTA_2015 
    else           : aba = 0

    df_bruto = ler_excel(caminho, aba, cabecalho = None)

    linha_cabecalho = _encontrar_linha_cabecalho(df_bruto)

    df = ler_excel(
        caminho, aba,
        pular_linhas = linha_cabecalho
    )

    df["ANO"] = ano # Add col ANO

    # Padroniza nomes do cabeçalho
    df.columns = df.columns.map(
        lambda col: normalizar_texto(col, separador = "_")
    )

    df = _remover_linhas_invalidas(df)

    # Garante que MUNICIPIO e UF são str e normaliza os textos
    df = colunas_para_string(df, ["MUNICIPIO", "UF"])
    df["MUNICIPIO"] = df["MUNICIPIO"].apply(normalizar_texto)
    df["UF"]        = df["UF"]       .apply(normalizar_texto)
    
    # Garante que demais colunas estão como int
    df = colunas_para_inteiro(df, COLUNAS_INT_SENATRAN)

    return df
