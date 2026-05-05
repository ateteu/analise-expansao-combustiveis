import pandas as pd
from collections.abc import Iterable


def colunas_para_string(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """
    Converte as colunas informadas para string e aplica trim.
    """
    for col in colunas:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

    return df


def colunas_para_inteiro(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """
    Converte as colunas informadas para inteiro.
    """
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors = "coerce"
            ).astype("Int64")

    return df


def colunas_para_float(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """
    Converte as colunas informadas para float.
    """
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors = "coerce"
            ).astype(float)

    return df


def colunas_para_numero(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """
    Converte as colunas informadas para tipo numérico (int ou float).
    """
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors = "coerce"
            )

    return df
