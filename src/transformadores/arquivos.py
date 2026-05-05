import re
from configs.constantes import (
    ANO_INICIO_ESCOPO_PROJETO,
    ANO_FIM_ESCOPO_PROJETO
)


def extrair_ano(nome_arquivo: str) -> int:
    """
    Extrai o ano do nome de um arquivo.
    Tenta primeiro anos com 4 dígitos, depois com 2 dígitos (prefixo '20').
    """
    numeros = re.findall(r"\d{2,4}", nome_arquivo)

    if not numeros:
        raise ValueError(
            f"Nenhum número encontrado no nome do arquivo: {nome_arquivo}"
        )

    for valor in numeros:
        if len(valor) == 4:
            ano = int(valor)
            if ANO_INICIO_ESCOPO_PROJETO <= ano <= ANO_FIM_ESCOPO_PROJETO:
                return ano

    for valor in numeros:
        if len(valor) == 2:
            ano = int("20" + valor)
            if ANO_INICIO_ESCOPO_PROJETO <= ano <= ANO_FIM_ESCOPO_PROJETO:
                return ano

    raise ValueError(
        f"Nenhum ano válido ({ANO_INICIO_ESCOPO_PROJETO} a {ANO_FIM_ESCOPO_PROJETO}) encontrado em: {nome_arquivo}"
    )
