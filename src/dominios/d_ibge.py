import pandas as pd
from transformadores.tipos import colunas_para_string
from configs.mapeamentos   import CORRECOES_MUNICIPIOS
from configs.caminhos      import ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE


def _carregar_municipios_ibge() -> pd.DataFrame:
    """
    Carrega a tabela intermediária de municípios do IBGE.
    """

    df = pd.read_csv(
        ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
        sep = ";",
        dtype = str
    )

    return (
        df[
            [
                "id_municipio",
                "id_uf",
                "nome_municipio"
            ]
        ]
        .rename(
            columns={
                "id_uf": "uf",
                "nome_municipio": "municipio"
            }
        )
    )


def _corrigir_municipios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige nomes divergentes de municípios da base SENATRAN 
    para compatibilização com a base de referência do IBGE.
    """

    df["municipio"] = df.apply(
        lambda linha: CORRECOES_MUNICIPIOS.get(
            (
                linha["uf"],
                linha["municipio"]
            ),
            linha["municipio"]
        ),
        axis=1
    )

    return df


def adicionar_codigo_ibge(df: pd.DataFrame) -> pd.DataFrame:
    """
    Faz merge com a tabela de referência de municípios do IBGE 
    para adicionar o código do município.
    """

    # Remove linhas sem município informado
    df = df[
        df["municipio"] != "MUNICIPIO NAO INFORMADO"
    ].copy()

    # Corrige divergências conhecidas da SENATRAN
    df = _corrigir_municipios(df)

    # Carrega tabela de referência
    df_ibge = _carregar_municipios_ibge()

    # Adiciona código IBGE
    df = df.merge(
        df_ibge,
        on  = ["uf", "municipio"],
        how = "left"
    )

    # Garante tipo string
    df = colunas_para_string(
        df,
        ["id_municipio"]
    )

    municipios_sem_codigo = (
        df[df["id_municipio"].isna()]
        [["uf", "municipio"]]
        .drop_duplicates()
    )

    if not municipios_sem_codigo.empty:
        print(
            f"\n{len(municipios_sem_codigo)} município(s) sem código IBGE:"
        )

        print(
            municipios_sem_codigo
            .sort_values(["uf", "municipio"])
            .to_string(index=False)
        )

    return df
