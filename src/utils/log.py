SEPARADOR = "=" * 60
SIMBOLOS = {
    "sucesso" : "✓",
    "erro"    : "✗",
    "aviso"   : "⚠",
    "nenhum"  : "",
}


def log(
    mensagem: str,
    tipo: str = "nenhum",
    separador_antes: bool = False,
    separador_depois: bool = False,
) -> None:
    """
    Exibe uma mensagem padronizada no console.

    O argumento 'tipo' ("sucesso", "erro", "aviso" e "nenhum" (padrão)) 
    determina o símbolo utilizado.

    Os separadores antes e depois são opcionais.
    """
    if tipo not in SIMBOLOS:
        raise ValueError(
            f"Tipo de log inválido: '{tipo}'. "
            f"Use: {list(SIMBOLOS.keys())}"
        )

    if separador_antes:
        print(SEPARADOR)

    simbolo = SIMBOLOS[tipo]

    if simbolo:
        print(f"{simbolo} {mensagem}")
    else:
        print(mensagem)

    if separador_depois:
        print(SEPARADOR)


def log_etapa(
    nome: str,
    antes: int,
    depois: int,
    origem: str | None = None,
) -> None:
    """
    Registra uma etapa de processamento mostrando a variação
    no número de registros e a quantidade descartada.
    """
    descartadas = antes - depois
    prefixo = f"[{origem}] " if origem else ""

    log(
        f"{prefixo}{nome}: "
        f"{antes} → {depois} "
        f"({descartadas} descartadas)",
        tipo="sucesso",
    )


def log_resumo_item(
    rotulo: str,
    valor,
    separador_final: bool = False,
) -> None:
    """
    Exibe um item do resumo final de um pipeline.
    """
    print(f"  {rotulo:<22}: {valor}") # Deixa os ":" alinhados
    if separador_final:
        print(SEPARADOR)
