import pandas as pd
from arquivos.ler_arquivo      import ler_csv
from arquivos.salvar_arquivo   import salvar_quarentena
from configs.constantes        import (
    STRINGS_NULAS,
)
from configs.esquemas          import (
    ESQUEMA_ORIGINAL_COORD_MUNICIPIOS
)
from configs.colunas           import (
    COLUNAS_CRITICAS_COORD_MUNICIPIOS
)
from configs.caminhos          import (
    AUDITORIA_COORD_MUNICIPIOS,
    ARQUIVO_CONSOLIDADO_COORD,
    ARQUIVO_CODIGOS_IBGE,
    ARQUIVO_COORD_MUNICIPIOS
)
from transformadores.texto     import normalizar_texto
from utils.log                 import log_etapa

# =========================================================
# ETAPA 2 - VALIDAR SCHEMA
# =========================================================

def validar_schema(df):

    recebidas = set(df.columns)

    if recebidas != ESQUEMA_ORIGINAL_COORD_MUNICIPIOS:

        faltando = ESQUEMA_ORIGINAL_COORD_MUNICIPIOS - recebidas
        sobrando = recebidas - ESQUEMA_ORIGINAL_COORD_MUNICIPIOS

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
        "latitude": "latitude",
        "longitude": "longitude",
    })

# =========================================================
# ETAPA 4 - LIMPEZA
# =========================================================

def limpar(df):

    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: normalizar_texto(
                x,
                remover_acentos=False,
                remover_pontuacao=False,
                strings_nulas=STRINGS_NULAS,
            )
        )

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

    mask = df[COLUNAS_CRITICAS_COORD_MUNICIPIOS].isnull().any(axis=1)

    invalidas = df[mask].copy()

    salvar_quarentena(
        invalidas,
        AUDITORIA_COORD_MUNICIPIOS,
        "nulos_criticos.csv"
    )

    df_ok = df[~mask].copy()

    log_etapa("Nulos críticos", len(df), len(df_ok))

    return df_ok

# =========================================================
# ETAPA 7 - VALIDAR FORMATO
# =========================================================

def validar_formatos(df):

    mask_id = df["id_municipio"].str.match(
        r"^\d{7}$",
        na=False,
    )
    mask_lat = df["latitude"].between(-90, 90)
    mask_lon = df["longitude"].between(-180, 180)
    
    mask_final = (
        mask_id &
        mask_lat &
        mask_lon
    )

    invalidas = df[~mask_final].copy()

    salvar_quarentena(
        invalidas,
        AUDITORIA_COORD_MUNICIPIOS,
        "formato_invalido.csv"
    )

    df_ok = df[mask_final].copy()

    log_etapa("Validação formato", len(df), len(df_ok))

    return df_ok

# =========================================================
# ETAPA 8 - DEDUP
# =========================================================

def tratar_duplicidades(df):

    chave = ["id_municipio"]

    # duplicata exata
    duplicatas_exatas = df[df.duplicated(keep=False)]

    salvar_quarentena(
        duplicatas_exatas,
        AUDITORIA_COORD_MUNICIPIOS,
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
        AUDITORIA_COORD_MUNICIPIOS,
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
        "Código Município Completo"
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

    df = df[["id_municipio"]].copy()

    df["id_municipio"] = (
        df["id_municipio"]
        .str.strip()
        .str.zfill(7)
    )

    return df


def validar_com_ibge(df, df_ibge):

    chaves_validas = set(
        zip(
            df_ibge["id_municipio"]
        )
    )

    chaves_df = list(
        zip(
            df["id_municipio"]
        )
    )

    mask = pd.Series(
        [c in chaves_validas for c in chaves_df],
        index=df.index,
    )

    invalidas = df[~mask].copy()

    salvar_quarentena(
        invalidas,
        AUDITORIA_COORD_MUNICIPIOS,
        "fora_referencia_ibge.csv"
    )

    df_ok = df[mask].copy()

    log_etapa("Validação IBGE", len(df), len(df_ok))

    return df_ok

# =========================================================
# ETAPA 10 - EXPORT FINAL
# =========================================================

def exportar(df):

    df = (
        df[COLUNAS_CRITICAS_COORD_MUNICIPIOS]
        .sort_values(
            by=["id_municipio"]
        )
        .reset_index(drop=True)
    )

    df.to_csv(
        ARQUIVO_CONSOLIDADO_COORD,
        sep=";",
        index=False,
        encoding="utf-8",
    )

    print(f"\nArquivo salvo em: {ARQUIVO_CONSOLIDADO_COORD}")

# =========================================================
# MAIN
# =========================================================

def main():

    print("Carregando referência IBGE...")
    df_ibge = carregar_ibge(ARQUIVO_CODIGOS_IBGE)

    print("Lendo CSV...")
    df = ler_csv(ARQUIVO_COORD_MUNICIPIOS)

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
