import pandas as pd
from arquivos.ler_arquivo      import ler_csv
from arquivos.salvar_arquivo   import salvar_csv
from configs.caminhos          import (
    ARQUIVO_CONSOLIDADO_VENDAS_ANP,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    AUDITORIA_VENDAS,
    ARQUIVO_VENDAS_ETANOL,
    ARQUIVO_VENDAS_DIESEL,
    ARQUIVO_VENDAS_GASOLINA,
    ARQUIVO_TIPOS_COMBUSTIVEL,
)
from configs.constantes        import (
    ANO_INICIO_ESCOPO_PROJETO,
    ANO_FIM_ESCOPO_PROJETO,
    UFS_ESCOPO,
    STRINGS_NULAS,
)
from configs.mapeamentos       import (
    MAPA_UF_SIGLA,
    MAPA_VENDAS,
)
from configs.colunas           import (
    COLUNAS_CRITICAS_VENDAS,
    COLUNAS_SAIDA_VENDAS,
    COLUNAS_IDENTIFICADORAS,
    COLUNAS_IDENTIFICADORAS_FINAIS,
)
from transformadores.texto     import normalizar_texto
from transformadores.tipos     import (
    colunas_para_inteiro,
    colunas_para_string,
    converter_decimal_br,
)
from transformadores.dataframe import (
    concatenar,
    ordenar_linhas,
    renomear_colunas,
    selecionar_colunas,
)
from utils.validacoes          import (
    validar_esquema,
    validar_existencia_em_referencia,
)
from utils.auditoria           import (
    separar_nulos,
    validar_regex,
    validar_dominio,
    validar_intervalo,
    validar_minimo,
    tratar_duplicidades,
    validar_consistencia_grupo,
    identificar_outliers,
)
from utils.log                 import (
    log,
)


# =========================================================
# CONFIGURAÇÕES
# =========================================================

ARQUIVOS = {
    "Etanol"     : ARQUIVO_VENDAS_ETANOL,
    "Diesel"     : ARQUIVO_VENDAS_DIESEL,
    "Gasolina C" : ARQUIVO_VENDAS_GASOLINA,
}

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def limpar_textos(df):
    """
    Normaliza colunas textuais e converte strings nulas em pd.NA.
    """
    for coluna in ["uf", "nome_combustivel", "id_municipio"]:
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
    """
    Converte os campos para seus tipos adequados.
    Valores inválidos viram pd.NA (via errors='coerce').
    """
    df = colunas_para_inteiro(df, ["ano"])

    df["uf"] = df["uf"].map(MAPA_UF_SIGLA)

    df = colunas_para_string(df, ["id_municipio"])
    df["id_municipio"] = df["id_municipio"].apply(
        lambda x: x.zfill(7) 
            if pd.notna(x) and x != "" 
            else pd.NA
    )

    df = converter_decimal_br(df, ["vol_vendido_m3"])

    return df


def aplicar_regras_de_dominio(df, origem, ids_combustiveis_validos):
    """
    Aplica regras de plausibilidade por coluna.
    Linhas reprovadas em cada regra vão para quarentena separada.
    """
    df = validar_intervalo(
        df, 
        coluna="ano", 
        minimo=ANO_INICIO_ESCOPO_PROJETO, 
        maximo=ANO_FIM_ESCOPO_PROJETO, 
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=origem
    )

    df = validar_dominio(
        df, 
        coluna="uf", 
        valores_validos=MAPA_UF_SIGLA.values(), 
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=origem
    )

    df = validar_dominio(
        df, 
        coluna="uf", 
        valores_validos=UFS_ESCOPO,  
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=f"{origem}_escopo"
    )

    df = validar_dominio(
        df, 
        coluna="id_combustivel", 
        valores_validos=ids_combustiveis_validos, 
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=origem
    )
    
    df = validar_minimo(
        df, 
        coluna="vol_vendido_m3", 
        minimo=0, 
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=origem
    )
    
    return df

# =========================================================
# PIPELINE COMPLETO DE UM ARQUIVO INDIVIDUAL
# =========================================================

def processar_arquivo(
        caminho_arquivo, 
        combustivel_fixo, 
        df_municipios,
        mapa_combustivel_id,
        ids_combustiveis_validos,
    ):
    """
    Executa o pipeline completo de limpeza de um arquivo individual.
    Cada etapa loga quantas linhas sobreviveram e salva os descartados em quarentena.
    """
    log(
        f"ARQUIVO {combustivel_fixo.upper()}:\n",
        separador_interno_antes=True
    )

    try:
        df = ler_csv(caminho_arquivo)
    
    except Exception as e:
        raise RuntimeError(
            f"Erro ao ler arquivo de vendas {caminho_arquivo}: {e}"
        )
    
    log("Registros lidos", len(df), tipo="sucesso")

    # Coluna temporária de rastreamento p/ identificar a origem nas quarentenas
    df["_arquivo_origem"] = combustivel_fixo
    origem = combustivel_fixo

    validar_esquema(
        df=df.drop(columns=["_arquivo_origem"]), 
        esperado=MAPA_VENDAS.keys(), 
        origem=origem
    )

    df = renomear_colunas(df, MAPA_VENDAS)
    df = limpar_textos(df)
    df = converter_tipos(df)

    id_combustivel = mapa_combustivel_id.get(combustivel_fixo)
    if id_combustivel is None:
        raise ValueError(
            f"Combustível '{combustivel_fixo}' não possui ID na tabela domínio."
        )
    df["id_combustivel"] = id_combustivel

    df = separar_nulos(
        df, 
        colunas=COLUNAS_CRITICAS_VENDAS, 
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=origem
    )

    df = validar_regex(
        df, 
        coluna="id_municipio", 
        regex=r"^\d{7}$", 
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=origem
    )
 
    df = aplicar_regras_de_dominio(df, origem, ids_combustiveis_validos)

    df = validar_existencia_em_referencia(
        df=df,
        df_ref=df_municipios,
        chaves_df=["id_municipio"],
        chaves_df_ref=["id_municipio"],
        caminho=AUDITORIA_VENDAS / f"fora_ibge_{origem}.csv",
    )

    df = tratar_duplicidades(df, COLUNAS_IDENTIFICADORAS, AUDITORIA_VENDAS, origem)

    validar_consistencia_grupo(
        df, 
        coluna_id="id_municipio", 
        coluna_grupo="uf", 
        pasta_auditoria=AUDITORIA_VENDAS, 
        prefixo=origem
    )

    log("Linhas aprovadas", len(df), tipo="sucesso")
    return df

# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_vendas():
    """
    Executa todas as operações necessárias para realizar 
    a limpeza dos arquivos de vendas.
    """
    log("PIPELINE VENDAS\n", separador_antes=True)
    
    try:
        df_municipios = ler_csv(ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE)
        df_combustiveis = ler_csv(ARQUIVO_TIPOS_COMBUSTIVEL) # Domínio dos combustíveis
    
    except Exception as e:
        raise RuntimeError(f"Falha ao carregar bases de referência: {e}")

    # Cria um mapa nome-id dos combustíveis existentes
    mapa_combustivel_id = dict(zip(
        df_combustiveis["nome_combustivel"], 
        df_combustiveis["id_combustivel"]
    ))

    ids_combustiveis_validos = set(
        df_combustiveis["id_combustivel"].dropna()
    )

    # Processa individualmente os arquivos de cada combustível
    dfs = [
        processar_arquivo(
            arquivo, 
            combustivel, 
            df_municipios, 
            mapa_combustivel_id,
            ids_combustiveis_validos
        )
        for combustivel, arquivo in ARQUIVOS.items()
    ]

    df_final = concatenar(dfs)
    df_final = df_final.drop(columns=["_arquivo_origem"], errors="ignore")
    
    df_final = selecionar_colunas(df_final, COLUNAS_SAIDA_VENDAS)
    df_final = ordenar_linhas(df_final, COLUNAS_IDENTIFICADORAS)

    # Outliers calculados no consolidado para comparar os 3 combustíveis juntos
    resultado_outliers = identificar_outliers(
        df_final,
        coluna="vol_vendido_m3",
        pasta_auditoria=AUDITORIA_VENDAS,
        sufixo="_consolidado"
    )

    # Verificação final: nenhuma duplicidade lógica pode sobrar
    n_dupl = df_final.duplicated(subset=COLUNAS_IDENTIFICADORAS_FINAIS).sum()
    if n_dupl > 0:
        raise ValueError(
            f"Duplicidade lógica no dataset final: {n_dupl} linhas. "
            f"Verifique os arquivos em {AUDITORIA_VENDAS}."
        )

    try:
        salvar_csv(df_final, ARQUIVO_CONSOLIDADO_VENDAS_ANP)

    except Exception as e:
        raise RuntimeError(f"Falha ao salvar output final: {e}")

    # Printa a mensagem final de resumo do pipeline
    log("Processamento finalizado:\n", separador_interno_antes=True)
    log("Total de registros finais", len(df_final))
    log("Combustíveis (IDs)", sorted(df_final['id_combustivel'].unique()))
    log(
        "Anos cobertos", 
        f"{int(df_final['ano'].min())} a {int(df_final['ano'].max())}"
    )
    if resultado_outliers is not None:
        limiar, quantidade = resultado_outliers
        log(
            f"P99 vol_vendido_m3",
            f"{limiar:,.2f} ({quantidade} linhas acima do limiar)",
            tipo="aviso",
        )
    log("Municípios distintos", df_final['id_municipio'].nunique())
    log("Auditoria", AUDITORIA_VENDAS)
    log("Arquivo limpo salvo em",  ARQUIVO_CONSOLIDADO_VENDAS_ANP)


if __name__ == "__main__":
    executar_ppl_vendas()
