import pandas as pd
from pathlib import Path


def salvar_csv(
    df           : pd.DataFrame,
    pasta_saida  : Path,
    nome_arquivo : str,
    separador    : str = ";",
    encoding     : str = "utf-8",
):
    """
    Salva um DataFrame como um CSV, utilizando por padrão
    ';' como separador e encoding utf-8.

    Retorna o caminho onde foi salvo o arquivo.
    """
    # Cria a pasta, caso ela não exista
    pasta_saida.mkdir(parents=True, exist_ok=True)

    caminho = pasta_saida / nome_arquivo

    df.to_csv(
        caminho,
        index=False,
        sep=separador,
        encoding=encoding,
    )

    return caminho


def salvar_quarentena(
    df           : pd.DataFrame,
    diretorio    : Path,
    nome_arquivo : str,
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
    print(f"\nQuarentena: {len(df)} linhas salvas\n")

    return caminho
