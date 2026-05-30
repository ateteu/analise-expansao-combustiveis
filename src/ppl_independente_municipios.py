import pandas as pd
from arquivos.de_excel     import ler_excel
from transformadores.tipos import (
    colunas_para_string
)
from configs.caminhos      import (
    ARQUIVO_CODIGOS_IBGE,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE
)


# =========================================================
# CONFIGURAÇÕES
# =========================================================

INDICE_CABECALHO_IBGE = 7

ESQUEMA_TABELA_IBGE = {
    "UF": "id_uf",
    "Nome_UF": "nome_uf",
    "Região Geográfica Intermediária": "id_regiao_intermediaria",
    "Nome Região Geográfica Intermediária": "nome_regiao_intermediaria",
    "Região Geográfica Imediata": "id_regiao_imediata",
    "Nome Região Geográfica Imediata": "nome_regiao_imediata",
    "Código Município Completo": "id_municipio",
    "Nome_Município": "nome_municipio"
}

COLUNAS_FINAIS = [
    "id_municipio",
    "nome_municipio",
    "id_uf",
    "nome_uf",
    "id_regiao_imediata",
    "nome_regiao_imediata",
    "id_regiao_intermediaria",
    "nome_regiao_intermediaria"
]


# =========================================================
# ETAPA 1 - LEITURA
# =========================================================

def carregar_dados() -> pd.DataFrame:

    return ler_excel(
        caminho=ARQUIVO_CODIGOS_IBGE,
        pular_linhas=INDICE_CABECALHO_IBGE - 1,
        usar_colunas=list(ESQUEMA_TABELA_IBGE.keys())
    )


# =========================================================
# ETAPA 2 - VALIDAÇÃO DE SCHEMA
# =========================================================

def validar_schema(df: pd.DataFrame) -> None:

    colunas_recebidas = set(df.columns)
    colunas_esperadas = set(ESQUEMA_TABELA_IBGE.keys())

    if colunas_recebidas != colunas_esperadas:

        faltando = sorted(
            colunas_esperadas - colunas_recebidas
        )

        sobrando = sorted(
            colunas_recebidas - colunas_esperadas
        )

        raise ValueError(
            "Schema IBGE inválido.\n"
            f"Faltando: {faltando}\n"
            f"Sobrando: {sobrando}"
        )


# =========================================================
# ETAPA 3 - PADRONIZAÇÃO DE COLUNAS
# =========================================================

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:

    df = df.rename(
        columns=ESQUEMA_TABELA_IBGE
    )

    return df[COLUNAS_FINAIS].copy()


# =========================================================
# ETAPA 4 - LIMPEZA LEVE DE TEXTOS
# =========================================================

def limpar_textos(df: pd.DataFrame) -> pd.DataFrame:

    colunas_texto = [
        "nome_municipio",
        "nome_uf",
        "nome_regiao_imediata",
        "nome_regiao_intermediaria"
    ]

    for coluna in colunas_texto:

        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.strip()
        )

    return df


# =========================================================
# ETAPA 5 - CONVERSÃO DE TIPOS
# =========================================================

def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:

    colunas_codigo = [
        "id_municipio",
        "id_uf",
        "id_regiao_imediata",
        "id_regiao_intermediaria"
    ]

    df = colunas_para_string(
        df,
        colunas_codigo
    )

    for coluna in colunas_codigo:

        df[coluna] = (
            df[coluna]
            .str.strip()
        )

    df["id_municipio"] = (
        df["id_municipio"]
        .str.zfill(7)
    )

    return df


# =========================================================
# ETAPA 6 - DUPLICATAS EXATAS
# =========================================================

def remover_duplicatas_exatas(
    df: pd.DataFrame
) -> pd.DataFrame:

    antes = len(df)

    df = df.drop_duplicates()

    removidas = antes - len(df)

    if removidas > 0:

        print(
            f"Duplicatas exatas removidas: {removidas}"
        )

    return df


# =========================================================
# ETAPA 7 - VALIDAÇÕES
# =========================================================

def validar_nulos(df: pd.DataFrame) -> None:

    linhas_invalidas = df[
        df[COLUNAS_FINAIS]
        .isnull()
        .any(axis=1)
    ]

    if not linhas_invalidas.empty:

        raise ValueError(
            f"Foram encontrados {len(linhas_invalidas)} registros com valores nulos."
        )


def validar_id_municipio(df: pd.DataFrame) -> None:

    invalidos = df[
        ~df["id_municipio"]
        .str.match(r"^\d{7}$", na=False)
    ]

    if not invalidos.empty:

        raise ValueError(
            f"Foram encontrados {len(invalidos)} códigos de município inválidos."
        )


def validar_unicidade_id_municipio(
    df: pd.DataFrame
) -> None:

    duplicados = df[
        df["id_municipio"]
        .duplicated(keep=False)
    ]

    if not duplicados.empty:

        raise ValueError(
            f"Foram encontrados "
            f"{duplicados['id_municipio'].nunique()} "
            f"códigos de município duplicados."
        )


def validar_consistencia_uf(
    df: pd.DataFrame
) -> None:

    inconsistentes = df[
        df["id_municipio"].str[:2]
        != df["id_uf"]
    ]

    if not inconsistentes.empty:

        raise ValueError(
            f"Foram encontrados "
            f"{len(inconsistentes)} municípios "
            f"com UF incompatível."
        )


def validar_quantidade_municipios(
    df: pd.DataFrame
) -> None:

    if len(df) < 5560:

        print(
            f"⚠ Quantidade de municípios abaixo do esperado: {len(df)}"
        )


# =========================================================
# ETAPA 8 - ORDENAÇÃO
# =========================================================

def ordenar(df: pd.DataFrame) -> pd.DataFrame:

    return df.sort_values(
        by=[
            "id_uf",
            "nome_municipio"
        ],
        ignore_index=True
    )


# =========================================================
# PIPELINE
# =========================================================

def processar_municipios_ibge() -> pd.DataFrame:

    print("Carregando base do IBGE...")

    df = carregar_dados()
    print(
        f"Registros lidos: {len(df)}"
    )

    validar_schema(df)
    df = padronizar_colunas(df)
    df = limpar_textos(df)
    df = converter_tipos(df)
    df = remover_duplicatas_exatas(df)
    validar_nulos(df)
    validar_id_municipio(df)
    validar_unicidade_id_municipio(df)
    validar_consistencia_uf(df)
    validar_quantidade_municipios(df)
    df = ordenar(df)

    print(
        f"Municípios válidos: {len(df)}"
    )

    return df


# =========================================================
# EXECUÇÃO
# =========================================================

def main():

    df = processar_municipios_ibge()

    df.to_csv(
        ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
        sep=";",
        index=False,
        encoding="utf-8"
    )

    print(
        f"Arquivo salvo em: {ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE}"
    )


if __name__ == "__main__":
    main()
