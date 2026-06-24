import pandas as pd
from pathlib import Path


def salvar_csv(
    df: pd.Dataframe,
    pasta_saida: Path,
    nome_arquivo: str,
    separador=";",
    encoding="utf-8",
):
    """
    Salva um DataFrame como um CSV, utilizando por padrão
    ';' como separador e encoding utf-8.

    Retorna o caminho onde foi salvo o arquivo.
    """
    caminho = pasta_saida / nome_arquivo

    df.to_csv(
        caminho,
        index=False,
        sep=separador,
        encoding=encoding,
    )

    return caminho


def salvar_quarentena(
    df: pd.Dataframe,
    diretorio: Path,
    nome_arquivo: str,
):
    """
    Salva registros descartados para auditoria.
    Nome do arquivo é obrigatório para garantir rastreabilidade.
    """
    if df.empty:
        return None

    if not nome_arquivo:
        raise ValueError("'nome_arquivo' é obrigatório!")

    caminho = salvar_csv(df, diretorio, nome_arquivo)
    print(f"Quarentena: {len(df)} linhas salvas em '{caminho}'")

    return caminho
