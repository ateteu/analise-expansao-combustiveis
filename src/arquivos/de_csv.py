import pandas as pd
from configs.constantes import SEPARADOR_CSV
from pathlib            import Path


def ler_csv(
    caminho: Path,
    separador    = SEPARADOR_CSV,
    cabecalho    = 0,
    pular_linhas = 0,
    usar_colunas = None,
    encoding     = "utf-8-sig"
):
    """
    Lê um arquivo CSV e retorna um DataFrame.
    """
    return pd.read_csv(
        caminho,
        sep      = separador,
        header   = cabecalho,
        skiprows = pular_linhas,
        usecols  = usar_colunas,
        encoding = encoding
    )
