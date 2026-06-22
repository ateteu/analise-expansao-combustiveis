import pandas as pd
from pathlib                   import Path
from transformadores.dataframe import limpar_nomes_colunas
from detectar_encoding         import detectar_encoding


def ler_excel(
    caminho: Path,
    aba          = 0,
    pular_linhas = 0,
    cabecalho    = 0,
    usar_colunas = None
):
    """
    Lê um arquivo Excel e retorna um DataFrame.

    Ajusta automaticamente o engine com base na extensão do arquivo.
    """
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
    """
    Retorna o engine do pandas apropriado para a extensão do arquivo Excel.
    """
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


def ler_csv(
    caminho: Path,
    separador     = ";",
    cabecalho     = 0,
    pular_linhas  = 0,
    usar_colunas  = None,
    encoding      = "auto",
    forcar_string = True,
) -> pd.DataFrame:
    """
    Lê um CSV de forma conservadora.

    Por padrão:
    - encoding="auto": detecta o encoding em vez de assumir um fixo.
    - forcar_string=True: lê tudo como string, sem inferência de tipo do
      pandas. Conversão de tipos é responsabilidade explícita do pipeline.
    - keep_default_na=False: strings como "NA"/"NULL"/"-" não são
      convertidas para NaN automaticamente. Tratar isso é responsabilidade
      explícita do pipeline (ex: via normalizar_texto).
    - Remove BOM e espaços das bordas dos nomes das colunas.
    """

    if encoding == "auto":
        enc = detectar_encoding(caminho)
    else:
        enc = encoding

    df = pd.read_csv(
        caminho,
        sep             = separador,
        header          = cabecalho,
        skiprows        = pular_linhas,
        usecols         = usar_colunas,
        encoding        = enc,
        dtype           = str if forcar_string else None,
        keep_default_na = False,
    )

    return limpar_nomes_colunas(df)
