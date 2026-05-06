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

    arquivo_str = arquivo.name.lower()

    # Identifica o tipo de combustível
    if "diesel" in arquivo_str:
        combustivel = "DIESEL"
    
    elif "gasolina" in arquivo_str:
        combustivel = "GASOLINA C"
    
    elif "etanol" in arquivo_str:
        combustivel = "ETANOL"

    # Atribui o nome às linhas (para garantir consistência de nomenclatura)
    df["COMBUSTIVEL"] = combustivel

    # Garante a tipagem correta nas colunas
    df = colunas_para_string(df, ["UF"])
    df = colunas_para_inteiro(df, ["ANO"])
    df = colunas_para_float(df, ["VOLUME_VENDIDO_M3"])

    # Garantir que UF tá certinho

    return df
