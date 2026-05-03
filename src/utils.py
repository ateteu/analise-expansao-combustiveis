import re
import pandas as pd
import unicodedata
from pathlib import Path


def normalizar_texto(texto) -> str:
    """
    Normaliza uma string para comparação:
    remove acentos, converte para maiúsculo, remove pontuação
    e colapsa espaços duplicados.
    """
    if pd.isna(texto):
        return texto

    # Remove acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))

    # Maiúsculo + strip
    texto = texto.upper().strip()

    # Remove pontuação (mantém letras, números e espaço)
    texto = re.sub(r"[^\w\s]", " ", texto)

    # Colapsa espaços duplicados
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def extrair_ano_do_nome_arquivo(nome_arquivo: str) -> int:
    """
    Extrai o ano (2015-2025) do nome de um arquivo.
    Tenta primeiro anos com 4 dígitos, depois com 2 dígitos (prefixo '20').
    """
    numeros = re.findall(r"\d{2,4}", nome_arquivo)

    if not numeros:
        raise ValueError(f"Nenhum número encontrado no nome do arquivo: {nome_arquivo}")

    for valor in numeros:
        if len(valor) == 4:
            ano = int(valor)
            if 2015 <= ano <= 2025:
                return ano

    for valor in numeros:
        if len(valor) == 2:
            ano = int("20" + valor)
            if 2015 <= ano <= 2025:
                return ano

    raise ValueError(f"Nenhum ano válido (2015-2025) encontrado em: {nome_arquivo}")


def concatenar_dfs_e_ordenar(dfs: list[pd.DataFrame], ordem_colunas: list[str] = None) -> pd.DataFrame:
    """
    Concatena uma lista de DataFrames e ordena pelas colunas indicadas.
    Se nenhuma coluna for passada, ordena por ANO, UF, MUNICIPIO (se existirem).
    """
    df = pd.concat(dfs, ignore_index=True)

    if ordem_colunas is None:
        ordem_colunas = [c for c in ["ANO", "UF", "MUNICIPIO"] if c in df.columns]

    if ordem_colunas:
        df = df.sort_values(ordem_colunas)

    return df


def reordenar_colunas(df: pd.DataFrame, primeiras: list[str]) -> pd.DataFrame:
    """
    Move as colunas listadas em `primeiras` para o início do DataFrame,
    mantendo o restante na ordem original.
    """
    restantes = [c for c in df.columns if c not in primeiras]
    return df[primeiras + restantes]


def salvar_como_csv(df: pd.DataFrame, pasta_saida: Path, nome_arquivo: str) -> None:
    """
    Salva o DataFrame como CSV no diretório indicado.
    """   
    caminho = pasta_saida / nome_arquivo
    df.to_csv(caminho, index=False)
    
    print(f"\nArquivo salvo em: {caminho}")
