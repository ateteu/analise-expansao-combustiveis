from pathlib import Path


def salvar_csv(df, pasta_saida: Path, nome_arquivo: str):
    """
    Salva um DataFrame em arquivo CSV (separador: ponto e vírgula).
    """
    caminho = pasta_saida / nome_arquivo
    df.to_csv(caminho, index = False, sep=";")

    print(f"Arquivo salvo em: {caminho}")
