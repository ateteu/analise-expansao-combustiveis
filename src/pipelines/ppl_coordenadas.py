from arquivos.ler_arquivo      import ler_csv
from arquivos.salvar_arquivo   import salvar_csv
from configs.caminhos          import (
    ARQUIVO_COORD_MUNICIPIOS,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    ARQUIVO_CONSOLIDADO_COORD,
    AUDITORIA_COORD_MUNICIPIOS,
)
from configs.constantes        import STRINGS_NULAS
from configs.mapeamentos       import (
    MAPA_COORD_MUNICIPIOS,
)
from configs.colunas           import (
    COLUNAS_CRITICAS_COORD_MUNICIPIOS,
)
from transformadores.texto     import normalizar_texto
from transformadores.tipos     import (
    colunas_para_string,
    colunas_para_float,
)
from transformadores.dataframe import (
    renomear_colunas,
    selecionar_colunas,
    ordenar_linhas,
)
from utils.validacoes          import (
    validar_esquema,
    validar_existencia_em_referencia,
)
from utils.auditoria           import (
    separar_nulos,
    validar_regex,
    validar_intervalo,
    tratar_duplicidades,
)
from utils.log                 import (
    log,
    log_etapa,
)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def limpar_textos(df):

    for coluna in df.columns:
        df[coluna] = df[coluna].apply(
            lambda x: normalizar_texto(
                x,
                remover_acentos=False,
                remover_pontuacao=False,
                strings_nulas=STRINGS_NULAS,
            )
        )

    return df


def converter_tipos(df):

    df = colunas_para_string(df, ["id_municipio"])

    df["id_municipio"] = (
        df["id_municipio"]
        .str.zfill(7)
    )

    df = colunas_para_float(
        df,
        ["latitude", "longitude"],
    )

    return df


def aplicar_regras(df, origem):

    df = validar_regex(
        df,
        coluna="id_municipio",
        regex=r"^\d{7}$",
        pasta_auditoria=AUDITORIA_COORD_MUNICIPIOS,
        prefixo=origem,
    )

    df = validar_intervalo(
        df,
        coluna="latitude",
        minimo=-90,
        maximo=90,
        pasta_auditoria=AUDITORIA_COORD_MUNICIPIOS,
        prefixo=origem,
    )

    df = validar_intervalo(
        df,
        coluna="longitude",
        minimo=-180,
        maximo=180,
        pasta_auditoria=AUDITORIA_COORD_MUNICIPIOS,
        prefixo=origem,
    )

    return df

# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_coordenadas():
    """
    Executa o pipeline completo de limpeza dos dados de coordenadas.
    """
    log("PIPELINE COORDENADAS\n", separador_antes=True)
    try:

        df = ler_csv(
            ARQUIVO_COORD_MUNICIPIOS,
            separador=","
        )
        df_municipios = ler_csv(
            ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE
        )

    except Exception as e:
        raise RuntimeError(f"Erro ao carregar bases: {e}")

    log("Registros lidos", len(df), tipo="sucesso")

    validar_esquema(df, MAPA_COORD_MUNICIPIOS.keys())

    df = renomear_colunas(df, MAPA_COORD_MUNICIPIOS)
    df = limpar_textos(df)
    df = converter_tipos(df)

    origem = "coordenadas"
    df = separar_nulos(
        df,
        colunas=COLUNAS_CRITICAS_COORD_MUNICIPIOS,
        pasta_auditoria=AUDITORIA_COORD_MUNICIPIOS,
        prefixo=origem,
    )

    tamanho_df_antes = len(df)
    log_etapa(
        "Separação de nulos",
        tamanho_df_antes,
        depois=len(df),
    )

    df = aplicar_regras(df, origem)
    df = tratar_duplicidades(
        df,
        chave_logica=["id_municipio"],
        pasta_auditoria=AUDITORIA_COORD_MUNICIPIOS,
        prefixo=origem,
    )

    df = validar_existencia_em_referencia(
        df=df,
        df_ref=df_municipios,
        chaves_df=["id_municipio"],
        chaves_df_ref=["id_municipio"],
        caminho=AUDITORIA_COORD_MUNICIPIOS / f"fora_ibge_{origem}.csv",
    )

    df = selecionar_colunas(
        df,
        col_mantidas=COLUNAS_CRITICAS_COORD_MUNICIPIOS,
    )

    df = ordenar_linhas(df, colunas=["id_municipio"])

    if df.duplicated(subset=["id_municipio"]).any():

        raise ValueError(
            "Duplicidade lógica encontrada após processamento."
        )

    salvar_csv(df, ARQUIVO_CONSOLIDADO_COORD)

    log("Processamento finalizado:\n", separador_interno_antes=True)

    log("Total de municípios", len(df))
    log("Auditoria", AUDITORIA_COORD_MUNICIPIOS)
    log("Arquivo limpo salvo em", ARQUIVO_CONSOLIDADO_COORD)


if __name__ == "__main__":
    executar_ppl_coordenadas()
