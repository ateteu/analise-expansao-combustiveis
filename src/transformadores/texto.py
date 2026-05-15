import re
import pandas as pd
import unicodedata


def normalizar_texto(texto, separador = " ", maiusculo = True):
    """
    Padroniza texto para comparação:
    remove acentos, pontuação e espaços extras.

    Parâmetros:
    - separador: separador usado entre palavras
    - maiusculo:
        True  -> maiúsculo
        False -> minúsculo
    """
    # Se o valor é nulo, retorna como está
    if pd.isna(texto):
        return texto

    # Remove acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        c for c in texto 
        if not unicodedata.combining(c)
    )

    # Define caixa
    if maiusculo:
        texto = texto.upper().strip()
    else:
        texto = texto.lower().strip()

    # Troca pontuação por espaço
    texto = re.sub(r"[^\w\s]", " ", texto)

    # Normaliza múltiplos espaços usando o separador definido
    texto = re.sub(r"\s+", separador, texto)

    # Remove separadores excedentes nas extremidades
    texto = texto.strip(separador)

    return texto
