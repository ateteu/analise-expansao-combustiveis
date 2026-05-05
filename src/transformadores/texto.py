import re
import pandas as pd
import unicodedata


def normalizar_texto(texto, separador = " "):
    """
    Padroniza texto para comparação:
    remove acentos, pontuação e espaços extras.

    OBS: Separador padrão é espaço.
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

    # Põe em maiúsculas e remove espaços nas bordas
    texto = texto.upper().strip()

    # Troca pontuação por espaço
    texto = re.sub(r"[^\w\s]", " ", texto)

    # Normaliza múltiplos espaços usando o separador definido
    texto = re.sub(r"\s+", separador, texto)

    # Remove separadores excedentes nas extremidades
    texto = texto.strip(separador)

    return texto
