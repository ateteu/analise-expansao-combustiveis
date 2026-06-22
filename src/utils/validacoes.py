def validar_esquema(
        df, 
        esperado,
        origem = None
    ):
    """
    Valida se o DataFrame possui exatamente as colunas esperadas.
    """

    recebidas = set(df.columns)
    esperado  = set(esperado)

    if recebidas != esperado:
        faltando = esperado - recebidas
        sobrando = recebidas - esperado

        prefixo = f"[{origem}] " if origem else ""

        raise ValueError(
            f"{prefixo}Schema inválido.\n"
            f"Faltando: {sorted(faltando)}\n"
            f"Sobrando: {sorted(sobrando)}"
        )
