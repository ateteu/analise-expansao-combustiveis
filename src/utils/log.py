from pathlib import Path


# =========================================================
# CONFIGURAÇÕES
# =========================================================

SEPARADOR = "=" * 60
SIMBOLOS = {
    "sucesso" : "✓",
    "erro"    : "✗",
    "aviso"   : "⚠",
    "nenhum"  : "",
}

# =========================================================
# FUNÇÕES
# =========================================================

def log(
    rotulo: str,
    mensagem: str | Path = None,
    tipo: str = "nenhum",
    separador_antes: bool = False,
    separador_depois: bool = False,
) -> None:
    """
    Exibe uma mensagem padronizada no console.

    - O argumento 'tipo' ("sucesso", "erro", "aviso" e "nenhum" (padrão))
    determina o símbolo utilizado.
    - Quando 'rotulo' é informado, ele é alinhado à esquerda antes
    do separador ':'.
    - Os separadores antes e depois são opcionais.
    """
    if tipo not in SIMBOLOS:
        raise ValueError(
            f"Tipo de log inválido: '{tipo}'. "
            f"Use um destes: {list(SIMBOLOS.keys())}"
        )

    if separador_antes:
        print(SEPARADOR)

    simbolo = SIMBOLOS[tipo]
    prefixo = f"{simbolo} " if simbolo else ""

    # Printa "rotulo : mensagem"
    if mensagem is not None:
        print(f"{prefixo}{rotulo:<25}: {mensagem}")

    # Printa "rotulo"
    else:
        print(f"{prefixo}{rotulo}")

    if separador_depois:
        print(SEPARADOR)


def log_etapa(
    nome: str,
    antes: int,
    depois: int,
) -> None:
    """
    Registra uma etapa de processamento mostrando a variação
    no número de registros e a quantidade descartada.
    """
    descartadas = antes - depois

    log(
        rotulo=f"{nome}",
        mensagem=f"{antes} → {depois} ({descartadas} descartadas)",
        tipo="sucesso",
    )
