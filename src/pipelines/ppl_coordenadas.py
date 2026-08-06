from arquivos.ler_arquivo      import ler_csv
from arquivos.salvar_arquivo   import salvar_csv
from configs.caminhos          import (
    ARQUIVO_COORD_MUNICIPIOS,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    ARQUIVO_CONSOLIDADO_COORD,
    AUDITORIA_COORD_MUNICIPIOS,
    DADOS_MODIFICADOS,
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


def validar_com_municipios(df, df_ref, origem):

    return validar_existencia_em_referencia(
        df=df,
        df_ref=df_ref,
        chaves_df=["id_municipio"],
        chaves_df_ref=["id_municipio"],
        diretorio_quarentena=AUDITORIA_COORD_MUNICIPIOS,
        nome_arquivo=f"fora_ibge_{origem}.csv",
        origem=origem,
    )


# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_coordenadas():

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

    print(f"Registros lidos: {len(df)}")

    validar_esquema(
        df,
        MAPA_COORD_MUNICIPIOS.keys(),
    )

    origem = "coordenadas"

    df = renomear_colunas(
        df,
        MAPA_COORD_MUNICIPIOS,
    )

    df = limpar_textos(df)
    df = converter_tipos(df)
    df = separar_nulos(
        df,
        colunas=COLUNAS_CRITICAS_COORD_MUNICIPIOS,
        pasta_auditoria=AUDITORIA_COORD_MUNICIPIOS,
        prefixo=origem,
    )

    df = aplicar_regras(
        df,
        origem,
    )

    df = tratar_duplicidades(
        df,
        chave_logica=["id_municipio"],
        pasta_auditoria=AUDITORIA_COORD_MUNICIPIOS,
        prefixo=origem,
    )

    df = validar_com_municipios(
        df,
        df_municipios,
        origem,
    )

    df = selecionar_colunas(
        df,
        col_mantidas=COLUNAS_CRITICAS_COORD_MUNICIPIOS,
    )

    df = ordenar_linhas(
        df,
        colunas=["id_municipio"],
    )

    if df.duplicated(subset=["id_municipio"]).any():

        raise ValueError(
            "Duplicidade lógica encontrada após processamento."
        )

    salvar_csv(
        df,
        pasta_saida=DADOS_MODIFICADOS,
        nome_arquivo="coordenadas_municipios.csv",
    )

    print(f"\n{'='*60}")
    print("PROCESSAMENTO FINALIZADO")
    print(f"{'='*60}")
    print(f"  Total de municípios : {len(df)}")
    print(f"  Arquivo salvo em    : {ARQUIVO_CONSOLIDADO_COORD}")
    print(f"  Auditoria           : {AUDITORIA_COORD_MUNICIPIOS}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    executar_ppl_coordenadas()
