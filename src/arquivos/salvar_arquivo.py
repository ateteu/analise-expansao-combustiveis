from pathlib import Path


def salvar_csv(
    df,
    pasta_saida: Path,
    nome_arquivo: str,
    sep=";",
    encoding="utf-8",
):
    """
    Salva um DataFrame como um CSV, utilizando por padrão
    ';' como separador e encoding utf-8.

    Retorna o caminho onde foi salvo o arquivo.
    """
    caminho = pasta_saida / nome_arquivo

    df.to_csv(
        caminho,
        index=False,
        sep=sep,
        encoding=encoding,
    )

    print(f"\nArquivo salvo em: {caminho}")
    return caminho


def salvar_quarentena(
    df,
    diretorio: Path,
    nome_arquivo: str,
):
    """
    Salva registros descartados para auditoria.
    """
    if df.empty:
        return

    caminho = salvar_csv(
        df,
        diretorio,
        nome_arquivo,
    )

    print(
        f"Quarentena: "
        f"{len(df)} linhas salvas em '{caminho}'"
    )
