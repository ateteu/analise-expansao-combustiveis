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


def converter_decimal_br(df, colunas):
    """
    Converte colunas com valores numéricos no formato decimal brasileiro
    (ponto como separador de milhar, vírgula como separador decimal) para float.
 
    Aplica strip() antes da conversão para remover espaços residuais.
    Valores inválidos viram NaN (via errors="coerce").
 
    Exemplo de entrada:  "1.234,56"
    Exemplo de saída:    1234.56
    """
    for coluna in colunas:
        df[coluna] = (
            df[coluna]
            .str.strip()
            .str.replace(".", "", regex=False)   # remove separador de milhar
            .str.replace(",", ".", regex=False)  # decimal BR → ponto
        )
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df
