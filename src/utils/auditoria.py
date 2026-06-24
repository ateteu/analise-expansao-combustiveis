import pandas as pd

from typing                  import Sequence
from re                      import Pattern
from arquivos.salvar_arquivo import salvar_quarentena
from utils.log               import log_etapa


# Funções genéricas de auditoria e qualidade de dados.

# Convenções das funções implementadas nesse arquivo:
# - Recebem um DataFrame e retornam o DataFrame filtrado (apenas linhas válidas).
# - Linhas descartadas são salvas em quarentena antes da remoção.
# - Logam o número de linhas descartadas em cada etapa.

# ============================================================

def separar_nulos(
    df              : pd.DataFrame,
    colunas         : Sequence[str],
    pasta_auditoria : str,
    prefixo         : str = "",
) -> pd.DataFrame:
    """
    Separa e envia à quarentena linhas com ausências nas colunas informadas.
    Retorna apenas as linhas válidas.
    """
    n_antes = len(df)
    mask_nulos = df[colunas].isnull().any(axis=1)

    salvar_quarentena(
        df[mask_nulos].copy(), 
        pasta_auditoria, 
        f"nulos_{prefixo}.csv"
    )

    df = df[~mask_nulos].copy()
    log_etapa("Nulos críticos", n_antes, len(df), prefixo)

    return df


# ============================================================

def validar_regex(
    df              : pd.DataFrame,
    coluna          : str,
    regex           : str | Pattern[str],
    pasta_auditoria : str,
    prefixo         : str = "",
) -> pd.DataFrame:
    """
    Mantém apenas linhas onde a coluna corresponde ao padrão regex
    (padrão regex esperado (ex: r'^\d{7}$')).

    Linhas fora do padrão vão para quarentena.
    """
    n_antes = len(df)
    mask = df[coluna].str.match(regex, na=False)

    salvar_quarentena(
        df[~mask].copy(), 
        pasta_auditoria, 
        f"formato_{coluna}_{prefixo}.csv"
    )

    df = df[mask].copy()
    log_etapa(f"Formato {coluna}", n_antes, len(df), prefixo)

    return df


# ============================================================

def validar_dominio(
    df              : pd.DataFrame,
    coluna          : str,
    valores_validos : set[str],
    pasta_auditoria : str,
    prefixo         : str = "",
) -> pd.DataFrame:
    """
    Mantém apenas linhas cujo valor da coluna está no conjunto informado.
    Linhas fora do domínio vão para quarentena.
    """
    n_antes = len(df)
    mask = df[coluna].isin(valores_validos)

    salvar_quarentena(
        df[~mask].copy(), 
        pasta_auditoria, 
        f"dominio_{coluna}_{prefixo}.csv"
    )

    df = df[mask].copy()
    log_etapa(f"Domínio {coluna}", n_antes, len(df), prefixo)

    return df


# ============================================================

def validar_intervalo(
    df              : pd.DataFrame,
    coluna          : str,
    minimo          : int | float,
    maximo          : int | float,
    pasta_auditoria : str,
    prefixo         : str = "",
) -> pd.DataFrame:
    """
    Mantém apenas linhas cujo valor da coluna está dentro de [minimo, maximo].
    Linhas fora do intervalo vão para quarentena.
    """
    n_antes = len(df)
    mask = df[coluna].between(minimo, maximo)

    salvar_quarentena(
        df[~mask].copy(), 
        pasta_auditoria, 
        f"fora_intervalo_{coluna}_{prefixo}.csv"
    )

    df = df[mask].copy()
    log_etapa(f"Intervalo {coluna}", n_antes, len(df), prefixo)

    return df


# ============================================================

def validar_minimo(
    df              : pd.DataFrame,
    coluna          : str,
    minimo          : int | float,
    pasta_auditoria : str,
    prefixo         : str = "",
) -> pd.DataFrame:
    """
    Mantém apenas linhas cujo valor da coluna é >= minimo.
    Linhas abaixo do mínimo vão para quarentena.
    """
    n_antes = len(df)
    mask = df[coluna] >= minimo

    salvar_quarentena(
        df[~mask].copy(),
        pasta_auditoria, 
        f"abaixo_minimo_{coluna}_{prefixo}.csv"
    )

    df = df[mask].copy()
    log_etapa(f"Mínimo {coluna}", n_antes, len(df), prefixo)

    return df


# ============================================================

def tratar_duplicidades(
    df              : pd.DataFrame,
    chave_logica    : Sequence[str],
    pasta_auditoria : str,
    prefixo         : str = "",
) -> pd.DataFrame:
    """
    Trata duplicidades de forma conservadora.

    - Duplicata exata (linha inteira repetida): mantém uma ocorrência.
    - Duplicata lógica (mesma chave, valores distintos): envia à quarentena
      e remove do fluxo principal.

    Não soma automaticamente para não mascarar erros de origem.
    """
    n_antes = len(df)

    mask_exatas = df.duplicated(keep=False)

    salvar_quarentena(
        df[mask_exatas].copy(), 
        pasta_auditoria, 
        f"duplicatas_exatas_{prefixo}.csv"
    )

    df = df.drop_duplicates(keep="first").copy()
    mask_logicas = df.duplicated(subset=chave_logica, keep=False)

    salvar_quarentena(
        df[mask_logicas].copy(), 
        pasta_auditoria, 
        f"duplicatas_logicas_{prefixo}.csv"
    )

    df = df[~mask_logicas].copy()
    log_etapa("Deduplicação", n_antes, len(df), prefixo)

    return df


# ============================================================

def validar_consistencia_grupo(
    df              : pd.DataFrame,
    coluna_id       : str,
    coluna_grupo    : str,
    pasta_auditoria : str,
    prefixo         : str = "",
) -> None:
    """
    Valida se cada valor de coluna_id está associado a apenas um valor de coluna_grupo.
    Casos inconsistentes vão para quarentena (mas não são removidos do fluxo principal).

    Exemplo: garantir que cada id_municipio pertence a apenas uma uf.
    """
    grupos_por_id = df.groupby(coluna_id)[coluna_grupo].nunique()
    ids_inconsistentes = grupos_por_id[grupos_por_id > 1].index

    if not ids_inconsistentes.empty:
        inconsistencias = df[df[coluna_id].isin(ids_inconsistentes)].copy()
        print(
            f"  ⚠  [{prefixo}] {len(ids_inconsistentes)} IDs com {coluna_grupo} inconsistente."
        )
        salvar_quarentena(
            inconsistencias,
            pasta_auditoria,
            f"inconsistencia_{coluna_id}_{coluna_grupo}_{prefixo}.csv",
        )
    else:
        print(f"  ✓  [{prefixo}] Consistência {coluna_grupo} × {coluna_id}: OK")


# ============================================================

def identificar_outliers(
    df              : pd.DataFrame,
    coluna          : str,
    pasta_auditoria : str,
    sufixo          : str = "",
    percentil       : float = 0.99,
) -> None:
    """
    Identifica e salva em quarentena valores acima do percentil informado.
    Não remove automaticamente, apenas para auditoria e revisão manual.
    """
    if df.empty:
        return

    limiar = df[coluna].quantile(percentil)
    suspeitos = df[df[coluna] > limiar].copy()

    salvar_quarentena(
        suspeitos, 
        pasta_auditoria, 
        f"outliers_p{int(percentil * 100)}{sufixo}.csv"
    )

    print(
        f"  P{int(percentil * 100)} {coluna}: {limiar:,.2f} - {len(suspeitos)} linhas acima do limiar"
    )
