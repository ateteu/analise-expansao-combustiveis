import pandas as pd

from arquivos.ler_arquivo      import ler_excel
from arquivos.salvar_arquivo   import salvar_csv
from transformadores.tipos     import colunas_para_string
from transformadores.texto     import normalizar_texto
from transformadores.dataframe import (
    renomear_colunas,
    selecionar_colunas,
    ordenar_linhas,
)
from utils.validacoes          import (
    validar_esquema,
    validar_unicidade,
    validar_prefixo,
)
from utils.auditoria           import (
    separar_nulos, 
    validar_regex, 
    tratar_duplicidades
)
from configs.caminhos          import (
    ARQUIVO_CODIGOS_IBGE,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    AUDITORIA_MUNICIPIOS, 
)
from configs.mapeamentos       import MAPA_CODIGOS_IBGE
from configs.constantes        import (
    INDICE_CABECALHO_IBGE, 
    STRINGS_NULAS,
)
from utils.log                 import (
    log,
)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def carregar_dados() -> pd.DataFrame:
    """
    Lê a planilha de códigos do IBGE, restringindo às colunas mapeadas.
    """
    return ler_excel(
        caminho=ARQUIVO_CODIGOS_IBGE,
        pular_linhas=INDICE_CABECALHO_IBGE - 1,
        usar_colunas=list(MAPA_CODIGOS_IBGE.keys()),
    )


def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renomeia e seleciona as colunas conforme o mapeamento padrão.
    """
    df = renomear_colunas(df, MAPA_CODIGOS_IBGE)
    return selecionar_colunas(df, MAPA_CODIGOS_IBGE.values())


def limpar_textos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza colunas de exibição (nome de município, UF, etc.).
    Sem maiúsculo/sem remover acento: são campos de exibição, não chave de join.
    """
    colunas_texto = [
        "nome_municipio",
        "nome_uf",
        "nome_regiao_imediata",
        "nome_regiao_intermediaria",
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].apply(
            lambda x: normalizar_texto(
                x,
                maiusculo=False,
                remover_acentos=False,
                remover_pontuacao=False,
                strings_nulas=STRINGS_NULAS,
            )
        )

    return df


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte códigos para string e aplica zero-fill em id_municipio.
    """
    colunas_codigo = [
        "id_municipio",
        "id_uf",
        "id_regiao_imediata",
        "id_regiao_intermediaria",
    ]

    df = colunas_para_string(df, colunas_codigo)
    df["id_municipio"] = df["id_municipio"].str.zfill(7)

    return df


def tratar_duplicatas_exatas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicatas exatas, usando todas as colunas como chave.
    """
    return tratar_duplicidades(
        df,
        chave_logica=list(df.columns),
        pasta_auditoria=AUDITORIA_MUNICIPIOS,
        prefixo="municipios",
    )


def validar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Levanta erro se houver nulos nas colunas finais (referência exige dados completos).
    """
    n_antes = len(df)
    df_valido = separar_nulos(
        df, 
        colunas=list(MAPA_CODIGOS_IBGE.values()), 
        pasta_auditoria=AUDITORIA_MUNICIPIOS, 
        prefixo="municipios"
    )

    if len(df_valido) < n_antes:
        raise ValueError(
            f"Encontrados {n_antes - len(df_valido)} registros com nulos. "
            f"Verifique a quarentena em {AUDITORIA_MUNICIPIOS}."
        )

    return df_valido


def validar_id_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Levanta erro se algum id_municipio não tiver exatamente 7 dígitos.
    """
    n_antes = len(df)
    df_valido = validar_regex(
        df, 
        coluna="id_municipio", 
        regex=r"^\d{7}$", 
        pasta_auditoria=AUDITORIA_MUNICIPIOS, 
        prefixo="municipios"
    )

    if len(df_valido) < n_antes:
        raise ValueError(
            f"Encontrados {n_antes - len(df_valido)} códigos de município inválidos. "
            f"Verifique a quarentena em {AUDITORIA_MUNICIPIOS}."
        )

    return df_valido


def validar_quantidade_municipios(df: pd.DataFrame) -> None:
    """
    Avisa (sem interromper) se o total de municípios 
    estiver abaixo do esperado (5560).
    """
    if len(df) < 5560:
        log(
            f"Quantidade de municípios abaixo do esperado: {len(df)}", 
            tipo="aviso"
        )

# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_municipios() -> None:
    """
    Executa o pipeline de municípios e salva o resultado consolidado.
    """
    log("PIPELINE MUNICÍPIOS\n", separador_antes=True)

    try:
        df = carregar_dados()

    except Exception as e:
        raise RuntimeError(
            f"Erro ao ler arquivo do IBGE {ARQUIVO_CODIGOS_IBGE}: {e}"
        )

    log("Registros lidos", len(df), tipo="sucesso")

    # Garante que o arquivo de origem não mudou de formato
    validar_esquema(df, MAPA_CODIGOS_IBGE.keys())

    # Padronização estrutural: nomes de coluna, texto e tipos
    df = padronizar_colunas(df)
    df = limpar_textos(df)
    df = converter_tipos(df)

    # Remoção de duplicatas exatas (linha inteira repetida)
    df = tratar_duplicatas_exatas(df)

    # Validações de integridade; qualquer falha aqui interrompe o pipeline
    df = validar_nulos(df)
    df = validar_id_municipio(df)
    validar_unicidade(df, "id_municipio")
    validar_prefixo(df, "id_municipio", "id_uf", tamanho=2)
    validar_quantidade_municipios(df)

    df = ordenar_linhas(df, ["id_uf", "nome_municipio"])

    try:
        salvar_csv(df, ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE)

    except Exception as e:
        raise RuntimeError(f"Falha ao salvar output final: {e}")

    log("Processamento finalizado:\n", separador_interno_antes=True)

    log("Total de municípios", len(df))
    log("UFs", len(df['id_uf'].unique()))
    log("Regiões intermediárias", df['id_regiao_intermediaria'].nunique())
    log("Regiões imediatas", df['id_regiao_imediata'].nunique())
    log("Auditoria", AUDITORIA_MUNICIPIOS)
    log("Arquivo limpo salvo em", ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE)


if __name__ == "__main__":
    executar_ppl_municipios()
