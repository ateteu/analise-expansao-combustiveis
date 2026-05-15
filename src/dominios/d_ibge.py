import pandas as pd
from pathlib               import Path
from arquivos.de_excel     import ler_excel
from transformadores.texto import normalizar_texto
from transformadores.tipos import (
    colunas_para_string, 
    colunas_para_inteiro
)
from configs.mapeamentos   import (
    SIGLAS_UF,
    CORRECOES_MUNICIPIOS
)
from configs.caminhos      import ARQUIVO_CODIGOS_IBGE
from configs.esquemas      import ESQUEMA_DOMINIO_IBGE
from configs.constantes    import INDICE_CABECALHO_IBGE


def _carregar_codigos_ibge(caminho: Path) -> pd.DataFrame:
    """
    Carrega a base oficial de municípios do IBGE e padroniza
    para uso como tabela de referência.
    """
    df = ler_excel(
        caminho      = caminho,
        pular_linhas = INDICE_CABECALHO_IBGE - 1,
        usar_colunas = list(ESQUEMA_DOMINIO_IBGE.keys())
    )

    df = df.rename(columns = ESQUEMA_DOMINIO_IBGE)

    # Troca nomes de UF por siglas correspondentes
    df["uf"] = (
        df["uf"]
        .str.strip()
        .map(SIGLAS_UF)
    )

    # Normaliza e padroniza tipo dos valores da coluna municipio
    df["municipio"] = df["municipio"].apply(normalizar_texto)
    df = colunas_para_string(df, ["municipio"])

    return df


def _corrigir_municipios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige nomes divergentes de municípios 
    (segundo erros da base de dados de frota SENATRAN) 
    para compatibilização com a base oficial IBGE.
    """
    # Para cada linha, busca correção pelo par (uf, municipio);
    # se não houver correção mapeada, mantém o valor original

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
    Faz merge com a tabela de referência IBGE
    para adicionar código do município.
    """
    # Remove linhas sem município informado
    df = df[
        df["municipio"] != "MUNICIPIO NAO INFORMADO"
    ]

    df = _corrigir_municipios(df)

    # Adiciona os dados do IBGE ao df solicitado
    df_ibge = _carregar_codigos_ibge(ARQUIVO_CODIGOS_IBGE)
    df = df.merge(
        df_ibge,
        on  = ["uf", "municipio"],
        how = "left"
    )

    # Garante que id_municipio é str
    # (estava aparecendo como float, por isso a conversão para int antes)
    df = colunas_para_inteiro(df, ["id_municipio"])
    df = colunas_para_string(df, ["id_municipio"])

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
