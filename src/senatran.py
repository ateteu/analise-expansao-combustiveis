import pandas as pd
from pathlib import Path
from utils import normalizar_texto


def _engine_para(caminho: Path) -> str:
    return "xlrd" if caminho.suffix == ".xls" else "openpyxl"


def _aba_para(caminho: Path) -> str | int:
    """
    O arquivo de 2015 tem duas abas; a útil é 'JUL_2015'.
    Todos os outros têm uma aba só — usa índice 0.
    """
    return "JUL_2015" if "15" in caminho.name else 0


def _ler_bruto(caminho: Path) -> pd.DataFrame:
    """Lê o arquivo sem cabeçalho para inspeção da estrutura."""
    return pd.read_excel(
        caminho,
        sheet_name=_aba_para(caminho),
        header=None,
        engine=_engine_para(caminho),
    )


def _encontrar_linha_cabecalho(df_bruto: pd.DataFrame) -> int:
    """
    Percorre as linhas do DataFrame bruto procurando aquela que contém
    'UF', 'MUNIC' e 'TOTAL' — padrão do cabeçalho SENATRAN.
    """
    for indice, linha in df_bruto.iterrows():
        valores = linha.astype(str).str.upper()
        if (
            valores.str.contains("UF", na=False).any()
            and valores.str.contains("MUNIC", na=False).any()
            and valores.str.contains("TOTAL", na=False).any()
        ):
            return indice
    raise ValueError("Cabeçalho não encontrado no arquivo.")


def _ler_com_cabecalho(caminho: Path, skiprows: int) -> pd.DataFrame:
    """Lê o arquivo já pulando as linhas anteriores ao cabeçalho."""
    return pd.read_excel(
        caminho,
        sheet_name=_aba_para(caminho),
        skiprows=skiprows,
        engine=_engine_para(caminho),
    )


def _padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df


def _verificar_colunas_essenciais(df: pd.DataFrame, caminho: Path) -> None:
    for col in ["UF", "MUNICIPIO"]:
        if col not in df.columns:
            raise ValueError(f"Coluna '{col}' ausente em {caminho.name}")


def _limpar(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas inválidas: sem UF, cabeçalhos duplicados, UF != 2 chars."""
    df = df[df["UF"].notna()]
    df = df[df["UF"].astype(str) != "UF"]
    df = df[df["UF"].astype(str).str.len() == 2]
    df = df.dropna(how="all")
    return df


def _padronizar_municipio(df: pd.DataFrame) -> pd.DataFrame:
    df["MUNICIPIO"] = df["MUNICIPIO"].apply(normalizar_texto)
    df["UF"] = df["UF"].str.strip().str.upper()
    return df


def _adicionar_ano(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    df["ANO"] = ano
    return df


# ---------------------------------------------------------------------------
# Função principal — única interface pública deste módulo
# ---------------------------------------------------------------------------

def processar_arquivo(caminho: Path, ano: int) -> pd.DataFrame:
    """
    Pipeline completo para um arquivo SENATRAN:
    lê, encontra cabeçalho, padroniza, limpa, normaliza e adiciona ano.
    """
    df_bruto = _ler_bruto(caminho)
    indice_cabecalho = _encontrar_linha_cabecalho(df_bruto)

    df = _ler_com_cabecalho(caminho, skiprows=indice_cabecalho)
    df = _padronizar_colunas(df)
    _verificar_colunas_essenciais(df, caminho)
    df = _limpar(df)
    df = _padronizar_municipio(df)
    df = _adicionar_ano(df, ano)

    return df
