import re
import pandas as pd
import unicodedata

from collections.abc import Collection


def normalizar_texto(
    texto,
    separador: str = " ",
    maiusculo: bool | None = True,
    remover_acentos: bool = True,
    remover_pontuacao: bool = True,
    strings_nulas: Collection[str] | None = None,
):
    """
    Padroniza texto para comparação e limpeza.

    Parâmetros
    ----------
    - separador: Separador usado entre palavras.
    - maiusculo: True - maiúsculo, False - minúsculo, None - mantém capitalização.
    - remover_acentos: Remove acentos e diacríticos.
    - remover_pontuacao: Remove pontuação, substituindo por espaço.
    - strings_nulas: Conjunto de valores que devem ser tratados como ausentes.
    """

    if pd.isna(texto):
        return pd.NA

    texto = str(texto).strip()

    # Normaliza espaços múltiplos
    texto = " ".join(texto.split())

    # Normalização unicode
    if remover_acentos:
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(
            c for c in texto
            if not unicodedata.combining(c)
        )
    else:
        texto = unicodedata.normalize("NFKC", texto)

    # Caixa
    if maiusculo is True:
        texto = texto.upper()
    elif maiusculo is False:
        texto = texto.lower()

    # Pontuação
    if remover_pontuacao:
        texto = re.sub(r"[^\w\s]", " ", texto)

    # Espaços
    texto = re.sub(r"\s+", separador, texto)
    texto = texto.strip(separador)

    # Nulos lógicos
    if strings_nulas is not None and texto in strings_nulas:
        return pd.NA

    return texto