import pandas as pd
from pathlib import Path


def salvar_csv(
    df        : pd.DataFrame,
    caminho   : Path,
    separador : str = ";",
    encoding  : str = "utf-8",
):
    """
    Salva um DataFrame como um CSV, utilizando por padrão
    ';' como separador e encoding utf-8.

    Retorna o caminho onde foi salvo o arquivo.
    """
    
    # Cria a pasta, caso ela não exista
    caminho.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        caminho,
        index=False,
        sep=separador,
        encoding=encoding,
    )

    return caminho


def salvar_quarentena(
    df      : pd.DataFrame,
    caminho : Path,
):
    """
    Salva registros descartados para auditoria.
    Nome do arquivo é obrigatório para garantir rastreabilidade.
    """
    if df.empty:
        return None

    if not caminho:
        raise ValueError("'caminho' é obrigatório!")

    caminho = salvar_csv(df, caminho)

    return caminho
