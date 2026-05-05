import pandas as pd
from pathlib import Path


def ler_excel(
    caminho: Path,
    aba          = 0,
    pular_linhas = 0,
    cabecalho    = 0,
    usar_colunas = None
):
    engine = _definir_engine(caminho)

    return pd.read_excel(
        caminho,
        sheet_name = aba,
        skiprows   = pular_linhas,
        header     = cabecalho,
        usecols    = usar_colunas,
        engine     = engine
    )


def _definir_engine(caminho: Path):
    extensao = caminho.suffix.lower()

    if extensao == ".xls":
        return "xlrd"

    if extensao == ".xlsx":
        return "openpyxl"

    if extensao == ".xlsb":
        return "pyxlsb"

    raise ValueError(
        f"Formato não suportado: {extensao}"
    )
