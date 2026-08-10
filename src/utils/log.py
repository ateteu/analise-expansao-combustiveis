SEPARADOR = "=" * 60


def log(
    mensagem: str,
    valor=None,
    simbolo: str | None = None,
    separador_antes: bool = False,
    separador_depois: bool = False,
) -> None:
    """
    Exibe uma mensagem padronizada.

    Parâmetros
    ----------
    mensagem:
        Texto principal.

    valor:
        Valor opcional exibido após ':'.

    simbolo:
        Símbolo opcional exibido antes da mensagem
        (ex.: '✓', '⚠', '✗').

    separador_antes:
        Exibe uma linha separadora antes da mensagem.

    separador_depois:
        Exibe uma linha separadora após a mensagem.
    """

    if separador_antes:
        print(f"\n{SEPARADOR}")

    prefixo = f"{simbolo} " if simbolo else ""

    if valor is None:
        print(f"{prefixo}{mensagem}")
    else:
        print(f"{prefixo}{mensagem}: {valor}")

    if separador_depois:
        print(SEPARADOR)


def log_etapa(
    nome: str,
    antes: int,
    depois: int,
    origem: str = "",
    descricao: str = "descartadas",
) -> None:
    """
    Exibe o resultado de uma etapa que altera a quantidade de registros.
    """

    prefixo = f"[{origem}] " if origem else ""

    print(
        f"✓ {prefixo}{nome}: "
        f"{antes} → {depois} "
        f"({antes - depois} {descricao})"
    )


def log_resumo_item(rotulo: str, valor) -> None:
    """
    Exibe um item alinhado do resumo final.
    """

    print(f"  {rotulo:<22}: {valor}")
