import pandas as pd

from pathlib                 import Path
from arquivos.salvar_arquivo import salvar_quarentena
from utils.log               import log_etapa


def validar_esquema(
        df        : pd.DataFrame, 
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
            f"{prefixo}Esquema inválido.\n"
            f"Faltando: {sorted(faltando)}\n"
            f"Sobrando: {sorted(sobrando)}"
        )


def validar_existencia_em_referencia(
    df             : pd.DataFrame,
    df_ref         : pd.DataFrame,
    chaves_df      : list[str],
    chaves_df_ref  : list[str],
    caminho        : Path,
):
    """
    Valida, por comparação de tuplas de chaves compostas, 
    se combinações de colunas do df existem no df_ref.
    """

    if len(chaves_df) != len(chaves_df_ref):
        raise ValueError(
            "'chaves_df' e 'chaves_df_ref' devem ter o mesmo tamanho."
        )

    if not caminho:
        raise ValueError("É obrigatório informar 'caminho'!")

    n_antes = len(df)

    # Conjunto de chaves válidas da referência
    ref_set = set(
        zip(*(df_ref[col] for col in chaves_df_ref))
    )

    chaves_df = list(
        zip(*(df[col] for col in chaves_df))
    )

    linhas_com_chave_valida = pd.Series(
        [chave in ref_set for chave in chaves_df],
        index=df.index
    )

    df_invalidos = df[~linhas_com_chave_valida]

    if not df_invalidos.empty:
        salvar_quarentena(
            df_invalidos,
            caminho
        )

    df_validos = df[linhas_com_chave_valida]

    log_etapa(
        "Validação referência",
        n_antes,
        len(df_validos),
    )

    return df_validos


def validar_unicidade(df: pd.DataFrame, coluna: str) -> None:
    """
    Levanta erro se a coluna tiver valores duplicados.
    """
    duplicados = df[df[coluna].duplicated(keep=False)]
    if not duplicados.empty:
        raise ValueError(
            f"Encontrados {duplicados[coluna].nunique()} valores duplicados em '{coluna}'."
        )


def validar_prefixo(
    df              : pd.DataFrame,
    coluna_completa : str,
    coluna_prefixo  : str,
    tamanho         : int,
) -> None:
    """
    Levanta erro se o prefixo de coluna_completa não bater com coluna_prefixo.
    """
    inconsistentes = df[df[coluna_completa].str[:tamanho] != df[coluna_prefixo]]
    if not inconsistentes.empty:
        raise ValueError(
            f"Encontrados {len(inconsistentes)} registros com prefixo inconsistente "
            f"entre '{coluna_completa}' e '{coluna_prefixo}'."
        )
