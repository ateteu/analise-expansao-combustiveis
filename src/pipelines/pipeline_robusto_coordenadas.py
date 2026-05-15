import pandas as pd
import unicodedata
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================

# Diretório do script
BASE_DIR = Path(__file__).resolve().parents[2]

# Diretórios de dados
DIR_DADOS_BRUTOS = BASE_DIR / "dados" / "1-brutos"
DIR_DADOS_INTERMEDIARIOS = BASE_DIR / "dados" / "2-intermediarios"

# Arquivo de coordenadas
DIR_COORD = DIR_DADOS_BRUTOS / "lat-lon-github"
ARQUIVO_ENTRADA = DIR_COORD / "municipios.csv"

# IBGE
ARQUIVO_IBGE = (
    DIR_DADOS_BRUTOS
    / "codigos-ibge"
    / "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
)

ARQUIVO_SAIDA = (
    DIR_DADOS_INTERMEDIARIOS
    / "coordenadas_municipios.csv"
)

PASTA_AUDITORIA = DIR_DADOS_INTERMEDIARIOS / "auditoria-coord-municipios"
PASTA_AUDITORIA.mkdir(exist_ok=True)

# =========================================================
# SCHEMAS
# =========================================================

SCHEMA_ORIGINAL = {
    "codigo_ibge",
    "nome",
    "latitude",
    "longitude",
    "capital",
    "codigo_uf",
    "siafi_id",
    "ddd",
    "fuso_horario",
}

COLUNAS_FINAIS = [
    "id_municipio",
    "uf",
    "latitude",
    "longitude",
]

COLUNAS_CRITICAS = [
    "id_municipio",
    "uf",
    "latitude",
    "longitude",
]

MAPA_UF_CODIGO = {
    "11", "12", "13", "14", "15", "16", "17",
    "21", "22", "23", "24", "25", "26", "27",
    "28", "29",
    "31", "32", "33", "35",
    "41", "42", "43",
    "50", "51", "52", "53",
}

STRINGS_NULAS = {
    "", "NA", "N/A", "NULL", "NONE", "-", "--", "?"
}

# =========================================================
# HELPERS
# =========================================================

def normalizar_texto(valor):

    if pd.isna(valor):
        return pd.NA

    valor = str(valor).strip()
    valor = " ".join(valor.split())
    valor = unicodedata.normalize("NFKC", valor)

    if valor.upper() in STRINGS_NULAS:
        return pd.NA

    return valor


def salvar_quarentena(df, nome):

    if not df.empty:
        caminho = PASTA_AUDITORIA / nome

        df.to_csv(
            caminho,
            sep=";",
            index=False,
            encoding="utf-8",
        )

        print(f"⚠ Quarentena: {len(df)} linhas -> {caminho}")


def log_etapa(nome, antes, depois):

    descartadas = len(antes) - len(depois)

    print(
        f"{nome}: "
        f"{len(antes)} -> {len(depois)} "
        f"({descartadas} descartadas)"
    )

# =========================================================
# ETAPA 1 - LEITURA
# =========================================================

def ler_csv_seguro(caminho):

    df = pd.read_csv(
        caminho,
        dtype=str,
        keep_default_na=False,
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\ufeff", "", regex=False)
    )

    return df

# =========================================================
# ETAPA 2 - VALIDAR SCHEMA
# =========================================================

def validar_schema(df):

    recebidas = set(df.columns)

    if recebidas != SCHEMA_ORIGINAL:

        faltando = SCHEMA_ORIGINAL - recebidas
        sobrando = recebidas - SCHEMA_ORIGINAL

        raise ValueError(
            f"""
Schema inválido.

Faltando: {sorted(faltando)}
Sobrando: {sorted(sobrando)}
"""
        )

# =========================================================
# ETAPA 3 - PADRONIZAÇÃO
# =========================================================

def padronizar_colunas(df):

    return df.rename(columns={
        "codigo_ibge": "id_municipio",
        "codigo_uf": "uf",
        "latitude": "latitude",
        "longitude": "longitude",
    })

# =========================================================
# ETAPA 4 - LIMPEZA
# =========================================================

def limpar(df):

    for col in df.columns:
        df[col] = df[col].apply(normalizar_texto)

    return df

# =========================================================
# ETAPA 5 - TIPAGEM
# =========================================================

def converter_tipos(df):

    # ID município
    df["id_municipio"] = (
        df["id_municipio"]
        .str.strip()
        .str.zfill(7)
    )

    # uf
    df["uf"] = (
        df["uf"]
        .str.strip()
        .str.zfill(2)
    )

    # latitude
    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce",
    )

    # longitude
    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce",
    )

    return df

# =========================================================
# ETAPA 6 - NULOS CRÍTICOS
# =========================================================

def remover_nulos(df):

    mask = df[COLUNAS_CRITICAS].isnull().any(axis=1)

    invalidas = df[mask].copy()

    salvar_quarentena(
        invalidas,
        "nulos_criticos.csv"
    )

    df_ok = df[~mask].copy()

    log_etapa("Nulos críticos", df, df_ok)

    return df_ok

# =========================================================
# ETAPA 7 - VALIDAR FORMATO
# =========================================================

def validar_formatos(df):

    mask_id = df["id_municipio"].str.match(
        r"^\d{7}$",
        na=False,
    )
    mask_uf  = df["uf"].isin(MAPA_UF_CODIGO)
    mask_lat = df["latitude"].between(-90, 90)
    mask_lon = df["longitude"].between(-180, 180)
    
    mask_final = (
        mask_id &
        mask_uf &
        mask_lat &
        mask_lon
    )

    invalidas = df[~mask_final].copy()

    salvar_quarentena(
        invalidas,
        "formato_invalido.csv"
    )

    df_ok = df[mask_final].copy()

    log_etapa("Validação formato", df, df_ok)

    return df_ok

# =========================================================
# ETAPA 8 - DEDUP
# =========================================================

def tratar_duplicidades(df):

    chave = ["id_municipio", "uf"]

    # duplicata exata
    duplicatas_exatas = df[df.duplicated(keep=False)]

    salvar_quarentena(
        duplicatas_exatas,
        "duplicatas_exatas.csv"
    )

    df = df.drop_duplicates()

    # duplicata lógica
    mask_logica = df.duplicated(
        subset=chave,
        keep=False,
    )

    duplicatas_logicas = df[mask_logica].copy()

    salvar_quarentena(
        duplicatas_logicas,
        "duplicatas_logicas.csv"
    )

    df = df[~mask_logica].copy()

    return df

# =========================================================
# ETAPA 9 - REFERÊNCIA IBGE
# =========================================================

def carregar_ibge(caminho):

    df = pd.read_excel(
        caminho,
        dtype=str,
        skiprows=6,
    )

    colunas_esperadas = {
        "UF",
        "Código Município Completo",
    }

    faltando = (
        colunas_esperadas -
        set(df.columns)
    )

    if faltando:
        raise ValueError(
            f"Schema IBGE inválido: {faltando}"
        )

    df = df.rename(columns={
        "UF": "uf",
        "Código Município Completo": "id_municipio",
    })

    df = df[
        ["uf", "id_municipio"]
    ].copy()

    df["uf"] = (
        df["uf"]
        .str.strip()
        .str.zfill(2)
    )

    df["id_municipio"] = (
        df["id_municipio"]
        .str.strip()
        .str.zfill(7)
    )

    return df


def validar_com_ibge(df, df_ibge):

    chaves_validas = set(
        zip(
            df_ibge["uf"],
            df_ibge["id_municipio"],
        )
    )

    chaves_df = list(
        zip(
            df["uf"],
            df["id_municipio"],
        )
    )

    mask = pd.Series(
        [c in chaves_validas for c in chaves_df],
        index=df.index,
    )

    invalidas = df[~mask].copy()

    salvar_quarentena(
        invalidas,
        "fora_referencia_ibge.csv"
    )

    df_ok = df[mask].copy()

    log_etapa("Validação IBGE", df, df_ok)

    return df_ok

# =========================================================
# ETAPA 10 - EXPORT FINAL
# =========================================================

def exportar(df):

    df = (
        df[COLUNAS_FINAIS]
        .sort_values(
            by=["uf", "id_municipio"]
        )
        .reset_index(drop=True)
    )

    df.to_csv(
        ARQUIVO_SAIDA,
        sep=";",
        index=False,
        encoding="utf-8",
    )

    print(f"\nArquivo salvo em: {ARQUIVO_SAIDA}")

# =========================================================
# MAIN
# =========================================================

def main():

    print("Carregando referência IBGE...")
    df_ibge = carregar_ibge(ARQUIVO_IBGE)

    print("Lendo CSV...")
    df = ler_csv_seguro(ARQUIVO_ENTRADA)

    validar_schema(df)

    df = padronizar_colunas(df)

    df = limpar(df)

    df = converter_tipos(df)

    df = remover_nulos(df)

    df = validar_formatos(df)

    df = tratar_duplicidades(df)

    df = validar_com_ibge(df, df_ibge)

    exportar(df)

    print("\nProcessamento finalizado.")


if __name__ == "__main__":
    main()
