import pandas as pd
from collections.abc import Iterable


def concatenar(dfs: pd.DataFrame) -> pd.DataFrame:
    """
    Concatena múltiplos DataFrames em um só.
    """
    return pd.concat(dfs, ignore_index=True)


def ordenar_linhas(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """
    Ordena as linhas pelas colunas informadas.
    """
    colunas_validas = [
        c for c in colunas 
        if c in df.columns
    ]

    if colunas_validas:
        df = df.sort_values(colunas_validas)

    return df


def reordenar_colunas(df: pd.DataFrame, primeiras: Iterable[str]) -> pd.DataFrame:
    """
    Move as colunas informadas para o início.
    """
    restantes = [
        c for c in df.columns 
        if c not in primeiras
    ]

    return df[primeiras + restantes]
