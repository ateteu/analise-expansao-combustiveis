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
)
from configs.esquemas          import (
    ESQUEMA_VENDAS_ANP,
    ESQUEMA_ORIGINAL_VENDAS,
)
from configs.constantes        import (
    ANO_INICIO_ESCOPO_PROJETO,
    ANO_FIM_ESCOPO_PROJETO,
    UFS_ESCOPO,
    STRINGS_NULAS,
)
from configs.mapeamentos       import MAPA_UF_SIGLA
from configs.colunas           import COLUNAS_CRITICAS_VENDAS
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


# =========================================================
# CONFIGURAÇÕES
# =========================================================

ARQUIVOS = {
    "ETANOL":   ARQUIVO_VENDAS_ETANOL,
    "DIESEL":   ARQUIVO_VENDAS_DIESEL,
    "GASOLINA": ARQUIVO_VENDAS_GASOLINA,
}

UFS_VALIDAS          = set(MAPA_UF_SIGLA.values())
COMBUSTIVEIS_VALIDOS = {"ETANOL", "DIESEL", "GASOLINA"}
CHAVE_LOGICA         = ["ano", "uf", "id_municipio", "tipo_combustivel"]


# =========================================================
# ETAPA 1 - VALIDAÇÃO CRUZADA COM OS MUNICÍPIOS DE REFERÊNCIA
# =========================================================

def validar_com_municipios(df, df_municipios, origem=""):
    """
    Valida se cada par (uf, id_municipio) existe na base de referência do IBGE
    já processada pelo pipeline de municípios.
    Linhas sem correspondência vão para quarentena.
    """
    return validar_existencia_em_referencia(
        df=df,
        df_ref=df_municipios,
        chaves_df=["uf", "id_municipio"],
        chaves_df_ref=["id_uf", "id_municipio"],
        diretorio_quarentena=AUDITORIA_VENDAS,
        nome_arquivo=f"fora_ibge_{origem}.csv",
        origem=origem,
    )


# =========================================================
# ETAPA 2 - LIMPEZA TEXTUAL
# =========================================================

def limpar_textos(df):
    """Normaliza colunas textuais e converte strings nulas em pd.NA."""
    for coluna in ["uf", "tipo_combustivel", "municipio"]:
        df[coluna] = df[coluna].apply(
            lambda x: normalizar_texto(
                x,
                remover_acentos=False,
                remover_pontuacao=False,
                strings_nulas=STRINGS_NULAS,
            )
        )
    return df


# =========================================================
# ETAPA 3 - CONVERSÃO DE TIPOS
# =========================================================

def converter_tipos(df):
    """
    Converte os campos para seus tipos adequados.
    Valores inválidos viram pd.NA (via errors='coerce').
    """
    df = colunas_para_inteiro(df, ["ano"])

    df["uf"] = df["uf"].map(MAPA_UF_SIGLA)

    df = colunas_para_string(df, ["id_municipio"])
    df["id_municipio"] = df["id_municipio"].apply(
        lambda x: x.zfill(7) if pd.notna(x) and x != "" else pd.NA
    )

    df = converter_decimal_br(df, ["volume_vendas_m3"])

    return df


# =========================================================
# ETAPA 4 - REGRAS DE DOMÍNIO
# =========================================================

def aplicar_regras_de_dominio(df, origem=""):
    """
    Aplica regras de plausibilidade por coluna.
    Linhas reprovadas em cada regra vão para quarentena separada.
    """
    df = validar_intervalo(df, "ano", ANO_INICIO_ESCOPO_PROJETO, ANO_FIM_ESCOPO_PROJETO, AUDITORIA_VENDAS, origem)
    df = validar_dominio(df, "uf", UFS_VALIDAS, AUDITORIA_VENDAS, origem)
    df = validar_dominio(df, "uf", UFS_ESCOPO,  AUDITORIA_VENDAS, f"{origem}_escopo")
    df = validar_dominio(df, "tipo_combustivel", COMBUSTIVEIS_VALIDOS, AUDITORIA_VENDAS, origem)
    df = validar_minimo(df, "volume_vendas_m3", 0, AUDITORIA_VENDAS, origem)
    
    return df


# =========================================================
# ETAPA 5 - PIPELINE COMPLETO DE UM ARQUIVO
# =========================================================

def processar_arquivo(caminho_arquivo, combustivel_fixo, df_municipios):
    """
    Executa o pipeline completo de limpeza de um arquivo individual.
    Cada etapa loga quantas linhas sobreviveram e salva os descartados em quarentena.
    """
    origem = combustivel_fixo
    print(f"\n{'='*60}")
    print(f"Processando: {caminho_arquivo}  [{origem}]")
    print(f"{'='*60}")

    df = ler_csv(caminho_arquivo)
    print(f"  Linhas lidas: {len(df)}")

    # Coluna de rastreamento: identifica a origem nas quarentenas.
    # Removida antes do output final.
    df["_arquivo_origem"] = combustivel_fixo

    validar_esquema(df.drop(columns=["_arquivo_origem"]), ESQUEMA_ORIGINAL_VENDAS, origem)

    df = renomear_colunas(df, ESQUEMA_ORIGINAL_VENDAS)
    df = limpar_textos(df)
    df = converter_tipos(df)
    df = separar_nulos(df, COLUNAS_CRITICAS_VENDAS, AUDITORIA_VENDAS, origem)
    df = validar_regex(df, "id_municipio", r"^\d{7}$", AUDITORIA_VENDAS, origem)

    # Força o combustível fixo após validação de nulos;
    # garante consistência mesmo que o campo venha errado na origem.
    df["tipo_combustivel"] = combustivel_fixo

    df = aplicar_regras_de_dominio(df, origem)
    df = validar_com_municipios(df, df_municipios, origem)
    df = tratar_duplicidades(df, CHAVE_LOGICA, AUDITORIA_VENDAS, origem)

    validar_consistencia_grupo(df, "id_municipio", "uf", AUDITORIA_VENDAS, origem)

    print(f"  ✓ [{origem}] Linhas aprovadas: {len(df)}")
    return df


# =========================================================
# ETAPA 6 - EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_vendas():
    print("Carregando base de referência de municípios...")
    df_municipios = ler_csv(ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE)
    print(f"  {len(df_municipios)} municípios carregados\n")

    dfs = [
        processar_arquivo(arquivo, combustivel, df_municipios)
        for combustivel, arquivo in ARQUIVOS.items()
    ]

    print(f"\n{'='*60}")
    print("Consolidando os 3 arquivos...")
    print(f"{'='*60}")

    df_final = concatenar(dfs)
    df_final = df_final.drop(columns=["_arquivo_origem"], errors="ignore")
    df_final = renomear_colunas(df_final, ESQUEMA_VENDAS_ANP)
    df_final = selecionar_colunas(df_final, list(ESQUEMA_VENDAS_ANP.values()))
    df_final = ordenar_linhas(df_final, ["ano", "uf", "id_municipio", "tipo_combustivel"])

    # Outliers calculados no consolidado para comparar os 3 combustíveis juntos
    identificar_outliers(
        df_final, 
        coluna="volume_vendas_m3", 
        pasta_auditoria=AUDITORIA_VENDAS, 
        sufixo="_consolidado"
    )

    # Verificação final: nenhuma duplicidade lógica pode sobrar
    n_dupl = df_final.duplicated(subset=CHAVE_LOGICA).sum()
    if n_dupl > 0:
        raise ValueError(
            f"Duplicidade lógica no dataset final: {n_dupl} linhas. "
            f"Verifique os arquivos em {AUDITORIA_VENDAS}."
        )

    salvar_csv(df_final, ARQUIVO_CONSOLIDADO_VENDAS_ANP)

    print(f"\n{'='*60}")
    print("PROCESSAMENTO FINALIZADO")
    print(f"{'='*60}")
    print(f"  Total de linhas finais : {len(df_final)}")
    print(f"  Combustíveis presentes : {sorted(df_final['tipo_combustivel'].unique())}")
    print(f"  Anos cobertos          : {int(df_final['ano'].min())} - {int(df_final['ano'].max())}")
    print(f"  Municípios distintos   : {df_final['id_municipio'].nunique()}")
    print(f"  Arquivo salvo em       : {ARQUIVO_CONSOLIDADO_VENDAS_ANP}")
    print(f"  Quarentena/auditoria   : {AUDITORIA_VENDAS}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    executar_ppl_vendas()
