def log_etapa(
        nome, 
        antes, 
        depois, 
        origem = None
    ):
    """
    Log genérico de variação de linhas entre etapas.
    """
    descartadas = antes - depois

    prefixo = f"[{origem}] " if origem else ""

    print(
        f"{prefixo}{nome}: "
        f"{antes} → {depois} "
        f"({descartadas} descartadas)"
    )
