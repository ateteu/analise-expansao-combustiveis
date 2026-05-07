import pandas as pd
from pathlib                   import Path
from arquivos.de_csv           import ler_csv
from transformadores.texto     import normalizar_texto
from configs.esquemas          import ESQUEMA_VENDAS_ANP
from transformadores.tipos     import (
    colunas_para_string,
    colunas_para_inteiro,
    colunas_para_float
)


def processar_arquivo_anp(arquivo: Path) -> pd.DataFrame:
    """
    Processa arquivo de vendas da ANP.

    - Lê o CSV com colunas definidas no esquema
    - Renomeia colunas
    - Define a coluna COMBUSTIVEL com base no nome do arquivo
    - Ajusta tipos (UF, ANO, VOLUME_VENDIDO_M3)

    Retorna DataFrame padronizado.
    """
    # Lê o arquivo csv e renomeia as colunas segundo o esquema
    # 'usar_colunas = ...' estava dando algum erro desconhecido
    df = ler_csv(arquivo)
    df = df.drop(columns = ["GRANDE REGIÃO","MUNICÍPIO"])
    df = df.rename(columns = ESQUEMA_VENDAS_ANP)

    mapeamento = {"ÓLEO DIESEL": "DIESEL"}
    df["COMBUSTIVEL"] = df["COMBUSTIVEL"].replace(mapeamento)

    duplicados = df.duplicated().sum()

    if duplicados > 0:
        print(f"! Duplicados encontrados: {duplicados}")
        df = df.drop_duplicates()

    # Padroniza decimal brasileiro
    df["VOLUME_VENDIDO_M3"] = (
        df["VOLUME_VENDIDO_M3"]
        .astype(str)
        .str.replace(",", ".", regex = False)
    )

    # Converte para número
    df["VOLUME_VENDIDO_M3"] = pd.to_numeric(
        df["VOLUME_VENDIDO_M3"],
        errors = "coerce"
    )

    # Garante a tipagem correta nas colunas
    df = colunas_para_string(df, ["UF"])
    df = colunas_para_inteiro(df, ["ANO"])

    # Garantir que UF tá certinho

    return df
