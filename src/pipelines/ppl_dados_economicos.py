import pandas as pd

from arquivos.ler_arquivo      import ler_excel, ler_csv
from arquivos.salvar_arquivo   import salvar_csv
from configs.caminhos          import (
    ARQUIVO_DADOS_ECONOMICOS,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    DADOS_MODIFICADOS,
    AUDITORIA_DADOS_ECONOMICOS, 
)
from configs.mapeamentos       import MAPA_DADOS_ECONOMICOS
from configs.constantes        import (
    ANO_INICIO_ESCOPO_PROJETO,
    ANO_FIM_ESCOPO_PROJETO,
    STRINGS_NULAS,
)
from configs.colunas           import (
    ORDEM_LINHAS,
    ORDEM_COL_DADOS_ECONOMICOS, 
    COLUNAS_VAB_COMPONENTES,
    COLUNAS_NUM_DADOS_ECONOMICOS,
    COLUNAS_CRITICAS_DADOS_ECONOMICOS,
)
from transformadores.texto     import normalizar_texto
from transformadores.tipos     import (
    colunas_para_string,
    colunas_para_inteiro,
    colunas_para_float,
)
from transformadores.dataframe import (
    renomear_colunas,
    ordenar_linhas,
    reordenar_colunas,
)
from utils.validacoes          import (
    validar_esquema,
    validar_existencia_em_referencia,
)
from utils.auditoria           import (
    separar_nulos,
    validar_regex,
    validar_intervalo,
    validar_minimo,
    tratar_duplicidades,
    validar_soma_componentes,
    identificar_outliers,
)


# =========================================================
# FUNÇÕES DE APOIO
# =========================================================

def carregar_dados() -> pd.DataFrame:
    """
    Lê a planilha de dados econômicos do IBGE, restringindo às colunas mapeadas.
    """
    return ler_excel(
        caminho=ARQUIVO_DADOS_ECONOMICOS,
        usar_colunas=list(MAPA_DADOS_ECONOMICOS.keys()),
    )


def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renomeia as colunas conforme o mapeamento padrão.
    """
    return renomear_colunas(df, MAPA_DADOS_ECONOMICOS)


def limpar_textos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza as colunas de atividade econômica. Tratadas como 
    categóricas, já que podem ser usadas para agrupamento em análises.
    """
    colunas_texto = ["atividade_1", "atividade_2", "atividade_3"]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].apply(
            lambda x: normalizar_texto(
                x,
                remover_acentos=False,
                remover_pontuacao=False,
                strings_nulas=STRINGS_NULAS,
            )
        )

    return df


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte ano, id_municipio e colunas numéricas para os tipos adequados.
    """
    df = colunas_para_inteiro(df, ["ano"])
    df = colunas_para_string(df, ["id_municipio"])
    df["id_municipio"] = df["id_municipio"].str.zfill(7)
    df = colunas_para_float(df, COLUNAS_NUM_DADOS_ECONOMICOS)

    return df


def aplicar_regras_de_dominio(df: pd.DataFrame, origem: str = "") -> pd.DataFrame:
    """
    Aplica regras de plausibilidade: ano dentro do escopo e valores não-negativos.
    """
    df = validar_intervalo(
        df, 
        coluna="ano", 
        minimo=ANO_INICIO_ESCOPO_PROJETO, 
        maximo=ANO_FIM_ESCOPO_PROJETO,
        pasta_auditoria=AUDITORIA_DADOS_ECONOMICOS, 
        prefixo=origem,
    )

    # VAB e PIB não podem ser negativos; checagem por coluna
    for coluna in COLUNAS_NUM_DADOS_ECONOMICOS:
        df = validar_minimo(
            df, 
            coluna=coluna, 
            minimo=0, 
            pasta_auditoria=AUDITORIA_DADOS_ECONOMICOS, 
            prefixo=f"{origem}_{coluna}")

    return df


def validar_com_municipios(df: pd.DataFrame, df_municipios: pd.DataFrame, origem: str = "") -> pd.DataFrame:
    """
    Valida se o id_municipio existe na base de referência do IBGE.
    """
    return validar_existencia_em_referencia(
        df=df,
        df_ref=df_municipios,
        chaves_df=["id_municipio"],
        chaves_df_ref=["id_municipio"],
        diretorio_quarentena=AUDITORIA_DADOS_ECONOMICOS,
        nome_arquivo=f"fora_ibge_{origem}.csv",
        origem=origem,
    )

# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_dados_economicos() -> None:
    """
    Executa o pipeline completo de limpeza dos dados econômicos do IBGE.
    """
    try:
        df_municipios = ler_csv(ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE)
        df = carregar_dados()
    
    except Exception as e:
        raise RuntimeError(f"Falha ao carregar base de dados: {e}")

    print(f"Registros lidos: {len(df)}")

    # Garante que o arquivo de origem não mudou de formato
    validar_esquema(df, MAPA_DADOS_ECONOMICOS.keys())

    # Padronização estrutural: nomes de coluna, texto e tipos
    df = padronizar_colunas(df)
    df = limpar_textos(df)
    df = converter_tipos(df)

    origem = "dados_economicos"

    # Remove linhas sem os campos essenciais
    df = separar_nulos(
        df, 
        colunas=COLUNAS_CRITICAS_DADOS_ECONOMICOS, 
        pasta_auditoria=AUDITORIA_DADOS_ECONOMICOS, 
        prefixo=origem
    )

    # Valida formato do código do município (7 dígitos)
    df = validar_regex(
        df, 
        coluna="id_municipio", 
        regex=r"^\d{7}$", 
        pasta_auditoria=AUDITORIA_DADOS_ECONOMICOS, 
        prefixo=origem
    )

    # Validações de consistência e integridade
    df = aplicar_regras_de_dominio(df, origem)
    df = validar_com_municipios(df, df_municipios, origem)
    df = tratar_duplicidades(
        df, 
        chave_logica=["ano", "id_municipio"], 
        pasta_auditoria=AUDITORIA_DADOS_ECONOMICOS, 
        prefixo=origem
    )

    # Auditoria não bloqueante: VAB total deveria ~= soma dos componentes setoriais
    validar_soma_componentes(
        df, 
        coluna_total="vab_total", 
        colunas_componentes=COLUNAS_VAB_COMPONENTES, 
        pasta_auditoria=AUDITORIA_DADOS_ECONOMICOS, 
        prefixo=origem
    )

    identificar_outliers(
        df, 
        coluna="pib_per_capita", 
        pasta_auditoria=AUDITORIA_DADOS_ECONOMICOS, 
        sufixo=f"_{origem}"
    )

    # Ordenação do resultado final
    df = ordenar_linhas(df, ORDEM_LINHAS)
    df = reordenar_colunas(df, ORDEM_COL_DADOS_ECONOMICOS)

    # Verificação final: não pode sobrar duplicidade lógica
    n_dupl = df.duplicated(subset=["ano", "id_municipio"]).sum()
    if n_dupl > 0:
        raise ValueError(
            f"Duplicidade lógica no dataset final: {n_dupl} linhas. "
            f"Verifique {AUDITORIA_DADOS_ECONOMICOS}."
        )

    try:
        salvar_csv(df, DADOS_MODIFICADOS, "dados_economicos_ibge.csv")
    
    except Exception as e:
        raise RuntimeError(f"Falha ao salvar output final: {e}")

    print(f"\n{'='*60}")
    print("PROCESSAMENTO FINALIZADO")
    print(f"{'='*60}")
    print(f"  Total de linhas finais : {len(df)}")
    print(f"  Anos cobertos          : {int(df['ano'].min())} - {int(df['ano'].max())}")
    print(f"  Municípios distintos   : {df['id_municipio'].nunique()}")
    print(f"  Arquivo salvo em       : {DADOS_MODIFICADOS / 'dados_economicos_ibge.csv'}")
    print(f"  Quarentena/auditoria   : {AUDITORIA_DADOS_ECONOMICOS}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    executar_ppl_dados_economicos()
