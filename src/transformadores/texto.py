import re
import pandas as pd
import unicodedata


def normalizar_texto(
    texto,
    separador=" ",
    maiusculo=True,
    remover_acentos=True,
    remover_pontuacao=True,
    strings_nulas=None,
):
    """
    Padroniza texto para comparação e limpeza.

    Parâmetros
    ----------
    separador : str
        Separador usado entre palavras.

    maiusculo : bool
        True  -> converte para maiúsculo.
        False -> converte para minúsculo.

    remover_acentos : bool
        Remove acentos e diacríticos.

    remover_pontuacao : bool
        Remove pontuação, substituindo por espaço.

    strings_nulas : collection[str] | None
        Conjunto de valores que devem ser tratados como ausentes.
        A comparação ocorre após a normalização.
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
    texto = texto.upper() if maiusculo else texto.lower()

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